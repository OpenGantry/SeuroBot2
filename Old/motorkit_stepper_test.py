from Adafruit_CircuitPython_Motor.adafruit_motor import stepper
from Adafruit_CircuitPython_MotorKit.adafruit_motorkit import MotorKit
from adafruit_servokit import ServoKit

kit = MotorKit()

kit.stepper1.release()

while True:
    print("Single coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)

    print("Double coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    print("Interleaved coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)

    print("Microsteps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
