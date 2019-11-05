"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

NotDone = True
myRange=200
delay=1.0/myRange
n=8
delay=.05

for i in range(myRange):
    print("i: ",i)
   # time.sleep(delay)
    kit.stepper1.release()
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)

