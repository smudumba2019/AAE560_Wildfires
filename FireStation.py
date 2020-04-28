# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 12:07:17 2020

@author: Sai V. Mudumba
"""
import matplotlib.pyplot as plt
from LandGeneration import *
from FireCell import c1
import math

class FireStation():
    def __init__(self):
        # INITIATE THE FIRE STATION 1 AT THE CENTER 
        self.FS1Row = Land1.ResAreaCenters[0][1]
        self.FS1Col = Land1.ResAreaCenters[0][0]
        # INITIATE THE FIRE STATION 2 AT THE CENTER
        self.FS2Row = Land1.ResAreaCenters[1][1]
        self.FS2Col = Land1.ResAreaCenters[1][0]

    
    def GraphFireStation(self):
        plt.plot(self.FS1Col, self.FS1Row, 'rP')
        plt.plot(self.FS2Col, self.FS2Row, 'rP')
        plt.show
        
    def getFireDistance(self, FSrow, FScol):
        row_fire = c1.fuel[0]
        col_fire = c1.fuel[1]
        y = abs(FSrow - row_fire)
        x = abs(FScol - col_fire)
        Dist = math.sqrt(x**2 + y**2)
        return Dist
    
    def findClosestFireStation(self):
        # FIND THE GEODESIC DISTANCE OF FIRE ALERT AND FIRE STATION ON BOTTOM LEFT REGION
        DistGeo1 = self.getFireDistance(self.FS1Row, self.FS1Col)
        print("Geodesic Distance from Fire Station 1: " + str(DistGeo1))

        # FIND THE GEODESIC DISTANCE OF FIRE ALERT AND FIRE STATION ON TOP RIGHT REGION                
        DistGeo2 = self.getFireDistance(self.FS2Row, self.FS2Col)         
        print("Geodesic Distance from Fire Station 2: " + str(DistGeo2))

        # FIND THE CLOSEST FIRE STATION:
        if DistGeo1 < DistGeo2:
            return [self.FS1Row, self.FS1Col]
        elif DistGeo1 > DistGeo2:
            return [self.FS2Row, self.FS2Col]
        else:
            return [self.FS1Row, self.FS1Col]
                
    def findFarthestFireStation(self):
        # FIND THE GEODESIC DISTANCE OF FIRE ALERT AND FIRE STATION ON BOTTOM LEFT REGION
        DistGeo1 = self.getFireDistance(self.FS1Row, self.FS1Col)
        print("Geodesic Distance from Fire Station 1: " + str(DistGeo1))

        # FIND THE GEODESIC DISTANCE OF FIRE ALERT AND FIRE STATION ON TOP RIGHT REGION                
        DistGeo2 = self.getFireDistance(self.FS2Row, self.FS2Col)         
        print("Geodesic Distance from Fire Station 2: " + str(DistGeo2))

        # FIND THE CLOSEST FIRE STATION:
        if DistGeo1 > DistGeo2:
            return [self.FS1Row, self.FS1Col]
        elif DistGeo1 < DistGeo2:
            return [self.FS2Row, self.FS2Col]
        else:
            return [self.FS2Row, self.FS2Col]
        
FS1 = FireStation()
FSG = FS1.GraphFireStation()
DIST = FS1.findClosestFireStation()
print(DIST)