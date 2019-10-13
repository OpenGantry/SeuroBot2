from Axis import *

Class Location:


def __init__(self,x,y,z):
    X = x
    Y = y
    X = z

class Gantry:
    def __init__():
        X_Axis=Axis(0)
        Y_Axis=Axis(1)
        X_Axis=Axis(2)
    def GetX(self):
        self.X_Axis.GetLoc()
    def GetY(self):
        self.Y_Axis.GetLoc()
    def GetZ(self):
        self.Z_Axis.GetLoc()

    def MoveXY(self,xDelta,yDelta):
        self.X_Axis.MoveDistance(xDelta)
        self.Y_Axis.MoveDistance(yDelta)
    def MoveXYZ(self,xDelta,yDelta,zDelta):
        self.X_Axis.MoveDistance(xDelta)
        self.Y_Axis.MoveDistance(yDelta)
        self.Z_Axis.MoveDistance(zDelta)

    def MoveZ(self,zDelta):
        self.Z_Axis.MoveDistance(zDelta)

    def GoTO(self,xLoc,yLoc):


    def GoTo(self):




class GridType(Enum):
    Standard = 0
    Compact = 1

class Grid:
    def __init__(self,NumberCol=16,NumberRow=16,type=GridType.Standard):
        self.xLoc
        self.yLoc
        self.zLoc
        if(type==GridType.Standard):
            self.UserUnits=16#cm
        elif(type==GridType.Compact):
            self.UserUnits=7#cm




