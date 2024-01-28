# Endpoint security

Security pracitces for your machine.

## Linux

### Auditd

Install auditd:

```bash
sudo apt install auditd
sudo systemctl enable auditd --now
```

Add rules from [Neo23x0/auditd](https://github.com/Neo23x0/auditd/blob/master/audit.rules):
  
```bash
sudo curl -O /etc/audit/rules.d/audit.rules https://raw.githubusercontent.com/Neo23x0/auditd/master/audit.rules
sudo systemctl restart auditd
```

TODO: Make this a cron job.

Elastic-agent can collect auditd logs with the `linux/auditd` module.
