import json
import zlib


class ble20Packets:
    def __init__(self, message_id=1, max_payload=17):
        self.message_id = message_id
        self.max_payload = max_payload

    def build_packets(self, json_str):
        json_str = json.dumps(json_str, separators=(",", ":"))

        compressed = zlib.compress(json_str.encode("utf-8"))
        chunk_size = self.max_payload
        chunks = [compressed[i : i + chunk_size] for i in range(0, len(compressed), chunk_size)]
        total_packets = len(chunks)
        msg_id = self.message_id

        packets = []
        for seq, chunk in enumerate(chunks):
            header = bytes([seq, total_packets, msg_id])
            packet = header + chunk.ljust(self.max_payload, b"\x00")  # pad to full size
            packets.append(packet)

        return packets

    def decode_packets(self, received_packets):
        buffer = {}
        for packet in received_packets:
            seq, total_packets, msg_id = packet[0], packet[1], packet[2]
            payload = packet[3:].rstrip(b"\x00")
            buffer[seq] = payload

        if len(buffer) != total_packets:
            print("Still missing packets after retry.")
        else:
            full_data = b"".join(buffer[i] for i in range(total_packets))
            decompressed = zlib.decompress(full_data).decode("utf-8")
            reconstructed = json.loads(decompressed)

            return msg_id, reconstructed
