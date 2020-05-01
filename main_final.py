#!/usr/bin/env python
# coding: utf-8

# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
# from SoS_Drone import drone
# from LandGeneration import LandGeneration


# In[13]:


class LandGeneration():
    '''
    LandGeneration Class creates Land Object by plotting cells of different colors, representing vegetations:
        1. Residential Areas are in White Squares [Value 5]
        2. Agricultural Lands are in Light Green Squares [Value 15]
        3. Forest Type 1 Areas are given in Green Squares [Value 25]
        4. Forest Type 2 Areas are given in Dark Olive Green [Value 35]
        5. Forest Type 3 Areas are given in Forest Green [Value 45]
    '''
    
    def __init__(self, LandSize):
        '''
        Instantiate attributes: LandSize is a list [row, col]
        '''
        self.ROW = LandSize[0]
        self.COL = LandSize[1]
        self.DATA = []
        self.GRID = []
        self.count_res = 0
        self.count_ag = 0
        self.count_ft1 = 0
        self.count_ft2 = 1
        
    def ResArea(self):
        '''
        Residential Area Size Determination. Randomly sized every time code is run
        Returns ranges of row and column
        
        '''
        row = self.ROW
        col = self.COL        
        # DEFINE THE SIZE OF THE RESIDENTIAL AREA FROM CENTER
        rand_per = random.randint(3,10)
        interval_row = int(row * rand_per/100)
        interval_col = int(col * rand_per/100)
        # RESIDENTIAL AREA
        if self.count_res % 2 == 0:
            rand1 = random.randint(10,30)
        else:
            rand1 = random.randint(70,90)
        row_res1 = int(row * rand1/100) # POSITION OF THE ROW CENTER
        col_res1 = int(col * (1-rand1/100)) # POSITION OF THE COLUMN CENTER
        city1_row= range(row_res1 - interval_row,row_res1 + interval_row) 
        city1_col = range(col_res1 - interval_col, col_res1 + interval_col)
        li = [city1_row, city1_col]
        self.count_res += 1
        return li
    
    def AgLand(self):
        '''
        Agricultural Land Size Determination. Randomnly sized every time code is run
        Returns ranges of row and column
        '''
        row = self.ROW
        col = self.COL
        rand_per2 = random.randint(5,15)
        interval_row2 = int(row * rand_per2/100)
        interval_col2 = int(col * rand_per2/100)
        if self.count_ag % 2 == 0:
            rand3 = random.randint(30,45)
        else:
            rand3 = random.randint(45,60)
        row_res3 = int(row * rand3/100) 
        col_res3 = int(col * (1-rand3/100))
        ag1_row= range(row_res3 - interval_row2,row_res3 + interval_row2)
        ag1_col = range(col_res3 - interval_col2, col_res3 + interval_col2)
        li = [ag1_row, ag1_col]
        self.count_ag += 1
        return li
    
    def ForestLand(self):
        '''
        Forest Areas Land Size Determination. Randomly sized and returns range of row and column
        '''
        row = self.ROW
        col = self.COL
        rand_per3 = random.randint(15,40)
        interval_row3 = int(row * rand_per3/100)
        interval_col3 = int(col * rand_per3/100)
        if self.count_ft1 % 2 == 0:
            rand4 = random.randint(5,45)
            row_res4 = int(row * rand4/100) 
            col_res4 = int(col * (1-rand4/100))
        else:
            rand4 = random.randint(65,95)
            row_res4 = int(row * rand4/100) 
            col_res4 = int(col * (1-rand4/100))
        
        ft1_row= range(row_res4 - interval_row3,row_res4 + interval_row3)
        ft1_col = range(col_res4 - interval_col3, col_res4 + interval_col3)
        li = [ft1_row, ft1_col]
        self.count_ft1 += 1
        return li
    
    
    def CreateLand(self, LI, typ):     
        '''
        Taking the sizes of each of the areas specified in the above functions,
        this function maps their sizes to the map. It returns a list of values in
        an array. However, it can only do one area at a time, so the next funcntion 
        CombineLand, combines all these map arrays
        
        '''
        self.DATA = []  # CLEAR THE DATA LIST SO THAT IT DOES NOT KEEP APPENDING TO ITSELF
        print("Size of " + str(typ) + ": " +  str(LI))
        Col = LI[0]
        Row = LI[1]
        
        data = self.DATA
        my_list = [45] * 100
        for r in range(self.ROW):
            row_ = []
            for c in range(self.COL):        
                if c in Col and r in Row and typ == "res":
                    row_.append(5)
                elif c in Col and r in Row and typ == "ag":
                    row_.append(15)
                elif c in Col and r in Row and typ == "1":
                    row_.append(25)
                elif c in Col and r in Row and typ == "2":
                    row_.append(35)
                else:
                    d = random.choice(my_list)
                    row_.append(d)
            data.append(row_)
        return data    
        
    def CombineLands(self, DAT):
        '''
        Combines all the maps into one array, which will be used to plot a map
        Returns this array to the graphing function
        '''
        self.GRID = []
        t = 0
        for r in range(self.ROW):
            row_ = []
            for c in range(self.COL):
                temp = []
                for t in range(len(DAT)):
                    temp.append(DAT[t][r][c])
                min_ = min(temp)
                #min_ = min(DAT[t][r][c],DAT[t+1][r][c],DAT[t+2][r][c])
                row_.append(min_)
            self.GRID.append(row_)    
        return self.GRID
    
    def GraphLand(self, data):
        '''
        Graphs all the land maps in one figure
        0-9: White for Residential Areas
        10-19: Lawngreen for Agriculture Lands
        20-29: Green for Forest Area 1
        30-39: Olive Green for Forest Area 2
        40-49: Forest Green for Forest Area 3
        50-59: Gray for newly ignited fire
        60-159: Red for Actual Fire
        160-169: Black for destroyed land
        '''
        cmap = colors.ListedColormap(['white','lawngreen','green','#556B2F','#228B22', '#C0C0C0', '#B22222', '#000000'])
        bounds = [0,10,20,30,40,50,60,160,170]
        # ([0,20,30],2) = [0,20] is one color and [20,30] is another color?
        norm = colors.BoundaryNorm(bounds,cmap.N)
        fig, ax = plt.subplots()
        ax.imshow(data,cmap=cmap,norm=norm)
        #ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(-.5, len(data[1]), 1), " ")
        #ax.get_xaxis().set_visible(False)
        ax.set_yticks(np.arange(-.5, len(data), 1)," ")
        #ax.get_yaxis().set_visible(False)
        return fig, ax 
    
    def UpdateFire_All (self, x, y, data, init_data, temp, humid, wind, vehicle):
        '''
        Takes previous data, initial data, weather, and firefighting vehicle inputs
        Employs UpdateFire function - see next - to update the neighboring cells if current cell is on fire 
        Returns new data 
        '''
        (data, init_data) = (data, init_data)
        (temp, humid, wind) = (temp, humid, wind)
        vehicle = vehicle
        
        if data[y][x] in range (60, 159) and (y in range(1, self.ROW-1) and x in range (1, self.COL-1)):
            data[y][x-1] = self.UpdateFire(data[y][x-1], init_data[y][x-1], temp, humid, wind, vehicle) 
            data[y][x+1] = self.UpdateFire(data[y][x+1], init_data[y][x+1], temp, humid, wind, vehicle) 
            data[y-1][x] = self.UpdateFire(data[y-1][x], init_data[y-1][x], temp, humid, wind, vehicle)
            data[y+1][x] = self.UpdateFire(data[y+1][x], init_data[y+1][x], temp, humid, wind, vehicle)
            data[y+1][x-1] = self.UpdateFire(data[y+1][x-1], init_data[y+1][x-1], temp, humid, wind, vehicle)
            data[y+1][x+1] = self.UpdateFire(data[y+1][x+1], init_data[y+1][x+1], temp, humid, wind, vehicle)
            data[y-1][x-1] = self.UpdateFire(data[y-1][x-1], init_data[y-1][x-1], temp, humid, wind, vehicle)
            data[y-1][x+1] = self.UpdateFire(data[y-1][x+1], init_data[y-1][x+1], temp, humid, wind, vehicle)
        return data
        
    
    def UpdateFire(self, cell, init_landID, temp, humid, wind, vehicle):
        '''
        Updates ID in one cell due to effects of initial land type, weather, firefighting vehicle 
        '''
        # Fire spread rate: Forest Area 3 > Forest Area 2 > Forest Area 1  
        update_rateres = 0.7
        update_rateagr = 0.8
        update_rate1 = 1
        update_rate2 = 1.2
        update_rate3 = 1.4
        
        
        # Effects of weather of fire spread 
        (temp, humid, wind) = (temp, humid, wind)
        if temp >= 30: 
            temp_add = temp*0.05
            
        if humid >= 70: 
            humid_add = -humid*0.01
        elif humid < 30: 
            humid_add = humid*0.05
        else: 
            humid_add = 0
            
        wind_add = wind*0.05
        
        # Effect of firefighting vehicle 
        vehicle = -vehicle*0.05 
        
        if init_landID in range (0, 9):        # Agriculture Area
            cell = max(cell, 50) + update_rateres + temp_add + humid_add + wind_add + vehicle
        elif init_landID in range (10, 19):    # Residential Area 
            cell = max(cell, 50) + update_rateagr + temp_add + humid_add + wind_add + vehicle
        elif init_landID in range (20, 29):    # Forest Area 1
            cell = max(cell, 50) + update_rate1 + temp_add + humid_add + wind_add + vehicle 
        elif init_landID in range (30, 39):    # Forest Area 2
            cell = max(cell, 50) + update_rate2 + temp_add + humid_add + wind_add + vehicle
        elif init_landID in range (40, 49):    # Forest Area 3 
            cell = max(cell, 50) + update_rate3 + temp_add + humid_add + wind_add + vehicle
            
        # CAN ADD SMOKE AND HEAT AS A FUNCTION OF CELL HERE AND RETURN THEIR VALUES 
        return cell 
    
    def FireMeasure(self, data): 
        fire_cells = []
        unit_cost = 500
        
        for y in range (self.ROW):
            for x in range (self.COL): 
                if data[y][x] > 50 and data[y][x] < 159:   # If a cell is on fire (new and old), add it to the list
                    fire_cells.append(data[y][x])
        fire_size = len(fire_cells)    # Number of cells on fire represents fire size 
        cost = fire_size * unit_cost 
        return fire_size, cost 


