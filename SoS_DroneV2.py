# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 21:57:53 2020
@author: rpinkoh
"""
import random
import numpy as np
import matplotlib.pyplot as plt

class drone:
    batt_level = 100
    batt_drainrate = 1
    IR_radius = 5
    Visual_radius = 10
    IR_heat_trigger = 20
    Visual_heat_trigger = 60
    safety_factor = 1.02
    fire_location = []
    
    def __init__(self,xcell,ycell,mapsize):
        #define current location
        self.xcell=xcell
        self.ycell=ycell
        #define origin
        self.xorigin=xcell
        self.yorigin=ycell
        #Define map size and boundary
        self.mapsize=mapsize
        self.maprange=np.arange(0,mapsize)
                            
            
    #drain battery from movement and IR/visual cam usage
    def batt_drain(self):
            self.batt_level=self.batt_level-self.batt_drainrate
            print(self.batt_level)
            
    #move to random adjacent cell
    def moverandom(self):
        randlist = [[0,1],[1,1],[1,0],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]] #possible movement, excluding [0,0] so it wont stay in the same grid
        movement_step = random.choice(randlist) #get random direction from the list
        self.xcell = self.xcell+movement_step[0] 
        self.ycell = self.ycell+movement_step[1] 
        
        #if x or y coordinate is not in the map range, random new movement
        while self.xcell not in self.maprange or self.ycell not in self.maprange:
            movement_step = random.choice(randlist)
            self.xcell = self.xcell+movement_step[0]
            self.ycell = self.ycell+movement_step[1]
        self.batt_drain() # Drain battery after the move
                
    #instead of randomized movement, let's define a grid and allocate the detection to that drone alone
    def movepatternOne(self, xstart, ystart, xend, yend):
        ''' Moves one drone in a zig-zag pattern'''
        X = []
        Y = []
        xtemp = xstart
        movement_step = [-5, 5]
        timecounter = 0
        # while self.xcell > 1 and self.ycell > 1:
        #     self.movetotarget(xstart, ystart)
        #     X.append(self.xcell)
        #     Y.append(self.ycell)
        for y in range(ystart,yend,10):
            for x in range(xstart,xend,5):
                if y % 20 == 10:
                    xtemp = xtemp + movement_step[1]
                    X.append(xtemp)
                    Y.append(y)
                    timecounter += 1
                else:
                    xtemp = xtemp + movement_step[0]
                    X.append(xtemp)
                    Y.append(y)
                    timecounter += 1
        return X,Y, timecounter
    
    
    
    
    #move to specific target
    def movetotarget(self,xtarget,ytarget):
        #check x direction to target
        if self.xcell < xtarget:
            xdir = 1
        elif self.xcell > xtarget:
            xdir = -1
        else:
            xdir = 0
            
        #check y direction to target
        if self.ycell < ytarget:
            ydir = 1
        elif self.ycell > ytarget:
            ydir = -1
        else:
            ydir = 0
        
        #move toward x
        self.xcell=self.xcell+xdir
        
        #move toward y
        self.ycell=self.ycell+ydir
        self.batt_drain()
        
        # #check if need to return to base
        # self.check_return()
    
    #check battery level        
    def check_return(self):
        batt_threshold = self.batt_drainrate*(abs(self.xorigin-self.xcell)+abs(self.yorigin-self.ycell))
        if self.batt_level <= batt_threshold*self.safety_factor:
            self.movetotarget(self.xorigin,self.yorigin)            
    
    #read scan heat
    def scan_heat(self,heatmap):
        #preallocation the array
        
        
        self.fire_location = [[99,99]]
        
        
        #Identify search boundary so it wont spot outside map boundary
        if (self.xcell-self.IR_radius) < 0:
            IR_lower_x = 0
        else:
            IR_lower_x = self.xcell-self.IR_radius  
        
        if (self.xcell+self.IR_radius) > 99:
            IR_upper_x = 99
        else:
            IR_upper_x = self.xcell+self.IR_radius
            
        if (self.ycell-self.IR_radius) < 0:
            IR_lower_y = 0
        else:
            IR_lower_y = self.ycell-self.IR_radius  
        
        if (self.ycell+self.IR_radius) > 99:
            IR_upper_y = 99
        else:
            IR_upper_y = self.ycell+self.IR_radius
           
        self.IR_range_x=np.arange(IR_lower_x,IR_upper_x)
        self.IR_range_y=np.arange(IR_lower_y,IR_upper_y)
        
        #read fire status in IR range
        for x in self.IR_range_x:
            for y in self.IR_range_y:
                if heatmap[x][y] >= self.IR_heat_trigger:
                    print("Fire is detected by IR sensor at the coordinate" + "(" + str(x) + ", " + str(y))
                    self.fire_location = np.append(self.fire_location,[[x,y]],axis = 0)
        
        #Identify search boundart so it wont spot outside map boundary
        
        if (self.xcell-self.Visual_radius) < 0:
            Visual_lower_x = 0
        else:
            Visual_lower_x = self.xcell-self.Visual_radius  
        
        if (self.xcell+self.Visual_radius) > 99:
            Visual_upper_x = 99
        else:
            Visual_upper_x = self.xcell+self.Visual_radius
            
        if (self.ycell-self.Visual_radius) < 0:
            Visual_lower_y = 0
        else:
            Visual_lower_y = self.ycell-self.Visual_radius  
        
        if (self.ycell+self.IR_radius) > 99:
            Visual_upper_y = 99
        else:
            Visual_upper_y = self.ycell+self.Visual_radius
            
        self.Visual_range_x=np.arange(Visual_lower_x,Visual_upper_x)
        self.Visual_range_y=np.arange(Visual_lower_y,Visual_upper_y)
        
        #read smoke status in visual range
        for x in self.Visual_range_x:
            for y in self.Visual_range_y:
                if heatmap[x][y] >= self.Visual_heat_trigger:
                    print("Fire is detected by smoke at the coordinate" + "(" + str(x) + ", " + str(y))
                    self.fire_location = np.append(self.fire_location,[[x,y]],axis = 0)
        self.fire_location = np.delete(self.fire_location, np.where(self.fire_location == [999,999]),0)
        return np.unique(self.fire_location, axis = 0)
        #send fire location
    

# D1 = drone(50,50,100)

# # First drone
# [X1,Y1, timecounter1] = D1.movepatternOne(0,10,50,60)
# # Second Drone
# # [X2,Y2, timecounter2] = D1.movepatternOne(50,60,100,100)
# # # Third Drone
# # [X3,Y3, timecounter3] = D1.movepatternOne(0,60,50,100)
# # # Fourth Drone
# # [X4,Y4, timecounter4] = D1.movepatternOne(50,10,100,60)
# for i in range(1,len(X1)):
#     plt.plot(X1[0:i],Y1[0:i], 'b')
#     # plt.plot(X2[0:i],Y2[0:i], 'b')
#     # plt.plot(X3[0:i],Y3[0:i], 'b')
#     # plt.plot(X4[0:i],Y4[0:i], 'b')
    
#     circle1 = plt.Circle((X1[i],Y1[i]), D1.Visual_radius, color='y', alpha=0.5)
#     cl = plt.subplot()
#     cl.add_artist(circle1)
#     circle2 = plt.Circle((X1[i],Y1[i]), D1.IR_radius, color='r', alpha=0.5)
#     cl.add_artist(circle2)
#     plt.xlim(0,100)
#     plt.ylim(0,100)
#     plt.show()
