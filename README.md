# Deeper
Multi-Proccesing wrapper for NMAP

Maps all 65535 ports on a host in ~20 minutes.

Simplifies Enumeration, or allows user to input their own nmap commands.

usage: deeper [-h] [--nmap_command NMAP_COMMAND] [--udp] [--tcp]
              [--port_range PORT_RANGE]
              host

positional arguments:
  host                  -  Target of scan.

optional arguments:
  -h, --help            show this help message and exit
  
  --nmap_command NMAP_COMMAND, -n NMAP_COMMAND
                        nmap command with no ports specified."Must be enclosed in quotes." 
                        [Example: deeper "nmap -T2 -Pn -sS -v 127.0.0.1" 1-1024]
                        
  --udp, -u             scan top 1000 UDP ports
  
  --tcp, -t             scan top 1000 TCP ports
  
  --port_range PORT_RANGE, -p PORT_RANGE
  
                        port range eg. "80-443"
