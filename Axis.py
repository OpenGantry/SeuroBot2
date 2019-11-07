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


Count = 0


class Axis:

    def __init__(self, number=0, actuator=AxisType.Stepper, feedback=FeedbackType.QuadratureEncoder):
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

        if actuator == AxisType.Stepper:
            self.SubAxis = _Stepper(self.Number)
        if actuator == AxisType.Motor:
            self.SubAxis = _Motor(self.Number)

        self.FeedbackDevice = Feedback(feedback)
        self.PositionController = PID(.005, 0.01, 0.005, setpoint=0)

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
    def stop(self):
        if self.Number == 1:
            MotorController.motor1.throttle = 0
        elif self.Number == 2:
            MotorController.motor2.throttle = 0
        elif self.Number == 3:
            MotorController.motor3.throttle = 0
        elif self.Number == 4:
            MotorController.motor4.throttle = 0

    def move_distance(self, distance):
        cycles_at_finish = 0
        target = (distance * self.UserUnits)
        self.PositionController.setpoint = target
        done = False
        while not done:

            control = self.PositionController(Count)
            if control > self.PositiveCommandMinimum or control < self.NegativeCommandMinimum:
                if self.Number == 1:
                    MotorController.motor1.throttle = control
                elif self.Number == 2:
                    MotorController.motor2.throttle = control
                elif self.Number == 3:
                    MotorController.motor3.throttle = control
                elif self.Number == 4:
                    MotorController.motor4.throttle = control

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


class Feedback:

    def __init__(self, type=FeedbackType.QuadratureEncoder):
        self.Count = 0
        if (type == FeedbackType.QuadratureEncoder):
            self.SubAxis = _QuadratureEncoder()


class _QuadratureEncoder:
    def __init__(self):
        self.Count = 0
        self.encA = 7
        self.encB = 8
        pi = pigpio.pi()
        decoder = rotary_encoder.decoder(pi, self.encA, self.encB, self.callback)

    def callback(way):
        global Count
        Count += way


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
