# Import necessary modules
from machine import PWM
import machine
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from lcd1602 import LCD1602

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

def decode(data):
    i = 0

    def read():
        nonlocal i
        val = data[i]
        i += 1
        return val

    def read_bytes(n):
        nonlocal i
        val = data[i:i+n]
        i += n
        return val

    def unpack():
        prefix = read()

        # FixInt (positive)
        if prefix <= 0x7f:
            return prefix

        # FixMap
        elif 0x80 <= prefix <= 0x8f:
            size = prefix & 0x0f
            obj = {}
            for _ in range(size):
                key = unpack()
                val = unpack()
                obj[key] = val
            return obj

        # FixArray
        elif 0x90 <= prefix <= 0x9f:
            size = prefix & 0x0f
            return [unpack() for _ in range(size)]

        # FixStr
        elif 0xa0 <= prefix <= 0xbf:
            size = prefix & 0x1f
            return read_bytes(size).decode()

        # uint8
        elif prefix == 0xcc:
            return read()

        # uint16
        elif prefix == 0xcd:
            return int.from_bytes(read_bytes(2), 'big')

        # uint32
        elif prefix == 0xce:
            return int.from_bytes(read_bytes(4), 'big')

        # str8
        elif prefix == 0xd9:
            size = read()
            return read_bytes(size).decode()

        else:
            raise ValueError("Unsupported prefix: {}".format(hex(prefix)))

    return unpack()



def update_traffic(data):

    LCDLine0 = data['LCD']['0']['txt']
    moving_iron_volts = data["meter"]["m1"]["val"]
    lcd.write_text(0,0,LCDLine0)
    volt_meter.duty_u16(int(moving_iron_volts))

# Define a callback function to handle received data
def on_rx(data):

    global rx_packets
    
    seq, total_packets, msg_id = data[0], data[1], data[2]
    if(seq==0):
        rx_packets = []
    
    payload = data[3:].rstrip(b"\x00")
    rx_packets.append(payload)
    
    if( total_packets == seq + 1):
        print(total_packets)
        full_payload = b""
        for packet in rx_packets:
            full_payload = full_payload + packet
                    
        message = decode(full_payload)
        print(message)
        update_traffic(message)


if __name__ == "__main__":
    
    sp = BLESimplePeripheral(ble, "pico2w")
   
    # Start an infinite loop
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception
