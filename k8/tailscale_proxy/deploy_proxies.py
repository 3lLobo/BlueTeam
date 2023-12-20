import os
import subprocess
import time
from dotenv import load_dotenv
from typing import Dict, List
import argparse
import addict
import re
import kubernetes as k8s

# cd into the directory of this file
os.chdir(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
print(f"Loading .env from:\n {dotenv_path}\n\n")
load_dotenv(dotenv_path)

# K8 config
k8s.config.load_kube_config()

# ipv4 regex
ip_v4_regex = r"(\b25[0-5]|\b2[0-4][0-9]|\b[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}"
re_ip = re.compile(ip_v4_regex)

# TODO: auto deploy proxies


def make_apply(
    cmd: str, namespace: str, envs: Dict[str, str], log_file: str = "log.txt"
) -> bool:
    """Pipe the make command into kubectl apply
    with given variables.
    Return True if successful, False otherwise.

    Args:
        cmd (str): Make command
        namespace (str): Namespace
        envs (Dict[str, str]): Environment variables
        log_file (str, optional): Log file path. Defaults to 'log.txt'.

    Returns:
        bool: Success status
    """
    with open(log_file, "a") as f:
        sp = subprocess.Popen(
            ["make", cmd],
            env=envs,
            stdout=subprocess.PIPE,
            stderr=f,
        )

        sp2 = subprocess.run(
            ["kubectl", "apply", "-n", namespace, "-f", "-"],
            stdin=sp.stdout,
            stdout=f,
            stderr=f,
        )

    sp.wait()
    return sp2.returncode == 0


def get_svc_ip(name: str, namespace: str) -> str:
    """Get the cluster ip of the service.

    Args:
        name (str): Service name
        namespace (str): Namespace

    Returns:
        str: Cluster ip
    """
    v1 = k8s.client.CoreV1Api()
    # Get all services
    svc_all = v1.list_namespaced_service(namespace)
    # Get the service
    svc = [s for s in svc_all.items if name in s.metadata.name]
    if len(svc) == 0:
        raise Exception(f"Service {name} not found in namespace {namespace}")
    elif len(svc) > 1:
        # Ask user to choose
        print(f"Found multiple services with name {name}")
        print("Please choose one:")
        for i, s in enumerate(svc):
            print(f"{i}: {s.metadata.name}\t{s.spec.cluster_ip}\t{s.spec.type}")
        choice = input()
        assert choice.isdigit()
        assert int(choice) < len(svc)
        svc = svc[int(choice)]
    else:
        svc = svc[0]
    # Get the cluster ip
    svc_ip = svc.spec.cluster_ip
    return svc_ip


def get_envs(name: str, namespace: str, is_auth: bool = False) -> Dict[str, str]:
    """Get environment variables for the instance name.

    Args:
        name (str): Instance name
        is_auth (bool, optional): Whether to include the authkey.
            Defaults to False.

    Returns:
        Dict[str, str]: Environment variables
    """
    svc_name = name
    dest_ip = get_svc_ip(svc_name, namespace)
    try:
        dest_ip = re_ip.search(dest_ip).group(0)
    except AttributeError:
        raise Exception(f"Failed to get ip for {name}\n{dest_ip}")

    print(f"k8 ip for {name}: {dest_ip}")
    envs = {
        # 'SA_NAME': f'tailscale',
        "SA_NAME": f"tailscale-{name}",
        "ROLE_NAME": f"tailscale-role-{name}",
        "TS_KUBE_SECRET": f"tailscale-auth-{name}",
        "CONTAINER_NAME": f"tailscale-{name}",
        "TS_DEST_IP": dest_ip,
    }
    if is_auth:
        envs["XXX"] = get_auth_key(name)

    return envs


def get_auth_key(name: str) -> str:
    """Get the auth key for the instance name,
    from a local .env file.

    Args:
        name (str): Instance name

    Returns:
        str: Auth key
    """
    key = "TS_API_KEY_" + name.upper()
    if key in os.environ:
        return os.environ.get(key)
    else:
        raise Exception(f"Auth key for {name} not found in .env")


def get_args() -> Dict[str, str]:
    """Parse args from command line.
    Service names are required.
    Namespace is optional.
    Authkeys are optional.

    Returns:
        Dict[str, str]: Args for building service proxies
    """
    parser = argparse.ArgumentParser(
        description="Deploy tailscale proxies for k8 services"
    )
    parser.add_argument("names", nargs="+", help="Service names")
    parser.add_argument("--namespace", "-n", help="Namespace", default="default")
    parser.add_argument(
        "--auth",
        "-a",
        nargs="?",
        help="Tailscale authkeys for each service",
        default=None,
    )

    args = parser.parse_args()
    args = addict.Dict(vars(args))
    return args


def main():
    """Main function"""

    args = get_args()
    names = args.names
    namespace = args.namespace

    is_auth = not args.auth is None

    for name in names:
        # Envs
        envs = get_envs(name, is_auth=is_auth, namespace=namespace)
        # Auth
        scs_auth = make_apply("authkey", namespace, envs)
        if not scs_auth:
            raise Exception(f"Failed to apply authkey for {name}")
        # RBAC
        scs_rbac = make_apply("rbac", namespace, envs)
        if not scs_rbac:
            raise Exception(f"Failed to apply rbac for {name}")
        # Proxy
        scs_proxy = make_apply("proxy", namespace, envs)
        if not scs_proxy:
            raise Exception(f"Failed to apply proxy for {name}")

        print(f"Tailscale proxy for started for {name} 🐳")


if __name__ == "__main__":
    main()
