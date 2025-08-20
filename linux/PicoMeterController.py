#!/usr/bin/python3

import asyncio
from time import sleep
from bleak import BleakClient
import json
from base64 import b64encode
import math
from ble20Packets import ble20Packets
import msgpack


async def main():

    ble_address = "2C:CF:67:E4:D5:10"
    characteristic_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

    # Packet list handler
    packer = ble20Packets(message_id=1, max_payload=17)
    
    transmission = {
        "LCD": {
                "0": {"txt": "This is a test"},
 #               "Line2": {"text": 1, "startcol": 0},
            },
 #       "baseVoltage": 19.5,
        "meter": {
            "m1": {
 #               "duty_min": 32768,
 #               "duty_max": 65535,
                "v": 3,
 #               "fullscale": 19,
                },
            "m2": {
            #     "duty_min": 32768,
            #     "duty_max": 65535,
                "v": 3,
            #     "fullscale": 19,
                },
            },
        }
    

 
    async with BleakClient(ble_address) as client:
        
        # data = await client.read_gatt_char(characteristic_uuid)
        # data[0] = 1
        a=0
        level = float(1)
        while(1==1):

            for i in range(0,180, 2):
                sin = math.sin(math.radians(i))
                v = (sin+1)

                duty_cycle = int(float(v) * (65536/2)*level)

                transmission["LCD"]["0"]["txt"] = str(duty_cycle)
                transmission["meter"]["m1"]["val"] = str(duty_cycle)
                mpack = msgpack.packb(transmission)
                packets = packer.build_packets(mpack)
                                
                for packet in packets:
                    print(packet)
                    await client.write_gatt_char(characteristic_uuid, packet)
            
                #sleep(0.01)

asyncio.run(main())


