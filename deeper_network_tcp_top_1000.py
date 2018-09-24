#!/usr/bin/env python3

import argparse
import os
import sys
import time
import subprocess
import datetime
from concurrent import futures


class Deeper:

    def __init__(self):
        try:
            self.top_udp = False
            self.top_tcp = True
            self.port_range = False
            self.command = "nmap -T2 -Pn -v "
            self.network = ""
            self.scan_type = "-sS"
            self.min = ""
            self.max = ""
            self.num_ports: int = 0
            self.procs: int = 0
            self.timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            self.logfile = os.getcwd() + "/deeper_" + self.timestamp + ".log"
        except Exception as e:
            print("Error! in __init__: " + str(e))

    def clear_files(self):
        try:
            with open(self.logfile, "w") as file:
                file.write("")
            os.system("reset")
        except Exception as e:
            print("Error! in clear_files: " + str(e))

    def get_args(self) -> argparse:
        try:
            args = argparse.ArgumentParser()
            args.add_argument("network", help="/24 Network to scan")
            args.add_argument("--procs", "-z", help="Number of processes to spawn", type=int)
            parsed = args.parse_args()
            self.network = parsed.network

            if parsed.procs:
                if parsed.procs > 0 and parsed.procs < 1000:
                    self.procs = parsed.procs
                else:
                    print("Processes must be less than 1000 due to OS limitations.")
                    exit(1)
            else:
                self.procs = 500
        except Exception as e:
            print("Error! in get_args: " + str(e))

    def get_top_ports_list(self, protocol):
        try:
            if "tcp" in protocol:
                path = os.getcwd() + "/tcp_ports_1000.txt"
            elif "udp" in protocol:
                path = os.getcwd() + "/udp_ports_1000.txt"
            else:
                raise Exception
            with open(path, "r") as file:
                ports = file.readlines()
                ports = [b.rstrip() for b in str(ports).split(",")]
            return ports
        except Exception as e:
            print("Error in get_top_ports_list: " + str(e))

    def get_ports(self):
        try:
            ports = self.get_top_ports_list("tcp")
            return ports
        except Exception as e:
            print("Error! in get_ports: " + str(e))

    def command_runner(self, port):
        try:
            cmd = (self.command + self.network + " " + self.scan_type + " -p " + port + " >> " + self.logfile)
            print(cmd)
            subprocess.run(cmd, shell=True)
        except Exception as e:
            print("Error in command_runner: " + str(e))

    def controller(self, ports):
        try:
            with futures.ProcessPoolExecutor(self.procs) as pool:
                pool.map(self.command_runner, ports)
        except Exception as e:
            print("Error! in controller: " + str(e))

    def write_results(self, results):
        with open(self.logfile, "a") as file:
            file.write("\n*************************************************\n")
            file.writelines(results)

    def display_results(self):
        try:
            t1 = time.perf_counter()
            with open(self.logfile, "r") as file:
                logs = file.readlines()
                ports = [l for l in logs if "tcp" in l or "udp" in l]
                [print(p.rstrip("\n")) for p in ports]
                closed = [p for p in ports if "closed" in p]
                filter = [p for p in ports if "filter" in p]
                open_ports = [p for p in ports if "Discovered open" in p
                              and not "closed" in p and not "filter" in p]
                total = len(ports)
                num_cl = len(closed)
                num_fl = len(filter)
                num_op = len(open_ports)
                total = total - num_op
                print("\n******************************************************\n"
                      "Total Ports Scanned: " + str(total))
                print("Closed: " + str(num_cl))
                print("Filtered: " + str(num_fl))
                print("Open: " + str(num_op))
                if num_op > 0:
                    print("\n********* Open Ports *********")
                    [print(o.rstrip()) for o in open_ports]
                    print("*********************************")
                else:
                    print("\nNo ports discovered open. :(")
            t2 = time.perf_counter()
            print("\nTime to calculate and display results: " + str(round(t2-t1, 4)) + "sec\n")
        except Exception as e:
            print("Error! in display_results: " + str(e))


def check_python_version():
    try:
        x, y, z, a, b = sys.version_info
        ver = str(x) + str(y)
        if int(ver) < 36:
            print("\nThis application requires Python 3.6 or greater.\nhttps://www.python.org/downloads/\n")
            exit(0)
    except Exception as e:
        print("Error! in check_python_version: " + str(e))


if __name__ == '__main__':
    try:
        check_python_version()
        t1 = time.perf_counter()
        new_Nmap = Deeper()
        new_Nmap.clear_files()
        new_Nmap.get_args()
        print("\nWARNING! This program intentionally utalises system resources for performance.\n"
              "Your system may become temporarily unresponsive.\nProcessing..")

        ports = new_Nmap.get_ports()
        new_Nmap.controller(ports)
        new_Nmap.display_results()

        t2 = time.perf_counter()
        print("\nTotal Execution Time: " + str(round(t2 - t1, 4)) + "sec\n")
        time.sleep(1)
        os.system("stty sane")
    except Exception as e:
        print("Error! in main(): " + str(e))
