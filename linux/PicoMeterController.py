#!/usr/bin/python3

import asyncio
from time import sleep
from bleak import BleakClient
import json
from base64 import b64encode
import math

async def main():

    ble_address = "2C:CF:67:E4:D5:10"
    characteristic_uuid = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

    
    data = {'l' : 0 }
    j = json.dumps(data)
    data_bytes = j.encode('utf-8')

    async with BleakClient(ble_address) as client:
        
        # data = await client.read_gatt_char(characteristic_uuid)
        # data[0] = 1
        a=0
        while(1==1):
            
            for i in range(0,180, 1):
                sin = math.sin(math.radians(i))
                v = int(sin*1000)
                a += 1
                data['l'] = v
                j = json.dumps(data)
                
                data_bytes = b64encode(j.encode('utf-8'))
                print(f"{j} {data_bytes}")
                await client.write_gatt_char(characteristic_uuid, data_bytes)
            
                sleep(0.1)

asyncio.run(main())


