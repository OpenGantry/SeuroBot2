"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

NotDone = True
myRange=200
delay=3


for i in range(myRange):
    kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)

