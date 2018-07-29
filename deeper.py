#!/bin/python3

import argparse
import os
import asyncio


class NmapSpeedTest:

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.ip, self.min, self.max = self.get_args()
        self.logfile = os.getcwd() + "/nmap_speed_test.log"
        self.pids = []
        self.apd = self.pids.append

    def clear_files(self):
        with open(self.logfile, "w") as file:
            file.write("")

    def get_args(self) -> argparse:
        try:
            os.system("reset")
            args = argparse.ArgumentParser()
            args.add_argument("ip", help="address to scan.", type=str)
            args.add_argument("--min", help="port start", type=int, default=1)
            args.add_argument("--max", help="port end", type=int, default=655)
            parsed = args.parse_args()
            return parsed.ip, parsed.min, parsed.max
        except Exception as e:
            print("Error! in cliargs: " + str(e))

    async def get_ports(self):
        ports = (str(i) for i in range(self.min, self.max+1))
        return ports

    async def command_runner(self, port):
        try:
            cmd = ("nmap -T3 -sS -Pn " + self.ip + " -p " + port + " >> " + self.logfile)
            await asyncio.create_subprocess_shell(cmd=cmd, stdout=asyncio.subprocess.PIPE, loop=self.loop)
        except Exception as e:
            print("Error in runner: " + str(e))

    async def controller(self):
        ports = await self.get_ports()
        [await self.command_runner(p) for p in ports]

    def display_results(self):
        with open(self.logfile, "r") as file:
            ports = [l for l in file.readlines() if "tcp" in l or "udp" in l
                     or "closed" in l or "filtered" in l or "open" in l]
            [print(p) for p in ports]
            closed = [p for p in ports if "closed" in p]
            filter = [p for p in ports if "filter" in p]
            open_ports = [p for p in ports if "open" in p and not "closed" in p and not "filter" in p]
            num_cl = len(closed)
            num_fl = len(filter)
            num_op = len(open_ports)
            print("\n*******************")
            print("HOST: " + self.ip)
            print("*******************\nTotal Ports Scanned: " + str((num_cl + num_fl + num_op)))
            print("Closed: " + str(num_cl))
            print("Filtered: " + str(num_fl))
            print("Open: " + str(num_op))
            print("\n***** Open Ports on " + self.ip + " *****")
            [print(o.rstrip()) for o in open_ports]
            print("***********************************")
        os.system("stty sane")


if __name__ == '__main__':
    new_Nmap = NmapSpeedTest()
    new_Nmap.clear_files()
    print("\nProcessing... hold onto your ass.")
    loopy = asyncio.get_event_loop()
    loopy.run_until_complete(new_Nmap.loop.create_task(new_Nmap.controller()))
    import time
    time.sleep(2)
    new_Nmap.display_results()
    os.system("stty sane")
