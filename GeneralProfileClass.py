#Author: Yadong Jiang @ NUI Galway Ireland
#Email: yadong.jiang@nuigalway.ie
#Created Date: 8th June 2018
#
#Description:
#    This is a gerenal profile class, which contains the XY data of a profile, you can make rotate, scale and transfer the profile..

import numpy as np

class GeneralProfile:

    def __init__(self, *args):
        if len(args) == 1:
            self.setPoints(args[0])
        elif len(args) == 2:
            self.setPoints(args[0], args[1])
        return None

    #Set profile points by XY data
    def setPoints(self, Xdata, Ydata):
        self.Xdata, self.Ydata = Xdata, Ydata
        return None
    
    #Set profile points by pointArray
    def setPointsByArray(self, pointArray):
        self.Xdata, self.Ydata = self.pointArrayToXYdata(pointArray)
        return None

    def XYdataToPointArray(self, Xdata, Ydata):
        out = np.vstack((Xdata, Ydata)).T
        return out

    def pointArrayToXYdata(self, pointArray):
        return pointArray[:,0], pointArray[:,1]
    #Rotate profile aournd the centre point
    def rotate(self, angle, centrePoint):
        angle = angle  * np.pi / 180.0
        tempX = self.Xdata - centrePoint[0]
        tempY = self.Ydata - centrePoint[1]
        outX = tempX * np.cos(angle) - tempY * np.sin(angle)
        outY = tempX * np.sin(angle) + tempY * np.cos(angle)
        outX += centrePoint[0]
        outY += centrePoint[1]
        self.Xdata = outX
        self.Ydata = outY

    #Transfer profile by a vector
    def transfer(self, vector):
        self.Xdata += vector[0]
        self.Ydata += vector[1]
    
    #Scale profile according to the centre point
    def scale(self, scaleFactor, centrePoint):
        outX = self.Xdata - centrePoint[0]
        outY = self.Ydata - centrePoint[1]
        outX *= scaleFactor
        outY *= scaleFactor
        outX += centrePoint[0]
        outY += centrePoint[1]
        self.Xdata = outX
        self.Ydata = outY

    def getXYdata(self):
        return self.Xdata, self.Ydata

    def getPoints(self):
        return self.XYdataToPointArray(self.Xdata, self.Ydata)
