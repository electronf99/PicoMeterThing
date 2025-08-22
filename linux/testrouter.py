#!/usr/bin/python3

from RouterInfo import RouterInfo
import threading
import json
import time             


rx = 0

def get_rinfo(ri):
    
    global rx
    
    while True:
        traffic = json.loads(ri.get_traffic())

        print(traffic['speed']['rx'])
        duty_cycle = int((traffic['speed']['rx'] / 120) * 32768 + 32768)


        if duty_cycle > 65535:
            duty_cycle = 65535

        print(duty_cycle)
        rx = duty_cycle


ri = RouterInfo("192.168.0.1", "admin", "electronf11")

thread = threading.Thread(target=get_rinfo,args=(ri,))
thread.start()

while True:
    time.sleep(1)
    print(f"----> {rx}")