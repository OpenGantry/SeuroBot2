from Gantry import Gantry


Robot=Gantry()

Robot.X_Axis.UserUnits=1
Robot.Y_Axis.UserUnits=1

Robot.move_loc_xy(200, 200)
