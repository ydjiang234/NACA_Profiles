from NACA_Class import NACA_Profile, NACA4Digits
import numpy as np
import matplotlib.pyplot as plt

a = NACA4Digits(profileName='NACA2412', chordLength=1.5, description='A test profile')
X, Y = a.combineUperLowerPoints()
plt.plot(X, Y)
#plt.plot(a.upperPointX,a.upperPointY)
#plt.plot(a.lowerPointX,a.lowerPointY)
plt.show()
