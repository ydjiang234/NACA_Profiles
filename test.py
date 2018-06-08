from NACA_Class import NACA_Profile, NACA4Digits
import numpy as np
import matplotlib.pyplot as plt

a = NACA4Digits(profileName='NACA2412', chordLength=1.0, twist = 0.0, description='A test profile')
b = NACA4Digits(profileName='NACA2412', chordLength=2.0, twist = 90, description='A test profile')
X, Y = a.getUpperXYdata()
plt.plot(X, Y, 'o-')
X, Y = b.getLowerXYdata()
plt.plot(X, Y, 'o-')
plt.axis('equal')
#plt.plot(a.upperPointX,a.upperPointY)
#plt.plot(a.lowerPointX,a.lowerPointY)
plt.show()
