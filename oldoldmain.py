from Makerverse_Motor_2ch import motor
import time

m1 = motor(pwmPin = 0, dirPin = 1)

while( 1 == 1) :
    v = int(input("Percent: "))
    m1.speed(v)
    

m1.stop()