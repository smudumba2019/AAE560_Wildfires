#!/usr/bin/env python
# coding: utf-8

# In[8]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
from SoS_Drone import drone
from LandGeneration import LandGeneration


# In[9]:




# In[10]:


# GENERATE LAND BOUNDARIES        
Land1 = LandGeneration([100,100])
# GENERATE RESIDENTIAL SIZE
Res1 = Land1.ResArea()
Res2 = Land1.ResArea()
# GENERATE AGRICULTURAL SIZE
Ag1 = Land1.AgLand()
Ag2 = Land1.AgLand()
# GENERATE TYPE 1 FOREST SIZE
Ft11 = Land1.ForestLand() 
Ft12 = Land1.ForestLand()
# GENERATE TYPE 2 FOREST SIZE
Ft21 = Land1.ForestLand()
Ft22 = Land1.ForestLand()
# CREATE THE LANDS 
C1 = Land1.CreateLand(Res1,"res")
C2 = Land1.CreateLand(Res2,"res")
C3 = Land1.CreateLand(Ag1,"ag")
C4 = Land1.CreateLand(Ag2,"ag")
C5 = Land1.CreateLand(Ft11, "1")
C6 = Land1.CreateLand(Ft12, "1")
C7 = Land1.CreateLand(Ft21, "2")
C8 = Land1.CreateLand(Ft22, "2")
# COMBINE THE LANDS INTO ONE ARRAY
AA = Land1.CombineLands([C1, C2, C3, C4, C5, C6, C7, C8])       # Land matrix used to update and plot
init_AA = Land1.CombineLands([C1, C2, C3, C4, C5, C6, C7, C8])  # Land matrix unchanged, used for reference 

# CREATE FIRE STATIONS 
'''
Create markers for fire stations using locations Station 1 (x1, y1), Station 2 (x2, y2); 
For example
'''
x1 = 20
y1 = 30
x2 = 50
y2 = 80

'''
This part loops through each time step from 0 to (time-1)
t = 0: fire starts, drones and fire engines are at fire stations 
t > 0: fire propagates, 
       drones start surveiling and send signal when sensing fire, 
       engines on stand-by and move when receiving fire signal from drones 
'''

time = 50
drone_list = []
eng_list = []
vehicle = 0 

