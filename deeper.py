#!/usr/bin/env python3

import argparse
import asyncio
import os
import sys


class Deeper:

    def __init__(self):
        try:
            self.loop = asyncio.get_event_loop()
            self.command, self.port_range = self.get_args()
            self.min, self.max = self.port_range.split("-")
            self.logfile = os.getcwd() + "/deeper.log"
        except Exception as e:
            print("Error! in __init__: " + str(e))


    def clear_files(self):
        try:
            with open(self.logfile, "w") as file:
                file.write("")
        except Exception as e:
            print("Error! in clear_files: " + str(e))


    def get_args(self) -> argparse:
        try:
            os.system("reset")
            args = argparse.ArgumentParser()
            args.add_argument("nmap_command", help="nmap command with no ports specified. "
                                                   "\"Must be enclosed in quotes\"", type=str)
            args.add_argument("port_range", help="port range eg. \"80-443\"", type=str)
            parsed = args.parse_args()
            if not "-" in parsed.port_range:
                print("\nPlease specify a range of ports. \"1-1024\"")
                exit(1)
            if len(parsed.nmap_command) < 79 and len(parsed.port_range) < 12:
                return parsed.nmap_command, parsed.port_range
            else:
                print("\nTry Harder..\n")
                exit(1)
        except Exception as e:
            print("Error! in get_args: " + str(e))


    async def get_ports(self):
        try:
            ports = (str(i) for i in range(int(self.min), int(self.max)+1))
            return ports
        except Exception as e:
            print("Error! in get_ports: " + str(e))


    async def command_runner(self, port):
        try:
            cmd = (self.command + " -p " + port + " >> " + self.logfile)
            await asyncio.create_subprocess_shell(cmd=cmd, stdout=asyncio.subprocess.PIPE, loop=self.loop)
        except Exception as e:
            print("Error in command_runner: " + str(e))

    async def controller(self):
        try:
            ports = await self.get_ports()
            [await self.command_runner(p) for p in ports]
        except Exception as e:
            print("Error! in controller: " + str(e))


    def display_results(self):
        try:
            import time
            t1 = time.perf_counter()
            with open(self.logfile, "r") as file:
                logs = file.readlines()
                ports = [l for l in logs if "tcp" in l or "udp" in l
                         or "closed" in l or "filtered" in l or "open" in l]
                [print(p.rstrip("\n")) for p in sorted(ports)]
                closed = [p for p in ports if "closed" in p]
                filter = [p for p in ports if "filter" in p]
                open_ports = [p for p in ports if "open" in p and not "closed" in p and not "filter" in p]
                total = sum([1 for l in logs if "PORT" in l and "STATE" in l and "SERVICE" in l])
                num_cl = len(closed)
                num_fl = len(filter)
                num_op = len(open_ports)
                print("\n******************************************************")
                print("Command: \"" + self.command + " -p " + str(self.port_range) + "\"")
                print("******************************************************\n"
                      "Total Ports Scanned: " + str(total))
                print("Closed: " + str(num_cl))
                print("Filtered: " + str(num_fl))
                print("Open: " + str(num_op))
                if num_op > 0:
                    print("\n********* Open Ports from *********")
                    [print(o.rstrip()) for o in open_ports]
                    print("***********************************")
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
        import time
        check_python_version()
        t1 = time.perf_counter()
        new_Nmap = Deeper()
        new_Nmap.clear_files()
        print("\nWARNING! This program intentionally utalises maximum system resources for performance.\n"
              "Your system may become unresponsive.")
        loopy = asyncio.get_event_loop()
        loopy.run_until_complete(new_Nmap.loop.create_task(new_Nmap.controller()))
        t2 = time.perf_counter()
        print("\nTotal Execution Time: " + str(round(t2-t1, 4)) + "sec\n")
        print("Calculating results..")
        new_Nmap.display_results()
        time.sleep(0.5)
        os.system("stty sane")

    except Exception as e:
        print("Error! in display_results: " + str(e))

