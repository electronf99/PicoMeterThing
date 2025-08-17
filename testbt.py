
from bluetooth import BLE
import ubluetooth
import time

ble = BLE()
ble.active(True)

# Define a simple BLE UART service (Nordic UART Service)
UART_UUID = ubluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
TX_UUID = ubluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
RX_UUID = ubluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")

UART_SERVICE = (
    UART_UUID,
    (
        (TX_UUID, ubluetooth.FLAG_NOTIFY,),
        (RX_UUID, ubluetooth.FLAG_WRITE,),
    ),
)

ble.config(gap_name="PicoBLE")
ble.gatts_register_services((UART_SERVICE,))
ble.gap_advertise(100, b'\x02\x01\x06\x03\x03\x9e\xfe')


while True:
    time.sleep(1)

