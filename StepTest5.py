"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

NotDone = True
myRange=400
delay=3

myDirection=stepper.FORWARD
myStyle=stepper.SINGLE

for i in range(myRange):
    kit.stepper2.onestep(myDirection, myStyle)

