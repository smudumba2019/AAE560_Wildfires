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


D1 = drone(50,50,100)

# First drone
[X1,Y1, timecounter1] = D1.movepatternOne(0,10,50,60)
# Second Drone
[X2,Y2, timecounter2] = D1.movepatternOne(50,50,100,100)
# Third Drone
[X3,Y3, timecounter3] = D1.movepatternOne(0,50,50,100)
# Fourth Drone
[X4,Y4, timecounter4] = D1.movepatternOne(50,10,100,60)



# '''
# This part loops through each time step from 0 to (time-1)
# t = 0: fire starts, drones and fire engines are at fire stations 
# t > 0: fire propagates, 
#        drones start surveiling and send signal when sensing fire, 
#        engines on stand-by and move when receiving fire signal from drones 
# '''

time = 100
drone_list = []
eng_list = []
vehicle = 0 
i = 1   # this is for plotting drones

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
    If fire detected, move towards fire and send signal; otherwise, move
    '''
    if i < len(X1): 
        if Y1[i] < 89 and X1[i] < 89: 
            for p1 in range(Y1[i]-10,Y1[i]+10):
                for q1 in range(X1[i]-10,X1[i]+10):                            
                    if AA[p1][q1] >= 50:
                        X1[i] = rfc
                        Y1[i] = rfr
                        print("Detected at time, t = " + str(t) + " min")
                        print("At location: " + str(X1[i]) + ", " + str(Y1[i]))
    if i < len(X2):
        if Y2[i] < 100 and X2[i] < 89: 
            for p2 in range(Y2[i]-10,Y2[i]+10):
                for q2 in range(X2[i]-10,X2[i]+10):        
                    if AA[p2][q2] >= 50:
                        X2[i] = rfc
                        Y2[i] = rfr
                        print("Detected at time, t = " + str(t) + " min")
                        print("At location: " + str(X2[i]) + ", " + str(Y2[i]))
    if i < len(X3):
        if Y3[i] < 89 and X3[i] < 89:
            for p3 in range(Y3[i]-10,Y3[i]+10):
                for q3 in range(X1[i]-10,X1[i]+10):                            
                    if AA[p3][q3] >= 50:
                        X3[i] = rfc
                        Y3[i] = rfr
                        print("Detected at time, t = " + str(t) + " min")
                        print("At location: " + str(X3[i]) + ", " + str(Y3[i]))
        
    if i < len(X4):                
        if Y4[i] < 100 and X4[i] < 89: 
            for p4 in range(Y4[i]-10,Y4[i]+10):
                for q4 in range(X4[i]-10,X4[i]+10):                
                    if AA[p4][q4] >= 50:
                        X4[i] = rfc
                        Y4[i] = rfr
                        print("Detected at time, t = " + str(t) + " min")
                        print("At location: " + str(X4[i]) + ", " + str(Y4[i]))
    print(i)
    
    '''
    Create markers for drones, using their locations
     '''
    

    print(t)
# Plot land 
    fig, ax = Land1.GraphLand(AA)
    if i < len(X1):
        plt.plot(X1[0:i],Y1[0:i], 'b')
        circle1 = plt.Circle((X1[i],Y1[i]), D1.Visual_radius, color='y', alpha=0.75)
        ax.add_artist(circle1)
        circle2 = plt.Circle((X1[i],Y1[i]), D1.IR_radius, color='r', alpha=0.75)
        ax.add_artist(circle2)
        
        plt.plot(X2[0:i],Y2[0:i], 'b')
        circle1 = plt.Circle((X2[i],Y2[i]), D1.Visual_radius, color='y', alpha=0.75)
        ax.add_artist(circle1)
        circle2 = plt.Circle((X2[i],Y2[i]), D1.IR_radius, color='r', alpha=0.75)
        ax.add_artist(circle2)
        
        plt.plot(X3[0:i],Y3[0:i], 'b')
        circle1 = plt.Circle((X3[i],Y3[i]), D1.Visual_radius, color='y', alpha=0.75)
        ax.add_artist(circle1)
        circle2 = plt.Circle((X3[i],Y3[i]), D1.IR_radius, color='r', alpha=0.75)
        ax.add_artist(circle2)
        
        plt.plot(X4[0:i],Y4[0:i], 'b')
        circle1 = plt.Circle((X4[i],Y4[i]), D1.Visual_radius, color='y', alpha=0.75)
        ax.add_artist(circle1)
        circle2 = plt.Circle((X4[i],Y4[i]), D1.IR_radius, color='r', alpha=0.75)
        ax.add_artist(circle2)
        
        plt.xlim(0,100)
        plt.ylim(0,100)
        plt.show()
        i += 1
    else:
        i += 1
        plt.show()



# In[ ]: