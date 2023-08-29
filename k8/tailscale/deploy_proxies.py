import os
import subprocess
import time
from dotenv import load_dotenv
from typing import Dict, List

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
print(f'Loading .env from:\n {dotenv_path}\n\n')
load_dotenv(dotenv_path)

# TODO: auto deploy proxies

def make_apply(cmd: str, envs: Dict[str, str], log_file: str='log.txt') -> bool:
  """Pipe the make command into kubectl apply
  with given variables.
  Return True if successful, False otherwise.

  Args:
      cmd (str): Make command
      envs (Dict[str, str]): Environment variables
      log_file (str, optional): Log file path. Defaults to 'log.txt'.

  Returns:
      bool: Success status
  """
  with open(log_file, 'a') as f:
    sp = subprocess.Popen(['make', cmd], env=envs,
      stdout=subprocess.PIPE,
      stderr=f)
    
    sp2 = subprocess.run(['kubectl', 'apply', '-f', '-'],
      stdin=sp.stdout,
      stdout=f,
      stderr=f)
    
  sp.wait()
  return sp2.returncode == 0

def get_svc_name(name: str) -> str:
  """Get the service name for the instance name.

  Args:
      name (str): Instance name

  Returns:
      str: Service name
  """
  svc_names = {
    'kibana': 'kibana-kb-http',
    'elastic': 'elasticsearch-es-http',
    'fleet': 'fleet-server-agent-http',
  }
  return svc_names[name]  

def get_envs(name: str, is_auth: bool=False) -> Dict[str, str]:
  """Get environment variables for the instance name.

  Args:
      name (str): Instance name
      is_auth (bool, optional): Whether to include the authkey. Defaults to False.

  Returns:
      Dict[str, str]: Environment variables
  """
  svc_name = get_svc_name(name)
  dest_ip = subprocess.run(['kubectl', 'get', 'svc', svc_name, '-o', 'jsonpath={.spec.clusterIP}'], capture_output=True).stdout.decode('utf-8').strip()
  print(f'k8 ip for {name}: {dest_ip}')
  envs = {
    # 'SA_NAME': f'tailscale',
    'SA_NAME': f'tailscale-{name}',
    'ROLE_NAME': f'tailscale-role-{name}',
    'TS_KUBE_SECRET': f'tailscale-auth-{name}',
    'CONTAINER_NAME': f'tailscale-{name}',
    'TS_DEST_IP': dest_ip,
  }
  if is_auth:
    envs['XXX'] = get_auth_key(name)

  return envs

def get_auth_key(name: str) -> str:
  """Get the auth key for the instance name,
  from a local .env file.

  Args:
      name (str): Instance name

  Returns:
      str: Auth key
  """
  key = 'TS_API_KEY_' + name.upper()
  if key in os.environ:
    return os.environ.get(key)
  else:
    raise Exception(f'Auth key for {name} not found in .env')


def main():
  """Main function"""
  names = ['kibana', 'elastic', 'fleet']
  is_auth = False

  for name in names:
    # Envs
    envs = get_envs(name, is_auth=is_auth)
    # Auth
    if is_auth:
      scs_auth = make_apply('authkey', envs)
      if not scs_auth:
        raise Exception(f'Failed to apply authkey for {name}')
    # RBAC
    scs_rbac = make_apply('rbac', envs)
    if not scs_rbac:
      raise Exception(f'Failed to apply rbac for {name}')
    # Proxy
    scs_proxy = make_apply('proxy', envs)
    if not scs_proxy:
      raise Exception(f'Failed to apply proxy for {name}')
    
    print(f'Tailscale proxy for started for {name} 🐳 ')

if __name__ == '__main__':
  main()