# In[14]:


class drone:
    batt_level = 100
    batt_drainrate = 1
    IR_radius = 5
    Visual_radius = 10
    IR_heat_trigger = 51
    Visual_heat_trigger = 61
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
#     def batt_drain(self):
#             self.batt_level=self.batt_level-self.batt_drainrate
#             print(self.batt_level)
            
#     #move to random adjacent cell
#     def moverandom(self):
#         randlist = [[0,1],[1,1],[1,0],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]] #possible movement, excluding [0,0] so it wont stay in the same grid
#         movement_step = random.choice(randlist) #get random direction from the list
#         self.xcell = self.xcell+movement_step[0] 
#         self.ycell = self.ycell+movement_step[1] 
        
#         #if x or y coordinate is not in the map range, random new movement
#         while self.xcell not in self.maprange or self.ycell not in self.maprange:
#             movement_step = random.choice(randlist)
#             self.xcell = self.xcell+movement_step[0]
#             self.ycell = self.ycell+movement_step[1]
#         self.batt_drain() # Drain battery after the move
                
    #instead of randomized movement, let's define a grid and allocate the detection to that drone alone
    def movepatternOne(self, xstart, ystart, xend, yend):
        ''' Moves one drone in a zig-zag pattern'''
        X = []
        Y = []
        xtemp = xstart
        movement_step = [-5, 5]
        timecounter = 0
