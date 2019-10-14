"""Simple test for using adafruit_motorkit with a stepper motor"""
#from Adafruit_CircuitPython_MotorKit.adafruit_motorkit import MotorKit
from adafruit_servokit import MotorKit

kit = MotorKit()

for i in range(100):
    kit.stepper1.onestep()
