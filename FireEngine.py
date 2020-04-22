# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 17:15:33 2020

@author: Sai V. Mudumba
"""
import matplotlib.pyplot as plt
import math
from FireStation import *
from FireCell import *
class FireEngine(FireCell):
        
    def __init__(self):
        self.typ = 'Type 3 Wildland Engine' 
        self.tankCap = 500 # US GALLONS 
        self.flowRate = 50 # GALLONS PER MINUTE, WITH A MAX VALUE OF 150
        self.operCost = 217 # DOLLARS PER HOUR
        self.color = '#FF4500' # ORANGE RED HEX CODE
        self.FE1 = FS1.findClosestFireStation() # LAT CENTER OF RES AREA
        self.FE2 = FS1.findFarthestFireStation() # LON CENTER OF RES AREA
        
        
    def printVehicleDescription(self):
        print('Vehicle Type: ' + str(self.typ))
        print('Tank Capacity (US Gal): ' + str(self.tankCap))
        print('Flow Rate (US Gal/min): ' + str(self.flowRate))
        print('Operating Cost ($/hr): ' + str(self.operCost))
        print('Vehicle Color: ' + str(self.color))
        #print('Starting Vehicle Location: (' + str(self.) + ', ' + str(self.lat) + ')')
        return None 
    
    def graphFireEngine(self, lon, lat):
        plt.plot(lon, lat,'b,')
        plt.show()
        return None
        
    def countTime(self, time):
        time += 1 # in minutes
        return time 
        
    def goTo(self, fireLoc):
        row_fire = fireLoc[0]
        col_fire = fireLoc[1]
        X = []
        Y = []
        X2 = []
        Y2 = []
        time1 = 0
        time2 = 0
        while abs(row_fire - self.FE1[0]) > 0 or abs(col_fire - self.FE1[1]) > 0:
            time1 = time1 + 1 # ASSUMING 1 CELL TAKES 1 MINUTE TO TRAVEL
            if row_fire > self.FE1[0]:
                self.FE1[0] += 1  # ROW OF FIRE ENGINE
            elif row_fire < self.FE1[0]:
                self.FE1[0] -= 1
            else:
                if col_fire > self.FE1[1]:
                    self.FE1[1] += 1
                elif col_fire < self.FE1[1]:
                    self.FE1[1] -= 1
                else:
                    tmp = None
            X.append(self.FE1[1])
            Y.append(self.FE1[0])
            if time1 % 6 == 0: # This is just to control the number of samples
                if (row_fire - self.FE1[0]) > 0:
                    plt.plot(self.FE1[1],self.FE1[0],color='blue',marker=r'$\downarrow$',markersize=10)
                elif (row_fire - self.FE1[0]) < 0:
                    plt.plot(self.FE1[1],self.FE1[0],color='blue',marker=r'$\uparrow$',markersize=10)
                elif (col_fire - self.FE1[1]) > 0:
                    plt.plot(self.FE1[1],self.FE1[0],color='blue',marker=r'$\rightarrow$',markersize=10)
                else:
                    plt.plot(self.FE1[1],self.FE1[0],color='blue',marker=r'$\leftarrow$',markersize=10)
        
        while abs(row_fire - self.FE2[0]) > 0 or abs(col_fire - self.FE2[1]) > 0:
            time2 = time2 + 1 # ASSUMING 1 CELL TAKES 1 MINUTE TO TRAVEL
            if col_fire > self.FE2[1]:
                self.FE2[1] += 1
            elif col_fire < self.FE2[1]:
                self.FE2[1] -= 1
            else:
                if row_fire > self.FE2[0]:
                    self.FE2[0] += 1  # ROW OF FIRE ENGINE
                elif row_fire < self.FE2[0]:
                    self.FE2[0] -= 1
                else:
                    tmp = None
            
        
            
            X2.append(self.FE2[1])
            Y2.append(self.FE2[0])
            if time2 % 6 == 0: # This is just to control the number of samples
                if (col_fire - self.FE2[1]) > 0:
                    plt.plot(self.FE2[1],self.FE2[0],color='pink',marker=r'$\rightarrow$',markersize=10)
                elif (col_fire - self.FE2[1]) < 0:
                    plt.plot(self.FE2[1],self.FE2[0],color='pink',marker=r'$\leftarrow$',markersize=10)           
                elif (row_fire - self.FE2[0]) > 0:
                    plt.plot(self.FE2[1],self.FE2[0],color='pink',marker=r'$\downarrow$',markersize=10)
                else:
                    plt.plot(self.FE2[1],self.FE2[0],color='pink',marker=r'$\uparrow$',markersize=10)
                  
        return [time1,time2]
    
    
    # def StartSpraying(self, tankCap, flowRate):
    #     time = 0  
    #     step = 1
    #     timeToEmpty = tankCap/flowRate
    #     Units = F1.fireSize
    #     SlowRate = F1.ReductionRate 
    #     FinalUnit = Units - SlowRate*tankCap
    #     while tankCap > 0:
    #         time = time + step
    #         tankCap = tankCap - flowRate
    #         Units = Units - SlowRate*flowRate
    #         if tankCap > 0 and Units > 0:
    #             print('Time ' + str(time) + ' min' + ': Tank Capacity = ' + str(tankCap) + ' Gal' + ' Fire Size: ' + str(Units) + ' Units')
    #         else:
    #             break
    #     # print('At Time ' + str(timeToEmpty) + ' min, Tank Capacity = 0' + ' Fire Size = ' + str(FinalUnit) + 'Units')
    #     print('At Time ' + str(time) + ' min, Tank Capacity = ' + str(tankCap) + ' Fire Size = ' + str(Units) + 'Units')
                      
# F1 = Fire(1000,1)
# F1.printFireDescription()
FE1 = FireEngine()
FE1.printVehicleDescription()
#FE1.graphFireEngine(FE1.FE1[1], FE1.FE1[0])
FE1.goTo(c1.fuel)
#FE1.StartSpraying(FE1.tankCap,FE1.flowRate)

FE2 = FireEngine()
FE2.printVehicleDescription()
print(FE2.goTo(c1.fuel))