#         while self.xcell > 1 and self.ycell > 1:
#             self.movetotarget(xstart, ystart)
#             X.append(self.xcell)
#             Y.append(self.ycell)
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
    
    
    
    
#     #move to specific target
#     def movetotarget(self,xtarget,ytarget):
#         #check x direction to target
#         if self.xcell < xtarget:
#             xdir = 1
#         elif self.xcell > xtarget:
#             xdir = -1
#         else:
#             xdir = 0
            
#         #check y direction to target
#         if self.ycell < ytarget:
#             ydir = 1
#         elif self.ycell > ytarget:
#             ydir = -1
#         else:
#             ydir = 0
        
#         #move toward x
#         self.xcell=self.xcell+xdir
        
#         #move toward y
#         self.ycell=self.ycell+ydir
#         self.batt_drain()
        
#         # #check if need to return to base
#         # self.check_return()
    
#     #check battery level        
#     def check_return(self):
#         batt_threshold = self.batt_drainrate*(abs(self.xorigin-self.xcell)+abs(self.yorigin-self.ycell))
#         if self.batt_level <= batt_threshold*self.safety_factor:
#             self.movetotarget(self.xorigin,self.yorigin)            
    
#     #read scan heat
#     def scan_heat(self,heatmap):
#         #preallocation the array
        
        
#         self.fire_location = [[99,99]]
        
        
#         #Identify search boundary so it wont spot outside map boundary
#         if (self.xcell-self.IR_radius) < 0:
#             IR_lower_x = 0
#         else:
#             IR_lower_x = self.xcell-self.IR_radius  
        
