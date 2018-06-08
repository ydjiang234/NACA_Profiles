#Author: Yadong Jiang @ NUI Galway Ireland
#Email: yadong.jiang@nuigalway.ie
#Created Date: 7th June 2018
#
#Description:
#    This is a python class which generate the NACA profiles

import numpy as np

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
        #Initial upper points
        self.upperPointX = np.array([])
        self.upperPointY = np.array([])
        #initial lower points
        self.lowerPointX = np.array([])
        self.lowerPointY = np.array([])
        return None

    #Combine the upper and lower points (not scaled)
    def combineUperLowerPoints(self):
        tempX = self.lowerPointX
        tempY = self.lowerPointY
        '''
        #Check if the fisrt point is the same 
        if (self.upperPointX[0] == self.lowerPointX[0]) and (self.upperPointY[0] == self.lowerPointY[0]):
            tempX = tempX[1:]
            tempY = tempY[1:]
        '''
        #Check if the last point is the same
        if (self.upperPointX[-1] == self.lowerPointX[-1]) and (self.upperPointY[-1] == self.lowerPointY[-1]):
            tempX = tempX[:-1]
            tempY = tempY[:-1]
        #Reverse the tempX and tempY
        tempX = tempX[::-1]
        tempY = tempY[::-1]
        #Combine the upper and lower points
        outX = np.append(self.upperPointX, tempX)
        outY = np.append(self.upperPointY, tempY)
        return outX, outY
    
    #Rotate the profile
    def rotate(self, angle):
        

class NACA4Digits(NACA_Profile):

    def __init__(self, **kwargs):
        NACA_Profile.__init__(self, **kwargs)
        #Maximum thickness as a fraction of the chord
        self.t = float(self.profileName[-2:]) / 100.0

        self.generate()
        return None

    def generate(self):
        tempX = np.linspace(0.0, 1.0, self.pointNum)
        tempY = 5.0 * self.t * (0.2969 * np.sqrt(tempX) - 0.1260 * tempX - 0.3516 * tempX**2 + 0.2843 * tempX**3 - 0.1015 * tempX**4) 
        self.upperPointX = tempX
        self.upperPointY = tempY
        self.lowerPointX = tempX
        self.lowerPointY = -1.0 * tempY
