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
        #Is close
        if 'isClose' in kwargs:
            self.isClose = kwargs['isClose']
        else:
            self.isClose = (0.0, 0.0)

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

    def getCamberXYdata(self, Type=0):
        if Type == 0:
            return self.camberProfile.getXYdata()
        elif Type == 1:
            return self.camberProfile.getPoints()

    def generateUnitProfiles(self):
        tempX = np.linspace(0.0, 1.0, self.pointNum)
        tempYt = self.ytFun(tempX)
        tempYc = self.ycFun(tempX)
        tempTheta = self.thetaFun(tempX)

        self.upperProfile = GeneralProfile(tempX - tempYt * np.sin(tempTheta), tempYc + tempYt * np.cos(tempTheta))
        self.lowerProfile = GeneralProfile(tempX + tempYt * np.sin(tempTheta), tempYc - tempYt * np.cos(tempTheta))
        self.camberProfile = GeneralProfile(tempX, tempYc)

    def generateProfiles(self):
        #Make tranfer to the upper and lower profiles
        for profile in [self.upperProfile, self.lowerProfile, self.camberProfile]:
            profile.rotate(self.twist, self.leadingPoint)
            profile.scale(self.chordLength, self.leadingPoint)
            profile.transfer(self.transfer)
        #Combine the upper and lower points
        tempX, tempY = self.combineUperLowerPoints()
        self.profile = GeneralProfile(tempX, tempY)

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
        if self.isClose:
            yt = 5.0 * self.t * (0.2969 * np.sqrt(x) - 0.1260 * x - 0.3516 * x**2 + 0.2843 * x**3 - 0.1036 * x**4)
        else:
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
            temp = 0.0
        else:
            if x<=self.p:
                temp = 2.0 * self.m / self.p**2 * (self.p - x)
            else:
                temp = 2.0 * self.m / (1.0 - self.p)**2 * (self.p - x)
        return np.arctan(temp)

class NACA5Digits(NACA4Digits):

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
        #Is relexed
        reflex = int(self.profileName[-3])
        if reflex==0:
            self.isReflex = False
        elif reflex==1:
            self.isReflex = True
        #Location of maximum camber
        self.xf = float(self.profileName[-4]) / 20.0
        #Design lift coefficient
        self.Cli = 1.5 * float(self.profileName[-5]) / 10.0

        self.otherParameters()
        return None

    def otherParameters(self):
        self.m = self.solveM()
        aa = 3.0 * self.m - 7.0 * self.m**2 + 8.0 * self.m**3 - 4.0 * self.m**4
        bb = np.sqrt(self.m * (1.0 - self.m))
        cc = 3.0 / 2.0 * (1.0 - 2.0 * self.m)
        dd = np.pi / 2.0 - np.arcsin(1.0 - 2.0 * self.m)
        Q = aa / bb - cc * dd
        self.K1 = 6.0 * self.Cli / Q
        aaa = 3.0 * (self.m - self.xf)**2 - self.m**3
        bbb = (1.0 - self.m**3)
        self.K2 = aaa / bbb * self.K1

    def xfFun(self, m):
        return m * (1.0 - np.sqrt(m / 3.0))

    def solveM(self, num=20):
        from scipy.interpolate import interp1d
        tempM = np.linspace(0.0, 1.0, num)
        tempXf = self.xfFun(tempM)
        mFun = interp1d(tempXf, tempM, kind='linear', bounds_error=False, fill_value=(0.0, 1.0))
        return mFun(self.xf)

    def ycFun1(self, x):
        if self.isReflex:
            if x<=self.m:
                yc = 0.0
            else:
                yc = 0.0      
        else:
            if x<=self.m:
                yc = self.K1 / 6.0 * (x**3 - 3.0 * self.m * x**2 + self.m**2 * (3.0 - self.m) * x)
            else:
                yc = self.K1 * self.m**3 / 6.0 * (1.0 - x)

        return yc

    def thetaFun1(self, x):
        if self.isReflex:
            if x<=self.m:
                temp = 0.0
            else:
                temp = 0.0
        else:
            if x<=self.m:
                temp = self.K1 / 6.0 * (3.0 * x**2 - 6.0 * self.m * x + self.m**2 * (3.0 - self.m))
            else:
                temp = -1.0 * self.K1 * self.m**3 / 6.0
        return np.arctan(temp)