#         if (self.xcell+self.IR_radius) > 99:
#             IR_upper_x = 99
#         else:
#             IR_upper_x = self.xcell+self.IR_radius
            
#         if (self.ycell-self.IR_radius) < 0:
#             IR_lower_y = 0
#         else:
#             IR_lower_y = self.ycell-self.IR_radius  
        
#         if (self.ycell+self.IR_radius) > 99:
#             IR_upper_y = 99
#         else:
#             IR_upper_y = self.ycell+self.IR_radius
           
#         self.IR_range_x=np.arange(IR_lower_x,IR_upper_x)
#         self.IR_range_y=np.arange(IR_lower_y,IR_upper_y)
        
#         #read fire status in IR range
#         for x in self.IR_range_x:
#             for y in self.IR_range_y:
#                 if heatmap[x][y] >= self.IR_heat_trigger:
#                     print("Fire is detected by IR sensor at the coordinate" + "(" + str(x) + ", " + str(y))
#                     self.fire_location = np.append(self.fire_location,[[x,y]],axis = 0)
        
#         #Identify search boundart so it wont spot outside map boundary
        
#         if (self.xcell-self.Visual_radius) < 0:
#             Visual_lower_x = 0
#         else:
#             Visual_lower_x = self.xcell-self.Visual_radius  
        
#         if (self.xcell+self.Visual_radius) > 99:
#             Visual_upper_x = 99
#         else:
#             Visual_upper_x = self.xcell+self.Visual_radius
            
#         if (self.ycell-self.Visual_radius) < 0:
#             Visual_lower_y = 0
#         else:
#             Visual_lower_y = self.ycell-self.Visual_radius  
        
#         if (self.ycell+self.IR_radius) > 99:
#             Visual_upper_y = 99
#         else:
#             Visual_upper_y = self.ycell+self.Visual_radius
            
#         self.Visual_range_x=np.arange(Visual_lower_x,Visual_upper_x)
#         self.Visual_range_y=np.arange(Visual_lower_y,Visual_upper_y)
        
#         #read smoke status in visual range
#         for x in self.Visual_range_x:
#             for y in self.Visual_range_y:
#                 if heatmap[x][y] >= self.Visual_heat_trigger:
#                     print("Fire is detected by smoke at the coordinate" + "(" + str(x) + ", " + str(y))
#                     self.fire_location = np.append(self.fire_location,[[x,y]],axis = 0)
#         self.fire_location = np.delete(self.fire_location, np.where(self.fire_location == [999,999]),0)
#         return np.unique(self.fire_location, axis = 0)
    


# In[17]:


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




