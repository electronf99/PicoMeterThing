#!/usr/bin/python3
import threading
import time
import random


class SharedState:
    def __init__(self):
        self.rx_speed = 0


def worker(state, increment):
    current_value = 0

    while True:
        print(f"[Worker] Counter: {state.rx_speed}")

        if current_value != state.rx_speed:
            if current_value - state.rx_speed < increment:
                current_value += increment
            if current_value < state.rx_speed:
                current_value += 1

            elif current_value - state.rx_speed > increment:
                current_value -= increment
                if current_value > state.rx_speed:
                    current_value -= 1

        print(f"CV {'-' * current_value}")
        print(f"RX {'-' * state.rx_speed}")
        time.sleep(0.2)


if __name__ == "__main__":
    state = SharedState()

    increment = 2

    t = threading.Thread(target=worker, args=(state, increment))
    t.start()

    while t.is_alive():
        print(f"[Main]{'-' * state.rx_speed}")
        state.rx_speed = int(random.random() * 100)
        time.sleep(2)
