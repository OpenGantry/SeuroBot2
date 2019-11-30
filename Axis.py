"""Axis"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import sys
from enum import Enum
from simple_pid import PID
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import time
import sys
from enum import Enum
import pigpio
import rotary_encoder

import RPi.GPIO as GPIO
import time
import threading

MotorController = MotorKit(0x6f)


# -------------------------Axis-------------------------
class Direction(Enum):
    POS = 1
    NEG = -1


class AxisType(Enum):
    none = 0
    Stepper = 1
    Servo = 2
    Motor = 3


class FeedbackType(Enum):
    none = 0
    QuadratureEncoder = 1


class ControllerType(Enum):
    none = 0
    PID = 1


class LimitAction(Enum):
    none = 0
    Abort = 1
    Disable = 2
    NegDisable = 3
    PosDisable = 4
    Home = 5


Count = 0


class Axis(object):
    def __init__(self, number, axis_type, feedback, pos_lim_switch, neg_lim_switch, home_switch=None):
        if axis_type == AxisType.Stepper:
            return _Stepper(number)
        elif axis_type == AxisType.Motor:
            return _Motor(number, feedback, pos_lim_switch, neg_lim_switch, home_switch)
        else:
            Axis.error("Unknown motor type.")

    def __init__(self, number, feedback, pos_lim_switch, neg_lim_switch, home_switch=None):
        self.Number = number
        self.UserUnits = 1
        self.DebugMode = True
        self.Enabled = True
        self.ReleaseOnFinish = False
        self.BrakeOnFinish = True
        self.HoldOnFinish = True
        self.AllowableError = 0
        self.PositiveCommandMinimum = 0
        self.NegativeCommandMinimum = 0
        self.MotionDone = True
        self.CoarsePositionError = 5
        self.InFinePosition = False
        self.InCoarsePosition = False
        self.NegativeTravelDisabled = False
        self.PositiveTravelDisabled = False

        if feedback != FeedbackType.none:
            self.FeedbackDevice = feedback

        self.PositionController = PID(.005, 0.01, 0.005, setpoint=0)
        """
        GPIO.setup(pos_lim_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP);
        GPIO.setup(pos_lim_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP);
        GPIO.setup(home_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP);

        GPIO.add_event_detect(pos_lim_switch, GPIO.BOTH, callback=self.pos_lim_callback)
        GPIO.add_event_detect(neg_lim_switch, GPIO.BOTH, callback=self.neg_lim_callback)
        GPIO.add_event_detect(home_switch, GPIO.BOTH, callback=self.home_callback)
        """

        #self.NegLimit = IO(neg_lim_switch, True, LimitAction.NegDisable, self.limit_action)
        #self.PosLimit = IO(pos_lim_switch, True, LimitAction.PosDisable, self.limit_action)
        #self.HomeSwitch = IO(home_switch, True, LimitAction.none, self.limit_action)

    def neg_lim_callback(self, input_pin):
        print("Input on pin", input_pin)
        current_state = self.NegLimit.get()
        action = self.NegLimit.Action
        if current_state:
            if action == LimitAction.Disable:
                self.Enabled = False
            elif action == LimitAction.Home:
                self.Home()
            elif action == LimitAction.NegDisable:
                self.NegativeTravelDisabled = current_state
            elif action == LimitAction.PosDisable:
                self.PositiveTravelDisabled = current_state
            else:
                self.error("Unknown limit action.")

    def pos_lim_callback(self, input_pin):
        print("Input on pin", input_pin)

    def home_callback(self, input_pin):
        print("Input on pin", input_pin)

    def limit_action(self, input_pin):
        print("Input on pin", input_pin)
        current_state = self.NegLimit.get()
        action = self.NegLimit.Action
        if current_state:
            if action == LimitAction.Disable:
                self.Enabled = False
            elif action == LimitAction.Home:
                self.Home()
            elif action == LimitAction.NegDisable:
                self.NegativeTravelDisabled = current_state
            elif action == LimitAction.PosDisable:
                self.PositiveTravelDisabled = current_state
            else:
                self.error("Unknown limit action.")

    def move_velocity(self, velocity):
        return self.SubAxis.move_velocity(velocity)

    def stop(self):
        self.move_distance(0)

    def move_distance(self, dist):
        if self.Enabled:
            return self.SubAxis.move_distance(dist)
        else:
            self.print_status()

    def set_user_units(self, units):
        self.SubAxis.set_user_units(units)

    def print_status(self):
        print("Axis: ", self.Number, " Status: ", self.Enabled, " UserUnits: ", self.UserUnits, "Count: ", Count)

    @staticmethod
    def error(message):
        print("Axis - Error: " + message)
        sys.exit()

    @staticmethod
    def warn(self, message):
        print("Axis - Warning : " + message)


class _Motor(Axis):
    # LocalMotorController: object

    def __init__(self, number, feedback, pos_lim_switch, neg_lim_switch, home_switch=None, ):
        super().__init__(self, number, AxisType.Motor, feedback, pos_lim_switch, neg_lim_switch, home_switch)
        if self.Number == 1:
            self.LocalMotorController = MotorController.motor1
        elif self.Number == 2:
            self.LocalMotorController = MotorController.motor2
        elif self.Number == 3:
            self.LocalMotorController = MotorController.motor3
        elif self.Number == 4:
            self.LocalMotorController = MotorController.motor4
        else:
            self.error("Axis must be 1-4 per shield")

    def stop(self):
        self.LocalMotorController.throttle = 0

    def move_velocity(self, velocity):
        self.error("Not Implemented")

    def command(self, vel):
        if self.Enabled:
            if vel > Axis.PositiveCommandMinimum or vel < Axis.NegativeCommandMinimum:
                if self.PositiveTravelDisabled and vel < 0:
                    if self.NegativeTravelDisabled and vel > 0:
                        self.LocalMotorController.throttle = vel

    def move_distance(self, distance):
        cycles_at_finish = 0
        target = (distance * self.UserUnits)
        self.PositionController.setpoint = target
        done = False
        while not done:

            control = self.PositionController(Count)
            self.command(control)

            if not self.HoldOnFinish:
                if target == Count:
                    cycles_at_finish += 1
                    if cycles_at_finish > 1000:
                        done = True

            if abs(target - Count) <= self.CoarsePositionError:
                self.InCoarsePosition = True
                if target == Count:
                    self.InFinePosition = True
                else:
                    self.InFinePosition = False
            else:
                self.InCoarsePosition = False

            if self.DebugMode:
                print("Moving with --- Target: ", target, "Control: ", control, "Count: ", Count)

        if self.ReleaseOnFinish:
            MotorController.stepper1.release()
            MotorController.stepper2.release()


class _Stepper(Axis):

    def __init__(self, number=0):
        self.Number = number
        self.Mode = stepper.SINGLE
        self.Count = 0
        self.UserUnits = 1

    def SetUserUnits(self, UserUnits):
        self.UserUnits = UserUnits

    def MoveSteps(self, Steps, Direction=None):
        if Direction is None:

            if (Steps > 0):
                Direction = 1
                moveDirection = stepper.FORWARD
            elif (Steps < 0):
                Direction = -1
                moveDirection = stepper.REVERSE
            else:
                super().warn("Steps = 0")
        else:
            if (Direction > 0):
                moveDirection = stepper.FORWARD
            elif (Direction < 0):
                moveDirection = stepper.REVERSE
            else:
                super().error("Invalid Direction")

        Steps = abs(Steps)

        if (self.Number == 0):
            MotorController.stepper1.release()
            for i in range(Steps):
                MotorController.stepper1.onestep(direction=moveDirection, style=self.Mode)
        elif (self.Number == 1):
            MotorController.stepper2.release()
            for i in range(Steps):
                MotorController.stepper2.onestep(direction=moveDirection, style=self.Mode)

        self.Count += (Direction * Steps)  # update our current position

    def GetLoc(self):
        return self.Count / self.UserUnits

    def MoveDistance(self, Distance):
        Steps = (Distance * self.UserUnits)
        self.MoveSteps(Steps)

    def MoveLocation(self, Loc):
        Loc = Loc * self.UserUnits  # convert location in user unit to ticks
        if (Loc > self.Count):
            moveDirection = stepper.FORWARD
        elif (Loc < self.Count):
            moveDirection = stepper.REVERSE
        else:
            super().Warn("New location equal to current location.")

        self.MoveSteps(moveDirection, abs(self.Count - Loc))

    def Stop(self):
        self.MoveSteps(Direction.POS)
        self.MoveSteps(Direction.NEG)

    def Zero(self):
        self.Count = 0

    def Home(self):
        print("NOT Implemented")


# -------------------------FEEDBACK-------------------------


class Feedback(object):
    '''
    def __init__(self, fb_type, pin_a, pin_b):
        if fb_type==FeedbackType.QuadratureEncoder:
            return _QuadratureEncoder(pin_a,pin_b)
        else:
            Feedback.error("Unknown feedback type.")
    '''

    def __init__(self, pin_a, pin_b):
        self.Count = 0
        self.encA = pin_a
        self.encB = pin_b
        self.Count

    @staticmethod
    def error(message):
        print("Feedback - Error: " + message)
        sys.exit()

    @staticmethod
    def warn(self, message):
        print("Feedback - Warning : " + message)


class QuadratureEncoder(Feedback):
    def __init__(self, A, B):
        super().__init__(A, B)
        self.Count = 0

        pi = pigpio.pi()
        decoder = rotary_encoder.decoder(pi, self.encA, self.encB, self.callback)

    def callback(self, way):
        # global Count
        self.Count += way


class IO:
    def __init__(self, pin, active_high, action, master_callback):
        self.active_high = active_high
        self.pin = pin
        # self.super_cb=master_callback
        self.action = action
        if active_high:
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)

            # GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.callback())
            GPIO.add_event_detect(pin, GPIO.BOTH, master_callback)

        else:
            GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP);
            GPIO.add_event_detect(pin, GPIO.BOTH, self.master_callback)

    def get_state(self):
        if self.active_high:
            return GPIO.input(self.pin)
        else:
            return not GPIO.input(self.pin)

    """    
    def callback(self,pin):
        self.super_cb(pin,self.action)
      """


# -------------------------Controller-------------------------
"""
class Controller:

    def __init__(self, type=ControllerType.PID):
        if (type == ControllerType.PID):
            self.SubAxis = _QuadratureEncoder()
            
class _PID:
    def __init__(self):
        self.P=.005
        self.I=.01
        self.D=.005
        pid = PID(self., 0.01, 0.005, setpoint=0)
        pid.output_limits = (-.5, .5)  # output value will be between 0 and 10
        pid.sample_time = 0.01  # update every 0.01 seconds
"""
