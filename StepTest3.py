"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

for i in range(200):
    #time.sleep(0.1)
    print(i)
    kit.stepper2.onestep()
