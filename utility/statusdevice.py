import psutil
import os

def get_uptime():
    uptime = dict(psutil.cpu_times(percpu=False)._asdict())
    print("Uptime: {} seconds ".format(uptime['idle']))
    return uptime['idle']

def get_cpu_percent():
    cpupercent = 0
    cpupercent = psutil.cpu_percent(interval=3, percpu=False)
    print("CPU Usage: {}%".format(cpupercent))
    return cpupercent

def get_avg_cpu_load():
    avgload = [x / psutil.cpu_count() * 100 for x in os.getloadavg()]
    print("Average CPU usage: {}% ".format(avgload))
    return avgload

def get_ram_usage():
    ramload = dict(psutil.virtual_memory()._asdict())
    print("RAM Usage: {}%".format(ramload['percent']))
    return ramload['percent']
