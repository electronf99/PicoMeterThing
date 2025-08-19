import bluetooth


class BLEPacketReceiver:
    def __init__(self, ble):
        self.ble = ble
        self.ble.active(True)
        self.ble.irq(self._irq)

        self.data_buffer = b""
        self.expected_packets = None
        self.received_packets = 0

        self._setup_services()

    def _setup_services(self):
        UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
        UART_SERVICE = (UART_UUID, (TX_UUID,))
        services = (UART_SERVICE,)

        ((self.tx_handle,),) = self.ble.gatts_register_services(services)
        self.ble.gatts_write(self.tx_handle, b"")
        self.ble.gap_advertise(100, b"\x02\x01\x06\x03\x03\x9e\xca")
        print("BLE advertising...")

    def _irq(self, event, data):
        if event == bluetooth._IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            value = self.ble.gatts_read(attr_handle)
            self._on_rx(value)

    def _on_rx(self, data):
        packet_index = data[0]
        total_packets = data[1]
        payload = data[2:]

        if self.expected_packets is None:
            self.expected_packets = total_packets

        self.data_buffer += payload
        self.received_packets += 1

        print(f"Received packet {packet_index + 1}/{total_packets}")

        if self.received_packets == self.expected_packets:
            print("All packets received!")
            print("Reassembled data:", self.data_buffer.decode())

            # Reset for next transmission
            self.data_buffer = b""
            self.expected_packets = None
            self.received_packets = 0


# Instantiate and run
ble = bluetooth.BLE()
receiver = BLEPacketReceiver(ble)
