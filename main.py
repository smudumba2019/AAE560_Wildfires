#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random

# Import classes (Land-Fire, Drones, Fire Engines) from files  
# from Land_Fire import *
# from Drone import *
# from Fire_Engine import *


# In[ ]:


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
Need to: Create markers for fire stations using locations Station 1 (x1, y1), Station 2 (x2, y2); 
For example
'''
x1 = 20
y1 = 30
x2 = 50
y2 = 80



# DYNAMICS
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
vehicle = np.zeros((Land1.ROW, Land1.COL)) 

for t in range (0, time):
    temp = 40   # [Celsius degree]
    humid = 50  # [percent]
    wind = 20   # [m/s]
  
    '''INITIALIZE FIRE, DRONES, FIRE ENGINES'''
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
    dr = drone(dr_x, dr_y, Land1.COL, Land1.ROW) # Rawin, mapsize is the Land1.ROW-Land1.COL pair
    drone_list.append(dr) 
        
    # Put fire engines at fire stations
    eng_num = 2
    for i in range (eng_num):
        # Even-indexed fire engines go to Station 2, odd-indexed ones go to Station 1
        if i in range (0, eng_num, 2):
            (eng_x, eng_y) = (x2, y2)
            station_loc = (x2,y2)
        if i in range (1, eng_num, 2): 
            (eng_x, eng_y) = (x1, y1)
            station_loc = (x1, y1)
    eng = FireEngine(eng_x, eng_y, [Land1.COL, Land1.ROW], station_loc)
    eng_list.append(eng) 
    
    
    
    
    
    '''UPDATE FIRE, DRONES, FIRE ENGINES'''
    
    # FIRE 
    '''
    In order to have the fire to propagate radially, 4 directions of looping are needed.
    Otherwise, fire would only propagates towards the one direction chosen.
        e.g. Direction 1 (below) only: fire would spread from the initial fire, 
        towards the corner of increasing row and column indexes
    4 directions of looping are done alternately, i.e. 1-2-3-4-1-2-3-4-... 
    For each direction, UpdateFire_All function is called to update the data.  
    '''
    
    if t in range (1, time, 4):
    # Update fire in direction 1
        for y in range (0,Land1.ROW-1):
            for x in range (0, Land1.COL-1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle[y][x]) 
                
    elif t in range (2, time, 4): 
    # Update fire in direction 2
        for y in range (Land1.ROW-1, 0, -1):
            for x in range (0, Land1.COL-1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle[y][x])
                
    elif t in range (3, time, 4):
    # Update fire in direction 3
        for y in range (Land1.ROW-1, 0, -1):
            for x in range (Land1.COL-1, 0, -1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle[y][x])
                
    else: 
    # Update fire in direction 4
        for y in range (0,Land1.ROW-1):
            for x in range (Land1.COL-1, 0, -1):
                AA = Land1.UpdateFire_All(x, y, AA, init_AA, temp, humid, wind, vehicle[y][x])
    
    # Size of fire and associated cost 
    size, cost = Land1.FireMeasure(AA)
    print('The size of fire is', size, 'cells. The cost associated is', cost, 'USD.')
    
    
    
    
    # DRONES
    '''
    PASTE RAWIN'S VERSION OF CODE HERE
    Drones scan for heat and smoke
    If fire detected, move towards fire and send signal; otherwise, move randomly
    
    '''
      
    vehicle = np.zeros((Land1.ROW, Land1.COL)) # Reset to make a new vehicle matrix (as the fire engine moves)
    
    # FIRE ENGINES
    '''
    PASTE SAI'S VERSION OF CODE HERE
    Fire engines receive fire signal (yes/no, target location) from drones
    If there's a fire, move towards fire till arriving at target location; otherwise, on standby at station 
    At fire location, if there's a fire, does firefighting; otherwise, stop (disappear forever) 
    If energy drains, pause for energy to come back
    '''

    # Plot land 
    fig, ax = Land1.GraphLand(AA)
    '''
    Need to: Add markers for the fire stations, drones, and fire engines here, 
    so that they can be plotted on top of the land
    '''
    plt.plot()
    

