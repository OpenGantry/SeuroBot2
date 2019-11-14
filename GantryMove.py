from simple_pid import PID
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import time
import pigpio

import rotary_encoder
import time

from Gantry import *
from Axis import  *

def main():
    Gantry()
    while True:

        Gantry.X_Axis.move_distance(30)
        if Gantry.X_Axis.InFinePosition:
            Gantry.X_Axis.move_distance(0)




if __name__ == "__main__":
    main()
