# intel amt honeypot
```
inspired by https://isc.sans.edu/forums/diary/Do+you+have+Intel+AMT+Then+you+have+a+problem+today+Intel+Active+Management+Technology+INTELSA00075/22364/

Inteneded to be run with packet capture in front, e.g. 
sudo tcpdump -nnvv -i eth0 -w intel_AMT_honeypot.pcap 'portrange 16992-16994 or port 623 or port 624'
```
