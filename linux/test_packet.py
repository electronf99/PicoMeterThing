#!/usr/bin/python3
from ble20Packets import ble20Packets

msg_id = 1
transmission = {
    "LCD": {
        "Line1": {"text": "This is a test", "startcol": 0},
        "Line2": {"text": msg_id, "startcol": 0},
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

packer = ble20Packets(message_id=1, max_payload=17)
packets = packer.build_packets(transmission)

for packet in packets:
    print(packet)

msg_id, data = packer.decode_packets(packets)

print(f"Message {msg_id}:")
print(data)
