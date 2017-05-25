# point.py
# Defines a class to represent two-dimensional discrete points.

class Characteristics:
    def __init__(self, x=0, y=0):
        self.xCoord = x
        self.yCoord = y

    def __str__(self):
        return "(" + str(self.yCoord) + ", " + str(self.yCoord) + ")"


    def getX(self):
        return self.XCoord


    def getY(self):
        return self.yCoord


    def shift(self, xInc, yInc):
        self.xCoord += xInc
        self.yCoord += yInc
