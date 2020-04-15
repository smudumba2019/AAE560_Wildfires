# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:46:10 2020

@author: Sai V. Mudumba
"""

# IMPORT THESE PYTHON PACKAGES
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random

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
        '''
        cmap = colors.ListedColormap(['white','lawngreen','green','#556B2F','#228B22'])
        bounds = [0,10,20,30,40,50]
        # ([0,20,30],2) = [0,20] is one color and [20,30] is another color?
        norm = colors.BoundaryNorm(bounds,cmap.N)
        fig, ax = plt.subplots()
        ax.imshow(data,cmap=cmap,norm=norm)
        #ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=1)
        ax.set_xticks(np.arange(-.5, len(data[1]), 1), " ")
        #ax.get_xaxis().set_visible(False)
        ax.set_yticks(np.arange(-.5, len(data), 1)," ")
        #ax.get_yaxis().set_visible(False)
        plt.show()


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
AA = Land1.CombineLands([C1, C2, C3, C4, C5, C6, C7, C8])
# GRAPH THE TOTAL LAND
Land1.GraphLand(AA)
