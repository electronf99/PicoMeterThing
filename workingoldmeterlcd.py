# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-pwm-micropython/
from machine import Pin, PWM
import machine
from time import sleep
import math
import _thread

from machine import Pin
from time import sleep
from lcd1602 import LCD1602

from bluetooth import BLE
import ubluetooth


STOP = False
LEVEL = 1
VAL = 1.0

def signal_out():
    # Set up PWM Pin
    volt_pin = machine.Pin(0)
    volt_meter = PWM(volt_pin)

    lcd = LCD1602.begin_4bit(rs=16, e=17, db_7_to_4=[21, 20, 19, 18])
    #lcd.write_text(0, 1, "Hello Mitchell!")

    #Set PWM frequency
    frequency = 5000
    volt_meter.freq (frequency)

    try:

        
        while True:
            
            level = float(LEVEL)
            
            for i in range(0,180, 1):
                sin = math.sin(math.radians(i))
                v = (sin+1)

                duty_cycle = int(float(v) * (65536/2)*level)
                VAL=duty_cycle
                volt_meter.duty_u16(duty_cycle)
                print(v, duty_cycle)
                lcd.write_text(0, 1, "Duty Cycle: " + str(duty_cycle))
                sleep(0.1)
                if(STOP == True):
                    print("Stopping")
                    volt_meter.duty_u16(32768)
                    sleep(10)
                    #volt_meter.deinit()
                    return
                
    except KeyboardInterrupt:
        print("Keyboard interrupt")
        volt_meter.duty_u16(32768)
        # print(volt_meter)
        #volt_meter.deinit()

#main()

if __name__ == "__main__":

    




    _thread.start_new_thread(signal_out,())
    try:
        while 1 == 1:
                #i = float(input("Test: "))
                # LEVEL=i
                #LEVEL = (math.sin(math.radians(i)) + 1)/2
                print(VAL)
                sleep(0.5)

                
          
    except:
        STOP= True
        sleep(2)
        print("Stopped")
