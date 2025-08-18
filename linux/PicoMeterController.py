#!/usr/bin/python3

import asyncio
from time import sleep
from bleak import BleakClient
import json
from base64 import b64encode
import math
from ble20Packets import ble20Packets

async def main():

    ble_address = "2C:CF:67:E4:D5:10"
    characteristic_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

    # Packet list handler
    packer = ble20Packets(message_id=1, max_payload=17)
    
    transmission = {
        "LCD": {
                "Line1": {"text": "This is a test", "startcol": 0},
                "Line2": {"text": 1, "startcol": 0},
            },
            "baseVoltage": 19.5,
            "meters": {
                "MovingIron": {
                    "duty_min": 32768,
                    "duty_max": 65535,
                    "value": 3,
                    "fullscale": 19,
                },
                "20VPlastic": {
                    "duty_min": 32768,
                    "duty_max": 65535,
                    "value": 3,
                    "fullscale": 19,
                },
            },
        }
    packets = packer.build_packets(transmission)

 
    async with BleakClient(ble_address) as client:
        
        # data = await client.read_gatt_char(characteristic_uuid)
        # data[0] = 1
        a=0
        while(1==1):
            

            for packet in packets:
                print(packet)

                await client.write_gatt_char(characteristic_uuid, packet)
        
            sleep(0.1)

asyncio.run(main())


