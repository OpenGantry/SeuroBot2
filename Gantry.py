from Axis import *


class Location:
    def __init__(self, x=0, y=0, z=0):
        X = x
        Y = y
        X = z


class Gantry:
    def __init__(self):

        self.X_Axis = Motor(4,QuadratureEncoder(7,8),22,27)
        self.Y_Axis = Motor(3,QuadratureEncoder(9,10),22,27)
        self.Z_Axis = Motor(3,QuadratureEncoder(9,10),22,27)

    def get_x(self):
        self.X_Axis.get_loc()

    def get_y(self):
        self.Y_Axis.get_loc()

    def get_z(self):
        self.Z_Axis.get_loc()

    def zero_xy(self):
        self.X_Axis.zero()
        self.Y_Axis.zero()

    def move_delta_xy(self, xDelta, yDelta):
        self.X_Axis.move_distance(xDelta)
        self.Y_Axis.move_distance(yDelta)

    def move_delta_xyz(self, xDelta, yDelta, zDelta):
        self.X_Axis.move_distance(xDelta)
        self.Y_Axis.move_distance(yDelta)
        self.Z_Axis.move_distance(zDelta)

    def move_delta_z(self, z_delta):
        self.Z_Axis.move_distance(z_delta)

    def move_loc_xy(self, x_loc, y_loc):
        self.X_Axis.move_location(x_loc)
        self.Y_Axis.move_location(y_loc)
    '''
    def move_loc_xy(self, Location):
        self.MoveLocXY(Location.X, Location.Y)
    '''

class GridType(Enum):
    Standard = 0
    Compact = 1


class XYGrid:
    def __init__(self, NumberCol=16, NumberRow=16, type=GridType.Standard):
        self.xLoc = 0
        self.yLoc = 0
        if (type == GridType.Standard):
            self.UserUnits = 16  # cm
        elif (type == GridType.Compact):
            self.UserUnits = 7  # cm
