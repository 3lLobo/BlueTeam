# Secure The Networq


## Monitor traffic

Mirror traffic to your server on interface <ethX>

Set promisc mode on:
```bash
sudo ifconfig ethX promisc
```

## Suricata

Can we do this from a container?

```bash
docker run --rm -d --net=host \
    --cap-add=net_admin --cap-add=net_raw --cap-add=sys_nice \
        -v $(pwd)/suricata/logs:/var/log/suricata \
		-v $(pwd)/suricata/config:/etc/suricata \
			-v $(pwd)/suricata/rules:/var/lib/suricata/rules \
				jasonish/suricata:latest -i ethX

```

Fine [detection rules](https://gist.githubusercontent.com/jgautheron/0bcd25e763b42ba338fc22eb208885f1/raw/8a24f482e0e6a710ca78c25275b3657c6b994c43/protoanomalies.rules).


Alexandira [library of rules](https://github.com/klingerko/nids-rule-library?tab=readme-ov-file).

## Zeek

