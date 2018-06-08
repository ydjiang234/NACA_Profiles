from NACA_Class import NACA_Profile
import numpy as np
import matplotlib.pyplot as plt

a = NACA_Profile(profileName='NACA2412', description='A test profile')
print(a.description)
plt.show()
