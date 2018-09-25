#!/usr/bin/env python3

import argparse
import os
import sys
import time
import subprocess
import datetime
from concurrent import futures


class Doppler:

    def __init__(self):
        try:
            self.port = ""
            self.command = ""
            self.network = ""
            self.scan_type = "-sS"
            self.num_ports: int = 0
            self.procs: int = 0
            self.timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            self.logfile = os.getcwd() + "/deeper_network_top_ten_" + self.timestamp + ".log"
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
            args.add_argument("network", help="/24 Network Target of scan.", type=str)
            args.add_argument("--procs", "-z", help="Number of processes to spawn Default:500", type=int)
            parsed = args.parse_args()
            self.network = parsed.network
            self.command = "nmap -T2 -Pn -v "
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

    def get_ip_list(self):
        try:
            net = self.network
            a,b,c,d = net.split(".")
            seq = [i for i in range(1, 255)]
            first = a + "." + b + "." + c + "."
            ip_list = [first+str(s) for s in seq]
            return ip_list
        except Exception as e:
            print("Error in get_ip_list: " + str(e) +
            "\nPlease Enter IP address of network in the format 10.10.10.0\n")

    def command_runner(self, ip):
        try:
            cmd = (self.command + ip + " " + self.scan_type + " -p " + self.port + " >> " + self.logfile)
            print(str(cmd))
            subprocess.run(cmd, shell=True)
        except Exception as e:
            print("Error in command_runner: " + str(e))

    def controller(self, ips):
        try:
            with futures.ProcessPoolExecutor(self.procs) as pool:
                pool.map(self.command_runner, ips)
        except Exception as e:
            print("Error! in controller: " + str(e))

    def write_results(self, results):
        with open(self.logfile, "a") as file:
            file.write("\n*************************************************\n")
            file.writelines(results)

    def get_ports(self):
        with open(os.getcwd() + "/top_ten_tcp.txt", "r") as file:
            ports = file.readlines()
            ports = [p.rstrip("\n") for p in ports]
            return ports

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
                    new_Nmap.write_results(open_ports)
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
        new_Nmap = Doppler()
        new_Nmap.clear_files()
        new_Nmap.get_args()
        print("\nWARNING! This program intentionally utalises system resources for performance.\n"
              "Your system may become temporarily unresponsive.\nProcessing..")
        ports = new_Nmap.get_ports()
        ips = new_Nmap.get_ip_list()
        for p in ports:
            new_Nmap.port = str(p)
            new_Nmap.controller(ips)
        new_Nmap.display_results()
        t2 = time.perf_counter()
        print("\nTotal Execution Time: " + str(round(t2 - t1, 4)) + "sec\n")
        time.sleep(1)
        os.system("stty sane")
    except Exception as e:
        print("Error! in main(): " + str(e))
