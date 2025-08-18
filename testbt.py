# Import necessary modules
from machine import Pin, PWM
import machine
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from lcd1602 import LCD1602
import json
import binascii

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble,"pico2w")
lcd = LCD1602.begin_4bit(rs=16, e=17, db_7_to_4=[21, 20, 19, 18])

# Set up PWM Pin
volt_pin = machine.Pin(0)
volt_meter = PWM(volt_pin)

#Set PWM frequency
frequency = 5000
volt_meter.freq (frequency)

def update_traffic(data):

    decoded_data = binascii.a2b_base64(data.decode('utf-8').rstrip('\r\n'))
    print(f"{data} {decoded_data}")

    data = json.loads(decoded_data)
    duty_cycle = (data['l'] / 1000) * 32767 +32767
    lcd.write_text(0,1,str(data['l']) + " " + str(duty_cycle))
    volt_meter.duty_u16(int(duty_cycle))



# Define a callback function to handle received data
def on_rx(data):
    
    update_traffic(data)

# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  # Set the callback function for data reception