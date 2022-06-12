# BlueTeam Wolf

Building a SOC for my home network 🛡️🗡️

## Roadmap

Basically implement what I learn during the [SANS sec450]() course.

1. PiHole for DNS server/monitoring/vpn
2. VPN mobile traffic through PiHole.
3. Kibana for traffic analysis and event/warning creation.
4. TheHive for incident monitoring
5. Tunnel netFlow to Kibana/elasticsearch.
6. Tap full package traffic with WireShark for a day and
7. Clean your machine from all the crapy malware you've accumulated.

## PiHole

![PiHoleLogo](res/Vortex-R.webp)

Follow this [tutorial](https://docs.pi-hole.net/guides/vpn/openvpn/overview/) to set up the PiHole.

Steps:

1. Run the [docker-compose](/pihole/docker-compose.yaml) file to start the Docker container.
2. Open a remote VS code window inside the container.
3. Turn password off `sudo pihole -a -p`.
4.

## Clone the sec450 SOC

Parallel approach is to use the setup provided in the course. Therefore we copy the [docker-compose]() file from the SANS VM and run it on our machine.

Steps.

1. Adjust docker file:
   - Elasticsearch version changed to default dist v.8.2.2
   - Kibana version changed to kibana:8.2.2
   - Changed network name
   - Get token and password for kibana from inside the Elasticsearch container.
