#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
NOTE: in "drone" class, change the following: 
    IR_heat_trigger = 51
    Visual_heat_trigger = 61
    
And make sure:
    IR_radius = 5
    Visual_radius = 10
'''

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

time = 50
drone_list = []
eng_list = []
vehicle = 0 
i = 1   # this is for plotting drones

for t in range (0, time):
    print(t)
    
    
    
    #INITIALIZE FIRE
    temp = 40   # [Celsius degree]
    humid = 50  # [percent]
    wind = 20   # [m/s]
    
    if t == 0: 
    # Start fire 
        rfr = random.randint(0,Land1.ROW-1)
        rfc = random.randint(0,Land1.COL-1)
        if AA[rfr][rfc] > 20 and AA[rfr][rfc] < 50: # Only ignite on forest
            AA[rfr][rfc] = 65
   

    
    # UPDATE FIRE, DRONES
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
    size, cost = Land1.FireMeasure(AA)
    print('The size of fire is', size, 'cells. The cost associated is', cost, 'USD.')
    
    
    
    
    # UPDATE DRONES

    # Visual camera has broader scanning range, but higher trigger value
    # IR camera has smaller scanning range, but lower trigger value
    
    if i < len(X1): 
        if Y1[i] < 89 and X1[i] < 89: 
            for p1 in range(Y1[i]-D1.Visual_radius,Y1[i]+D1.Visual_radius):
                for q1 in range(X1[i]-D1.Visual_radius,X1[i]+D1.Visual_radius):                            
                    if AA[p1][q1] >= D1.Visual_heat_trigger:
                        X1[i] = rfc
                        Y1[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by visual camera")
                        print("At location: x =" + str(q1) + ", y =" + str(p1))
                        
            for r1 in range(Y1[i]-D1.IR_radius,Y1[i]+D1.IR_radius):
                for s1 in range(X1[i]-D1.IR_radius,X1[i]+D1.IR_radius):                            
                    if AA[r1][s1] >= D1.IR_heat_trigger:
                        X1[i] = rfc
                        Y1[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by IR camera")
                        print("At location: x =" + str(s1) + ", y =" + str(r1))
                        
    if i < len(X2):
        if Y2[i] < 100 and X2[i] < 89: 
            for p2 in range(Y2[i]-D1.Visual_radius,Y2[i]+D1.Visual_radius):
                for q2 in range(X2[i]-D1.Visual_radius,X2[i]+D1.Visual_radius):                            
                    if AA[p2][q2] >= D1.Visual_heat_trigger:
                        X1[i] = rfc
                        Y1[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by visual camera")
                        print("At location: x =" + str(q2) + ", y =" + str(p2))
                        
            for r2 in range(Y2[i]-D1.IR_radius,Y2[i]+D1.IR_radius):
                for s2 in range(X2[i]-D1.IR_radius,X2[i]+D1.IR_radius):                            
                    if AA[r2][s2] >= D1.IR_heat_trigger:
                        X2[i] = rfc
                        Y2[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by IR camera")
                        print("At location: x =" + str(s2) + ", y =" + str(r2))
                        
    if i < len(X3):
        if Y3[i] < 89 and X3[i] < 89:
            for p3 in range(Y3[i]-D1.Visual_radius,Y3[i]+D1.Visual_radius):
                for q3 in range(X3[i]-D1.Visual_radius,X3[i]+D1.Visual_radius):                            
                    if AA[p3][q3] >= D1.Visual_heat_trigger:
                        X3[i] = rfc
                        Y3[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by visual camera")
                        print("At location: x =" + str(q3) + ", y =" + str(p3))
                        
            for r3 in range(Y3[i]-D1.IR_radius,Y3[i]+D1.IR_radius):
                for s3 in range(X3[i]-D1.IR_radius,X3[i]+D1.IR_radius):                            
                    if AA[r3][s3] >= D1.IR_heat_trigger:
                        X3[i] = rfc
                        Y3[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by IR camera")
                        print("At location: x =" + str(s3) + ", y =" + str(r3))
        
    if i < len(X4):                
        if Y4[i] < 100 and X4[i] < 89: 
            for p4 in range(Y4[i]-D1.Visual_radius,Y4[i]+D1.Visual_radius):
                for q4 in range(X4[i]-D1.Visual_radius,X4[i]+D1.Visual_radius):                            
                    if AA[p4][q4] >= D1.Visual_heat_trigger:
                        X4[i] = rfc
                        Y4[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by visual camera")
                        print("At location: x =" + str(q4) + ", y =" + str(p4))
                        
            for r4 in range(Y4[i]-D1.IR_radius,Y4[i]+D1.IR_radius):
                for s4 in range(X4[i]-D1.IR_radius,X4[i]+D1.IR_radius):                            
                    if AA[r4][s4] >= D1.IR_heat_trigger:
                        X4[i] = rfc
                        Y4[i] = rfr
                        print("Detected at time, t = " + str(t) + " min by IR camera")
                        print("At location: x =" + str(s4) + ", y =" + str(r4))
    print(i)

    
    # PLOT LAND, FIRE, AND DRONES
    
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




