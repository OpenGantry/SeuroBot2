from simple_pid import PID
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import time
import pigpio

import rotary_encoder
import time

pid = PID(.005, 0.01, 0.005, setpoint=0)
pid.output_limits = (-.5, .5)    # output value will be between 0 and 10
pid.sample_time = 0.01  # update every 0.01 seconds

kit = MotorKit(0x6f)

# assume we have a system we want to control in controlled_system
#v = controlled_system.update(0)
pos = 0


def callback(way):
    global pos

    pos += way

    print("pos={}".format(pos))

def main():
    print("Hello World!")
    pi = pigpio.pi()
    decoder = rotary_encoder.decoder(pi, 7, 8, callback)
    pid.setpoint=800
    while True:

        v = pos
        control = pid(v)  # compute new ouput from the PID according to the systems current value
        print("Control: ", control, "Pos: ",pos)
        # feed the PID output to the system and get its current value
        # v = controlled_system.update(control)
        kit.motor4.throttle = control


if __name__ == "__main__":
    main()
