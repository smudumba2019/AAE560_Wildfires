# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 21:57:53 2020

@author: rpinkoh
"""
import random
import numpy as np

class drone:
    batt_level = 100
    batt_drainrate = 1
    IR_radius = 20
    Visual_radius = 40
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
        self.mapsize=mapsize
        self.maprange=np.arange(0,mapsize)

    
    #drain battery from movement and IR/visual cam usage
    def batt_drain(self):
            self.batt_level=self.batt_level-self.batt_drainrate

    #move to random adjacent cell
    def moverandom(self):
        randlist = [[0,1],[1,1],[1,0],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]] #possible movement, excluding [0,0] so it wont stay in the same grid
        movement_step = random.choice(randlist)
        self.xcell = self.xcell+movement_step[0][0]
        self.ycell = self.ycell+movement_step[0][1]
        
        #if x or y coordinate is not in the map range, random new movement
        while self.xcell not in self.maprange or self.ycell not in self.maprange:
            movement_step = random.choice(randlist)
            self.xcell = self.xcell+movement_step[0][0]
            self.ycell = self.ycell+movement_step[0][1]
        self.batt_drain

        

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
        while self.xcell != xtarget:
            self.xcell=self.xcell+xdir
            self.batt_drain
        
        #move toward y
        while self.ycell != ytarget:
            self.ycell=self.ycell+ydir
            self.batt_drain
    
    #check battery level        
    def check_return(self):
        batt_threshold = self.batt_drainrate*(abs(self.xorigin-self.xcell)+abs(self.yorigin-self.ycell))
        if self.batt_level <= batt_threshold*self.safety_factor:
            self.movetotarget(self.xorigin,self.yorigin)            
    
    #read scan heat
    def scan_heat(self,heatmap):
        #read fire status in IR range
        self.IR_range_x=np.arange(self.xcell-self.IR_radius,self.xcell+self.IR_radius)
        self.IR_range_y=np.arange(self.ycell-self.IR_radius,self.ycell+self.IR_radius)
        for x in self.IR_range_x:
            for y in self.IR_range_y:
                if heatmap[x][y] >= self.IR_heat_trigger:
                    print("Fire is detected by IR sensor at the coordinate [" + x + "," + y + "]")
                    np.append(self.fire_location,[x,y],axis = 0)
        #read smoke status in visual range
        self.Visual_range_x=np.arange(self.xcell-self.Visual_radius,self.xcell+self.Visual_radius)
        self.Visual_range_y=np.arange(self.ycell-self.Visual_radius,self.ycell+self.Visual_radius)
        for x in self.Visual_range_x:
            for y in self.Visual_range_y:
                if heatmap[x][y] >= self.Visual_heat_trigger:
                    print("Fire is detected by smoke at the coordinate [" + x + "," + y + "]")        
                    np.append(self.fire_location,[x,y],axis = 0)
        return np.unique(self.fire_location)
        #send alarm


    

