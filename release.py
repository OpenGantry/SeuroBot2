"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

kit.stepper1.relsase()
kit.stepper2.relsase()
