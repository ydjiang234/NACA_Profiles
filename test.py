from NACA_Class import NACA_Profile, NACA4Digits
import numpy as np
import matplotlib.pyplot as plt

a = NACA4Digits(profileName='NACA9912', chordLength=1.5, twist = 0.0, description='A test profile')
b = NACA4Digits(profileName='NACA0012', chordLength=1.0, twist = 0.0, description='A test profile')
X, Y = a.getXYdata()
plt.plot(X, Y, 'o-')
X, Y = b.getXYdata()
#plt.plot(X, Y, 'o-')
plt.axis('equal')
plt.grid()
#plt.plot(a.upperPointX,a.upperPointY)
#plt.plot(a.lowerPointX,a.lowerPointY)
plt.show()
