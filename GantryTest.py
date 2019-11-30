from Gantry import Gantry


Robot=Gantry()

Robot.X_Axis.UserUnits=1
Robot.Y_Axis.UserUnits=1

Robot.MoveDeltaXY(200, 200)
