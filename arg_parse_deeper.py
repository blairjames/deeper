
import argparse
import os
import datetime
import exceptor

#TODO: make imp0rts from
#validate ip addresses - no letters no more than 3 digits
class Argparse_Deeper:

    def __init__(self):
        self.exceptor = exceptor.Exceptor()
        self.timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.top_udp = False
        self.top_tcp = False
        self.ports = False
        self.no_random = False
        self.ip_splitting = False
        self.top_ten = False
        self.internal_assessment = False
        self.command = ""
        self.target = ""
        self.scan_type = ""
        self.min = ""
        self.max = ""
        self.port = ""
        self.logfile = ""
        self.port_cnt: int = 0
        self.procs: int = 0
        self.port_list = []

    def check_for_network_address(self):
        if self.target.split(".")[3] == "0":
            self.target = self.target + "/24"
            self.ip_splitting = True
            log_target = self.target.replace("/", "_")
            self.logfile = os.getcwd() + "/deeper_" + log_target + "_" + self.timestamp + ".log"
            return True
        else:
            return False


    def get_args(self) -> argparse:
        try:
            args = argparse.ArgumentParser()
            args.add_argument("target", help="Network or host to scan", type=str)
            args.add_argument("--udp", "-sU", help="UDP Scan, default -sS syn", action='store_true')
            args.add_argument("--tcp", "-sT", help="TCP Scan, default -sS syn", action='store_true')
            args.add_argument("--ip", "-i", help="Spawn processes per IP, rather than by port. "
                                                 "Use when scanning a larger network for a single port.",
                                                 action="store_true")
            args.add_argument("--ver", "-sV", help="Determine service/version info", action='store_true')
            args.add_argument("--time", "-T", help="nmap time profile T1-5, default -T2")
            args.add_argument("--ports", "-p", help="Port range eg. \"80-443\"", type=str)
            args.add_argument("--internal", help="Ports for internal assessments", action='store_true')
            args.add_argument("--top-ten", "-tt", help="Scan top ten most common TCP ports.", action='store_true')
            args.add_argument("--no_random", "-r", help="Port range will not be randomised", action='store_true')
            args.add_argument("--procs", "-z", help="Number of processes to spawn, 1-999, default 256", type=int)

            parsed = args.parse_args()

            self.target = parsed.target
            if "/" in self.target:
                if parsed.ip:
                    self.ip_splitting = parsed.ip
                    log_target = str(self.target).replace("/", "_")
                    self.logfile = os.getcwd() + "/deeper_" + log_target + "_" + self.timestamp + ".log"
                else:
                    if not self.check_for_network_address():
                        self.target = self.target.split("/", 1)[0]
                        log_target = self.target
                        self.logfile = os.getcwd() + "/deeper_" + log_target + "_" + self.timestamp + ".log"
            else:
                if not self.check_for_network_address():
                    log_target = self.target
                    self.logfile = os.getcwd() + "/deeper_" + log_target + "_" + self.timestamp + ".log"

            self.no_random = parsed.no_random
            if parsed.procs:
                if parsed.procs > 0 and parsed.procs < 1000:
                    self.procs = parsed.procs
                else:
                    print("Processes must be less than 1000 due to OS limitations.")
                    exit(1)
            else:
                self.procs = 256

            if parsed.time:
                self.command = "nmap -Pn -v -T" + str(parsed.time) + " "
            else:
                self.command = "nmap -T2 -Pn -v "

            if parsed.ver:
                self.command = self.command + "-sCV --version-all "

            if not parsed.udp and not parsed.tcp:
                self.scan_type = "-sS"

            if parsed.tcp:
                if not parsed.udp:
                    self.scan_type = "-sT"
                else:
                    print("TCP and UDP scans are mutually exclusive. Please select only one.")
                    exit(1)

            if parsed.udp:
                if not parsed.tcp:
                    self.scan_type = "-sU"
                else:
                    print("TCP and UDP scans are mutually exclusive. Please select only one.")
                    exit(1)

            if parsed.ports:
                if len(parsed.ports) > 200:
                    print("\nPlease specify a range of ports. example: \"1-1024\"")
                    exit(1)
                elif "," in parsed.ports:
                    self.port_list = [parsed.ports.split(",")]
                elif "-" not in parsed.ports:
                    self.port = str(parsed.ports)
                else:
                    pmin, pmax = parsed.ports.split("-")
                    self.min = pmin
                    self.max = pmax
                    self.ports = True

            elif not parsed.ports:
                if parsed.internal:
                    self.internal_assessment = True
                if parsed.udp:
                    self.top_udp = True
                if parsed.top_ten:
                    self.top_ten = True
                else:
                    self.top_tcp = True

        except Exception as e:
            self.exceptor.catchit("get_args", e)
