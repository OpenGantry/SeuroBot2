"""Simple test for using adafruit_motorkit with a stepper motor"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

import time

kit = MotorKit(0x6f)

NotDone = True

while NotDone:
    print("Single coil steps")
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
    time.sleep(8)
    print("Double coil steps")
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    time.sleep(8)
    print("Interleaved coil steps")
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
    time.sleep(8)
    print("Microsteps")
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
    for i in range(200):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)

    notDone = False

