#Author: Yadong Jiang @ NUI Galway Ireland
#Email: yadong.jiang@nuigalway.ie
#Created Date: 7th June 2018
#
#Description:
#    This is a python class which generate the NACA profiles

class NACA_Profile:

    def __init__(self, **kwargs):
        self.profileName = kwargs['profileName']
        if 'description' in kwargs:
            self.description = kwargs['description']
        else:
            self.description = self.profileName
        return None

