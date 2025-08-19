# Import necessary modules
from machine import PWM
import machine
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from lcd1602 import LCD1602
from ble20PacketsMpy import ble20Packets
import json

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
lcd = LCD1602.begin_4bit(rs=16, e=17, db_7_to_4=[21, 20, 19, 18])

# Set up PWM Pin
volt_pin = machine.Pin(0)
volt_meter = PWM(volt_pin)

# Set PWM frequency
frequency = 5000
volt_meter.freq(frequency)

rx_packets = []

def update_traffic(data):

    LCDLine1 = data['LCD']['Line1']['text']
    print(LCDLine1)
    lcd.write_text(0,1,LCDLine1)


    # data = json.loads(decoded_data)
    # duty_cycle = (data['l'] / 1000) * 32767 +32767
    # lcd.write_text(0,1,str(data['l']) + " " + str(duty_cycle))
    # volt_meter.duty_u16(int(duty_cycle))

# Define a callback function to handle received data
def on_rx(data):

    global rx_packets
    
    seq, total_packets, msg_id = data[0], data[1], data[2]
    if(seq==0):
        rx_packets = []
    
    payload = data[3:].rstrip(b"\x00")
    rx_packets.append(payload)
    
    if( total_packets == seq + 1):
        full_payload = ""
        for packet in rx_packets:
            full_payload = full_payload + packet.decode("utf-8")
        
        message = json.loads(full_payload)
        print(message)


        update_traffic(message)


if __name__ == "__main__":
    sp = BLESimplePeripheral(ble, "pico2w")

    # Start an infinite loop
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception
