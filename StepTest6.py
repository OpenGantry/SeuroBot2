"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

NotDone = True
myRange=200/2
delay=1.0/myRange
tests=20
delay=.05
for n in range(tests):
    print("Test: ",n)
    delay+=.01
    print(*"delay = ", delay)
    delay(1)
    for i in range(myRange):
        print("i: ",i)
        time.sleep(delay)
        kit.stepper2.release()
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)

