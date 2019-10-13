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

    def __init__(self, Number=0):
        self.Number = Number
        self.UserUnits = 1
    def MoveSteps(self):
        return self.MoveSteps()
    def Stop(self):
        return self.MoveSteps()
    def MoveDistance(self):
        return self.MoveDistance()
    def Error(self,Message):
        print("Error: "+Message)
        sys.exit()


class Stepper(Axis):

        def __init__(self, Number=0):
            self.Number = Number
            self.Mode = stepper.SINGLE
            self.Count=0

        def MoveSteps(self,Direction,Steps):
            if(Direction>0):
                moveDirection=stepper.FORWARD
            elif(Direction<0):
                moveDirection=stepper.REVERSE
            else:
                super().Error("Invalid Direction")


            if(self.Number==0):
                kit.stepper1.release()
                for i in range(Steps):
                    kit.stepper1.onestep(moveDirection, self.Mode)
            elif(self.Number==1):
                kit.stepper2.release()
                for i in range(Steps):
                    kit.stepper2.onestep(moveDirection, self.Mode)

            self.Count+=(Direction*Steps)

        def GetLoc(self):
            return self.Count/self.UserUnits


        def MoveDistance(self,Distance):
            Steps=abs(Distance*self.UserUnits)
            if(Distance>0):
                Direction=1
            elif(Distance<0):
                Direction=-1

            self.MoveSteps(Direction,Steps)

        def Stop(self):
            self.MoveSteps(Direction.POS)
            self.MoveSteps(Direction.NEG)
        def Zero(self):
            self.Count=0

        def Home(self):
            print("NOT Implemented")