for t in range (0, time):
    temp = 40   # [Celsius degree]
    humid = 50  # [percent]
    wind = 20   # [m/s]
    
  
    #'''INITIALIZE FIRE, DRONES, FIRE ENGINES'''
    if t == 0: 
    
    # Start fire 
        rfr = random.randint(0,Land1.ROW-1)
        rfc = random.randint(0,Land1.COL-1)
        if AA[rfr][rfc] > 20 and AA[rfr][rfc] < 50: # Only ignite on forest
            AA[rfr][rfc] = 65
    
    # Put drones at fire stations
        drone_num = 3 
        for i in range (drone_num):
            # Even-indexed drones go to Station 2, odd-indexed drones go to Station 1
            if i in range (0, drone_num, 2):
                (dr_x, dr_y) = (x2, y2)
            if i in range (1, drone_num, 2): 
                (dr_x, dr_y) = (x1, y1)
            dr = drone(dr_x, dr_y, Land1.COL) # Rawin, mapsize is the Land1.ROW-Land1.COL pair
            drone_list.append(dr) 
        
    # Put fire engines at fire stations
        # eng_num = 2
        # for i in range (eng_num):
        # # Even-indexed fire engines go to Station 2, odd-indexed ones go to Station 1
        #     if i in range (0, eng_num, 2):
        #         (eng_x, eng_y) = (x2, y2)
        #     if i in range (1, eng_num, 2): 
        #         (eng_x, eng_y) = (x1, y1)
        #     eng = FireEngine(eng_x, eng_y, Land1.COL, Land1.ROW) 
        #     eng_list.append(eng) 
    
    
    
    #'''UPDATE FIRE, DRONES, FIRE ENGINES'''
    
    # FIRE 
    #'''
    #In order to have the fire to propagate radially, 4 directions of looping are needed.
    #Otherwise, fire would only propagates towards the one direction chosen.
    #    e.g. Direction 1 (below) only: fire would spread from the initial fire, 
    #    towards the corner of increasing row and column indexes
    #4 directions of looping are done alternately, i.e. 1-2-3-4-1-2-3-4-... 
    #For each direction, UpdateFire_All function is called to update the data.  
    #'''
    
    elif t in range (1, time, 4):
    # Update fire in direction 1
        for y in range (0,Land1.ROW-1):
            for x in range (0, Land1.COL-1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle) 
                
    elif t in range (2, time, 4): 
    # Update fire in direction 2
        for y in range (Land1.ROW-1, 0, -1):
            for x in range (0, Land1.COL-1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle)
                
    elif t in range (3, time, 4):
    # Update fire in direction 3
        for y in range (Land1.ROW-1, 0, -1):
            for x in range (Land1.COL-1, 0, -1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle)
                
    else: 
    # Update fire in direction 4
        for y in range (0,Land1.ROW-1):
            for x in range (Land1.COL-1, 0, -1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle)
    
    # Size of fire and associated cost 
    # size, cost = Land1.FireMeasure(AA)
    # print('The size of fire is', size, 'cells. The cost associated is', cost, 'USD.')
    
    # DRONES
    '''
    Drones scan for heat and smoke
    If fire detected, move towards fire and send signal; otherwise, move randomly
    '''
    for i in range (drone_num):
        fire_location = drone_list[i].scan_heat(AA) # Can replace with heat_AA (matrix of heat associated with AA) or AA itself is ok
        fire_distance= []
        
        if len(fire_location) > 1: # If fire detected (First two elements are both None, used for array preallocation): 
            
            for j in range (0,len(fire_location)-2):
                dist = abs(drone_list[i].xcell-fire_location[j+1][0]) + abs(drone_list[i].ycell-fire_location[j+1][1])
                fire_distance = np.append(fire_distance,dist)
            min_dist_loc = np.where(fire_distance == np.amin(fire_distance))
            xtarget = fire_location[j+1][0]
            ytarget = fire_location[j+1][1]

            drone_list[i].movetotarget(xtarget, ytarget)

        else: 
            drone_list[i].moverandom()
    print("time is")
    print(t)
    '''
    Create markers for drones, using their locations
    '''
    
    # FIRE ENGINES
    '''
    Fire engines receive fire signal (yes/no, target location) from drones
    If there's a fire, move towards fire till arriving at target location; otherwise, on standby at station 
    At fire location, if there's a fire, does firefighting; otherwise, stop (disappear forever) 
    If energy drains, pause for energy to come back
    '''
    
    # for i in range (eng_num): 
    #     energyfull = eng_list[i].energy_check() 
    #     '''This function compares current energy (of firefighters) with the limit, return energyfull = True or False'''
    #     waterfull = eng_list[i].water_check()
    #     '''This function compares current energy (of firefighters) with 0, return waterfull = True or False'''
    #     dist = eng_list[i].dist_calc(xtarget, ytarget) 
    #     '''This function calc & return the distance between a fire engine location and the target point identified by drone'''
        
    #     if energyfull == False:
    #         speed = 0 
    #         eng_list[i].energy_gain()
    #         '''This function adds a certain amount of energy to its current energy level'''
    #         vehicle = 0 # a parameter to pass into the FireCell in the beginning
    #     else:
    #         if fire == 0: # If there is no fire, return to station
    #             eng_list[i].return() 
    #             '''This function moves the fire engine towards its initial fire station (move() func with station location as target)'''
    #             vehicle = 0 
    #         elif fire == 1 and dist > 0: # If there is a fire and the engine is not at the fire, move towards fire 
    #             eng.list[i].move(xtarget, ytarget)
    #             '''This function moves the fire engine towards any target location passed in
    #             This needs the engine's current location, dist_calc() func, a fixed speed. For example: 
    #             speed = 5 
    #             if dist > speed: 
    #                 speed = speed
    #             else: 
    #                 speed = dist 
                
    #             Say, dist = 23 initially, the engine would move 5-5-5-5-3 to make sure it stops at the right cell 
    #             '''
    #             vehicle = 0 
    #         else: # If there is a fire and the engine arrived, no move + use energy and water
    #             eng_list[i].energy_drain()
    #             '''This function subtracts a certain amount of (firefighters') energy from the current energy level'''
    #             eng_list[i].water_drain()
    #             '''This function subtracts a certain amount of water from the current water level'''
    #             vehicle = 30             
    #     '''
    #     Create markers for fire engines, using their locations
    #     '''
    
    # Plot land 
    fig, ax = Land1.GraphLand(AA)
    plt.plot()
    


# In[ ]:




