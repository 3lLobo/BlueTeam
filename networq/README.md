# Secure The Networq


## Monitor traffic

Mirror traffic to your server on interface <ethX>

Set promisc mode on:
```bash
sudo ifconfig ethX promisc
```

## Suricata - docker

Can we do this from a container? ☑️

```bash
docker run --rm -d --net=host \
    --cap-add=net_admin --cap-add=net_raw --cap-add=sys_nice \
        -v $(pwd)/suricata/logs:/var/log/suricata \
		-v $(pwd)/suricata/config:/etc/suricata \
			-v $(pwd)/suricata/rules:/var/lib/suricata/rules \
				jasonish/suricata:latest -i <ethX>
```

Fine [detection rules](https://gist.githubusercontent.com/jgautheron/0bcd25e763b42ba338fc22eb208885f1/raw/8a24f482e0e6a710ca78c25275b3657c6b994c43/protoanomalies.rules).


Alexandira [library of rules](https://github.com/klingerko/nids-rule-library?tab=readme-ov-file).

## Zeek

Hypothesis: Zeek run on the host os uses less resources than running in a container.

Hypothesis2: Running two containers with net_admin raises the probability of a fck-up.

1. Installing [zeek on Debian](https://software.opensuse.org//download.html?project=security%3Azeek&package=zeek-lts)
2. Add zeek to zsh environment:
```bash
sudo echo 'PATH=$PATH:/opt/zeek/bin' >> /etc/zsh/zshenv
```
3. Create a service for persistent zeek monitoring:
```bash
sudo nvim /etc/systemd/system/zeek.service
```
```vim
[Unit]
Description=Zeek Network Security Monitor
After=network.target

[Service]
Type=simple
ExecStart=/opt/zeek/bin/zeek -i <ethX> -C LogAscii::use_json=T
Restart=allways
RestartSec=11
WorkingDirectory=/opt/zeek/logs

[Install]
WantedBy=multi-user.target
```
4. Start the service:
```bash
sudo systemctl enable zeek.service --now
```

