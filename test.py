from NACA_Class import NACA_Profile, NACA4Digits, NACA5Digits
import numpy as np
import matplotlib.pyplot as plt

a = NACA5Digits(profileName='NACA23015', isClose=False, chordLength=1.0, twist = 0.0, description='A test profile')
b = NACA4Digits(profileName='NACA2412', isClose=True, chordLength=1.0, twist = 0.0, description='A test profile')
X, Y = a.getXYdata()
plt.plot(X, Y, 'o-')
X, Y = a.getCamberXYdata()
plt.plot(X, Y, 'o-')

data = np.loadtxt('23015.txt').T
plt.plot(data[0], data[1], 'o-')
plt.axis('equal')
plt.grid()
#plt.plot(a.upperPointX,a.upperPointY)
#plt.plot(a.lowerPointX,a.lowerPointY)
plt.show()
print(a.m, a.K1)
