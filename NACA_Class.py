#Author: Yadong Jiang @ NUI Galway Ireland
#Email: yadong.jiang@nuigalway.ie
#Created Date: 7th June 2018
#
#Description:
#    This is a python class which generate the NACA profiles

import numpy as np
from GeneralProfileClass import GeneralProfile

class NACA_Profile:

    def __init__(self, **kwargs):
        self.profileName = kwargs['profileName']
        #Description
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = self.profileName
        #Chrod Length
        if 'chordLength' in kwargs:
            self.chordLength = kwargs['chordLength']
        else:
            self.chordLength = 1.0
        #Twist
        if 'twist' in kwargs:
            self.twist = kwargs['twist']
        else:
            self.twist = 0.0
        #Transfer
        if 'transfer' in kwargs:
            self.transfer = kwargs['transfer']
        else:
            self.transfer = (0.0, 0.0)
        #PointNum
        if 'pointNum' in kwargs:
            self.pointNum = kwargs['pointNum']
        else:
            self.pointNum = 50

        #Leading edge location
        if 'leadingPoint' in kwargs:
            self.leadingPoint = kwargs['leadingPoint']
        else:
            self.leadingPoint = (0.0, 0.0)

        return None

    #Combine the upper and lower points (not scaled)
    def combineUperLowerPoints(self):
        tempX = self.lowerProfile.Xdata
        tempY = self.lowerProfile.Ydata
        #Check if the last points of the two profiles are the same
        if (self.upperProfile.Xdata[-1] == self.lowerProfile.Xdata[-1]) and (self.upperProfile.Ydata[-1] == self.lowerProfile.Ydata[-1]):
            tempX = tempX[:-1]
            tempY = tempY[:-1]
        #Reverse the tempX and tempY
        tempX = tempX[::-1]
        tempY = tempY[::-1]
        #Combine the upper and lower points
        outX = np.append(self.upperProfile.Xdata, tempX)
        outY = np.append(self.upperProfile.Ydata, tempY)
        return outX, outY

    def generateProfiles(self):
        #Make tranfer to the upper and lower profiles
        for profile in [self.upperProfile, self.lowerProfile]:
            profile.rotate(self.twist, self.leadingPoint)
            profile.scale(self.chordLength, self.leadingPoint)
            profile.transfer(self.transfer)
        #Combine the upper and lower points
        tempX, tempY = self.combineUperLowerPoints()
        self.profile = GeneralProfile(tempX, tempY)

    def getXYdata(self, Type=0):
        if Type == 0:
            X, Y = self.profile.getXYdata()
            return X, Y
        elif Type == 1:
            return self.profile.getPoints()

    def getUpperXYdata(self, Type=0):
        if Type == 0:
            X, Y = self.upperProfile.getXYdata()
            return X, Y
        elif Type == 1:
            return self.upperProfile.getPoints()

    def getLowerXYdata(self, Type=0):
        if Type == 0:
            return self.lowerProfile.getXYdata()
        elif Type == 1:
            return self.lowerProfile.getPoints()

class NACA4Digits(NACA_Profile):

    def __init__(self, **kwargs):
        NACA_Profile.__init__(self, **kwargs)
        self.ycFun = np.vectorize(self.ycFun1)
        self.thetaFun= np.vectorize(self.thetaFun1)
        self.parseParameters()
        self.generateUnitProfiles()
        self.generateProfiles()
        return None

    def parseParameters(self):
        #Maximum thickness as a fraction of the chord
        self.t = float(self.profileName[-2:]) / 100.0
        #Maximum camber
        self.m = float(self.profileName[-4]) / 100.0
        #Location of maximum camber
        self.p = float(self.profileName[-3]) / 10.0
        if (self.m==0.0) and (self.p==0.0):
            self.isSym = True
        else:
            self.isSym = False
        return None

    def ytFun(self, x):
        yt = 5.0 * self.t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1015 * x**4)
        return yt

    def ycFun1(self, x):
        if self.isSym:
            yc = 0.0
        else:
            if x<=self.p:
                yc = self.m / self.p**2 * (2.0 * self.p *x - x**2)
            else:
                yc = self.m / (1.0 - self.p)**2 * ((1.0 - 2.0 * self.p) + 2.0 * self.p * x - x**2)
        return yc

    def thetaFun1(self, x):
        if self.isSym:
            theta = 0.0
        else:
            if x<=self.p:
                theta = 2.0 * self.m / self.p**2 * (self.p - x)
            else:
                theta = 2.0 * self.m / (1.0 - self.p)**2 * (self.p - x)
        return theta

    def generateUnitProfiles(self):
        tempX = np.linspace(0.0, 1.0, self.pointNum)
        tempYt = self.ytFun(tempX)
        tempYc = self.ycFun(tempX)
        tempTheta = self.thetaFun(tempX)

        self.upperProfile = GeneralProfile(tempX - tempYt * np.sin(tempTheta), tempYc + tempYt * np.cos(tempTheta))
        self.lowerProfile = GeneralProfile(tempX + tempYt * np.sin(tempTheta), tempYc - tempYt * np.cos(tempTheta))
