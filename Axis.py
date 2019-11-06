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
import pigpio

import rotary_encoder
import time

kit = MotorKit(0x6f)


class Direction(Enum):
    POS = 1
    NEG = -1

class AxisType(Enum):
    Stepper = 0
    Servo = 1
    Motor = 2


class Axis:

    def __init__(self, Number=0,Type=AxisType.Stepper):
        self.Number = Number
        self.UserUnits = 1
        self.Count = 0
        self.DebugMode=True
        self.Enabled=True
        self.ReleaseOnFinish=False
        self.BrakeOnFinish=True
        self.HoldOnFinish=True
        self.AllowableError=0

        if(Type==AxisType.Stepper):
            self.SubAxis=Stepper(self.Number)
        if(Type==AxisType.Motor):
            self.SubAxis=Motor(self.Number)

    def MoveVelocity(self,Velocity):
        return self.SubAxis.MoveVelocity(Velocity)
    def Stop(self):
        self.MoveDistance(0)
    def MoveDistance(self,Distance):
        if self.Enabled:
            return self.SubAxis.MoveDistance(Distance)
        else:
            self.PrintStatus()
    def SetUserUnits(self,UserUnits):
        self.SubAxis.SetUserUnits(UserUnits)

    def PrintStatus(self):
        print("Axis: ",self.Number," Status: ", self.Enabled, " UserUnits: ", self.UserUnits, "Count: ", self.Count)



    #Super Class Functions
    def Error(self,Message):
        print("Error: "+Message)
        sys.exit()
    def Warn(self,Message):
        print("Warning : "+Message)
class Motor(Axis):
    def __init__(self, Number=0):
        self.P=0
        self.I=0
        self.D=0
        self.PositiveCommandLimit=1
        self.NegativeCommandLimit=-11
        self.PositiveCommandMinimum=0
        self.NegativeCommandMinimum=0
        self.SampleTime=0.01
        self.encA=7
        self.encB=8
        self.
        pid = PID(self.P,self.I, self.D, setpoint=0)
        pid.output_limits = (self.NegativeCommandLimit, self.PositiveCommandLimit)
        pid.sample_time = self.SampleTime
        pi = pigpio.pi()
        decoder = rotary_encoder.decoder(pi, self.encA, self.encB, self.callback)

    def callback(way):
        #global pos
        super.Count += way
        if super.DebugMode:
            print("pos={}".format(super.Count))

    def MoveDistance(self,Distance):
        CyclesAtFinish=0
        target=Distance*super.UserUnits
        self.pid.setpoint = target
        Done=False
        while (not Done):

            control = self.pid(super.Count)
            if(control>self.PositiveCommandMinimum or control<self.NegativeCommandMinimum):
                if(super.Number==1):
                    kit.motor1.throttle = control
                elif(super.Number==2):
                    kit.motor2.throttle = control
                elif (super.Number == 3):
                    kit.motor3.throttle = control
                elif (super.Number == 4):
                    kit.motor4.throttle = control

            if(not super.HoldOnFinish):
                if(target==super.Count):
                    CyclesAtFinish+=1
                    if CyclesAtFinish>1000:
                        Done=True

            if super.DebugMode:
                print("Target: ",target,"Control: ", control, "Count: ", super.Count)


        if (super.ReleaseOnFinish):
            kit.stepper1.release()
            kit.stepper2.release()





class Stepper(Axis):

    def __init__(self, Number=0):
            self.Number = Number
            self.Mode = stepper.SINGLE
            self.Count=0
            self.UserUnits=1

    def SetUserUnits(self,UserUnits):
        self.UserUnits=UserUnits

    def MoveSteps(self,Steps,Direction=None):
        if Direction is None:

            if (Steps > 0):
                Direction=1
                moveDirection=stepper.FORWARD
            elif (Steps < 0):
                Direction=-1
                moveDirection=stepper.REVERSE
            else:
                super().Warn("Steps = 0")
        else:
            if(Direction>0):
                moveDirection=stepper.FORWARD
            elif(Direction<0):
                moveDirection=stepper.REVERSE
            else:
                super().Error("Invalid Direction")

        Steps = abs(Steps)

        if(self.Number==0):
            kit.stepper1.release()
            for i in range(Steps):
                kit.stepper1.onestep(direction=moveDirection, style=self.Mode)
        elif(self.Number==1):
            kit.stepper2.release()
            for i in range(Steps):
                kit.stepper2.onestep(direction=moveDirection, style=self.Mode)

        self.Count+=(Direction*Steps)#update our current position

    def GetLoc(self):
        return self.Count/self.UserUnits


    def MoveDistance(self,Distance):
        Steps=(Distance*self.UserUnits)
        self.MoveSteps(Steps)

    def MoveLocation(self,Loc):
        Loc=Loc*self.UserUnits#convert location in user unit to ticks
        if(Loc>self.Count):
            moveDirection=stepper.FORWARD
        elif(Loc<self.Count):
            moveDirection=stepper.REVERSE
        else:
            super().Warn("New location equal to current location.")

        self.MoveSteps(moveDirection,abs(self.Count-Loc))


    def Stop(self):
        self.MoveSteps(Direction.POS)
        self.MoveSteps(Direction.NEG)

    def Zero(self):
        self.Count=0

    def Home(self):
        print("NOT Implemented")


