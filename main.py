# Import necessary modules
from machine import PWM, Pin, I2C
import machine
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from pico_i2c_lcd import I2cLcd
from time import sleep
from msgpack_decoder import decode
from custom_char import get_arrow_chars

# Define the LCD I2C address and dimensions
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD objects
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=1000000)
i2clcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


i2clcd.clear()
i2clcd.putstr("BT Listening..")



# Set PWM frequency
frequency = 5000

# Set up PWM Pin
m1_volt_pin = machine.Pin(22)
m1_volt_meter = PWM(m1_volt_pin)
m1_volt_meter.freq(frequency)

m2_volt_pin = machine.Pin(15)
m2_volt_meter = PWM(m2_volt_pin)
m2_volt_meter.freq(frequency)

displayed = 0

spinner = ['-', '\\', '|', '/']
spincount = 0

rx_packets = []

custom = get_arrow_chars()

a=0
for custom_char in custom:
    i2clcd.custom_char(a,custom_char)
    a += 1

def pprint(obj, indent=0):
    spacing = '  ' * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            print(f"{spacing}{k}:")
            pprint(v, indent + 1)
    elif isinstance(obj, list):
        for item in obj:
            pprint(item, indent + 1)
    else:
        print(f"{spacing}{obj}")


def update_traffic(data):

    global spincount
   
    try:
        LCDLine0 = data['LCD']['0'][:16]
        LCDLine1 = data['LCD']['1'][:16]
    
        #moving_iron_volts = data["meter"]["m1"]["v"]
        moving_iron_volts = min(62000, data["meter"]["m1"]["v"])
        m1_volt_meter.duty_u16(int(moving_iron_volts))
        m2_volts = data["meter"]["m2"]["v"]
        if m2_volts > 0:
            m2_volt_meter.duty_u16(int(m2_volts))
    except Exception as e:
        print(e)

    i2clcd.move_to(0,0)
    i2clcd.putstr(LCDLine0)
    i2clcd.move_to(0,1)
    i2clcd.putstr(LCDLine1)
    
    i2clcd.move_to(15,1)
    i2clcd.putstr(chr(spincount))
    spincount += 1
    if spincount == 8:
        spincount = 0

    

# Define a callback function to handle received data
def on_rx(data):

    global rx_packets
    
    seq, total_packets, msg_id = data[0], data[1], data[2]
    if(seq==0):
        rx_packets = []
    
    payload = data[3:].rstrip(b"\x00")
    rx_packets.append(payload)
    
    if( total_packets == seq + 1):
        full_payload = b""
        for packet in rx_packets:
            full_payload = full_payload + packet

                   
        message = decode(full_payload)
        print(total_packets, message)

        update_traffic(message)


if __name__ == "__main__":
    
    # Create a Bluetooth Low Energy (BLE) object
    ble = bluetooth.BLE()
    print(">>------------")
    sp = BLESimplePeripheral(ble, "pico2w")
    print("------------<<")
   
    # Start an infinite loop
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception
            sleep(1)
        else:
            m1_volt_meter.duty_u16(int(32768))