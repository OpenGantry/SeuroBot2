"""Axis"""
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import sys
from enum import Enum

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
        if(Type==AxisType.Stepper):
            self.SubAxis=Stepper(self.Number)

    def MoveSteps(self,Steps,Direction=None):
        return self.SubAxis.MoveSteps(Steps,Direction)
    def Stop(self):
        return self.SubAxis.MoveSteps()
    def MoveDistance(self,Distance):
        return self.SubAxis.MoveDistance(Distance)
    def SetUserUnits(self,UserUnits):
        self.SubAxis.SetUserUnits(UserUnits)

    #Super Class Functions
    def Error(self,Message):
        print("Error: "+Message)
        sys.exit()
    def Warn(self,Message):
        print("Warning : "+Message)

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
                kit.stepper1.onestep(moveDirection, self.Mode)
        elif(self.Number==1):
            kit.stepper2.release()
            for i in range(Steps):
                kit.stepper2.onestep(moveDirection, self.Mode)

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


