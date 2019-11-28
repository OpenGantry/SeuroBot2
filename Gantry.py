from Axis import *

class Location:
    def __init__(self,x=0,y=0,z=0):
        X = x
        Y = y
        X = z

class Gantry:
    def __init__(self):
        self.X_Axis=Axis(4, AxisType.Motor,3,4,None,Feedback(FeedbackType.QuadratureEncoder,7,8))
        self.Y_Axis=Axis(1, AxisType.Motor,3,4,None,Feedback(FeedbackType.QuadratureEncoder,7,8))
        self.Z_Axis=Axis(2, AxisType.Motor,3,4,None,Feedback(FeedbackType.QuadratureEncoder,7,8))

    def GetX(self):
        self.X_Axis.GetLoc()
    def GetY(self):
        self.Y_Axis.GetLoc()
    def GetZ(self):
        self.Z_Axis.GetLoc()

    def ZeroXY(self):
        self.X_Axis.Zero()
        self.Y_Axis.Zero()

    def MoveDeltaXY(self,xDelta,yDelta):
        self.X_Axis.MoveDistance(xDelta)
        self.Y_Axis.MoveDistance(yDelta)

    def MoveDeltaXYZ(self,xDelta,yDelta,zDelta):
        self.X_Axis.MoveDistance(xDelta)
        self.Y_Axis.MoveDistance(yDelta)
        self.Z_Axis.MoveDistance(zDelta)

    def MoveDeltaZ(self,zDelta):
        self.Z_Axis.MoveDistance(zDelta)

    def MoveLocXY(self,xLoc,yLoc):
        self.X_Axis.MoveLocation(xLoc)
        self.Y_Axis.MoveLocation(yLoc)


    def MoveLocXY(self,Location):
        self.MoveLocXY(Location.X,Location.Y)






class GridType(Enum):
    Standard = 0
    Compact = 1

class XYGrid:
    def __init__(self,NumberCol=16,NumberRow=16,type=GridType.Standard):
        self.xLoc=0
        self.yLoc=0
        if(type==GridType.Standard):
            self.UserUnits=16#cm
        elif(type==GridType.Compact):
            self.UserUnits=7#cm




