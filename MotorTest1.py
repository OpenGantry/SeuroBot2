"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

NotDone = True
myRange=200
delay=5



kit.motor4.throttle = 0.5
time.sleep(delay)
kit.motor1.throttle = 0.0
