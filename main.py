# Import necessary modules
from machine import PWM, I2C, Pin
import machine
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
from lcd1602 import LCD1602

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
lcd = LCD1602.begin_4bit(rs=16, e=17, db_7_to_4=[21, 20, 19, 18])

# Turn backlight down
backlight_pin = machine.PWM(machine.Pin(28))
backlight_pin.freq(1000)
backlight_pin.duty_u16(16000)

# Set PWM frequency
frequency = 5000


# Set up PWM Pin
m1_volt_pin = machine.Pin(22)
m1_volt_meter = PWM(m1_volt_pin)
m1_volt_meter.freq(frequency)

m2_volt_pin = machine.Pin(15)
m2_volt_meter = PWM(m2_volt_pin)
m2_volt_meter.freq(frequency)



rx_packets = []

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

    LCDLine0 = data['LCD']['0']
    LCDLine1 = data['LCD']['1']
  
    #moving_iron_volts = data["meter"]["m1"]["v"]
    moving_iron_volts = min(62000, data["meter"]["m1"]["v"])
    m1_volt_meter.duty_u16(int(moving_iron_volts))
    m2_volts = data["meter"]["m2"]["v"]
    m2_volt_meter.duty_u16(int(m2_volts))


    lcd.write_text(0,0,LCDLine0)
    lcd.write_text(0,1,LCDLine1)
    

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
    
    print(">>------------")
    sp = BLESimplePeripheral(ble, "pico2w")
    print("------------<<")
   
    # Start an infinite loop
    while True:
        if sp.is_connected():  # Check if a BLE connection is established
            sp.on_write(on_rx)  # Set the callback function for data reception
        else:
            m1_volt_meter.duty_u16(int(32768))