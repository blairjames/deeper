# Deeper
Multi-Proccesing wrapper for NMAP
usage: deeper [-h] [--udp] [--tcp] [--time TIME] [--port_range PORT_RANGE]
              [--procs PROCS] [--fast]
              target

positional arguments:
  target                Network or host to scan

optional arguments:
  -h, --help            show this help message and exit
  --udp, -u             scan top 1000 UDP ports
  --tcp, -t             scan top 1000 TCP ports
  --time TIME, -T TIME  nmap time profile T1-5
  --port_range PORT_RANGE, -p PORT_RANGE
                        port range eg. "80-443", TCP SYN Scan
  --procs PROCS, -z PROCS
                        Number of processes to spawn
  --fast, -f            Use Masscan for performance, requires port range




