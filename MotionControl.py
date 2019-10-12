#from adafruit_motorkit import MotorKit

from Adafruit_CircuitPython_MotorKit import adafruit_motorkit
from Adafruit_CircuitPython_MotorKit.adafruit_motorkit import MotorKit

kit = MotorKit()

for i in range(100):
    kit.stepper1.onestep()