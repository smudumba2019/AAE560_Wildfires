# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 18:33:06 2020

@author: Sai V. Mudumba
"""

import numpy as np
#matplotlib inline
import matplotlib.pyplot as plt
import random
from LandGeneration import *

class FireCell():

    def __init__(self, prev_fire_score, prev_neighbor_score, vehicle_cap, spark, t):
        fuel = np.array(AA, dtype='f')   # matrix of vegetation, float type 
        self.fuel = self.StartFire()  # index vegetation type 
        
        self.ign_veg = 0.5
        self.ign_humid = 0.5
        self.ign_temp = 0.5

        self.spr_veg = 0.5
        self.spr_humid = 0.5
        self.spr_temp = 0.5
        self.spr_wind = 0.5
        
        self.humid = 90      # [percent]
        self.temp = 40       # [Celsius degree] 
        self.wind = 30       # [m/s]
        self.ign_thres = 80  # from this value and above, high potential of fire ignition

        self.intensify_rate = 0.05  # fire score increases by 5% of its own score
        self.spread_rate = 0.02     # fire score increases by 2% of total score of neighbors
        self.vehicle_eff = 0.2      # fire score decreases by 50% of vehicle capacity 
        
        self.prev_fire_score = prev_fire_score
        self.prev_neighbor_score = prev_neighbor_score
        self.vehicle_cap = vehicle_cap
        
        if t == 0:
            self.spark = 0
        else:
            self.spark = spark 
        self.t = t
        
        self.fire_score =[]
        self.state =[]
        self.smoke = []
        self.heat = []
        self.cost = []
        self.color = []

    # Start Fire at a Random Forest Location
    def StartFire(self):
        # FIRE!
        startFire = None
        while startFire == None:
            rfr = random.randint(0,Land1.ROW-1)
            rfc = random.randint(0,Land1.COL-1)
            if AA[rfr][rfc] >= 25 and AA[rfr][rfc] <= 45:
                AA[rfr][rfc] = 55
                startFire = AA[rfr][rfc]
                print([rfr,rfc])
                print(startFire)
            else:
                tmp = None # Just a placeholder
        Land1.GraphLand(AA)
    
    # Ignition probability - a func of vegetation type, weather (humidity & temp.), and time
    def get_ign_prob(self):
        ign_prob = (self.ign_veg * self.fuel + self.ign_humid * self.humid + self.ign_temp * self.temp)*t
        return ign_prob
    
    # "Natural" fire score - a function of vegetation type and weather (humidity, temp., wind)
    def get_nat_fire_score(self):
        nat_fire_score = self.spr_veg*self.fuel + self.spr_humid*self.humid + self.spr_temp*self.temp + self.spr_wind*self.wind
        return nat_fire_score
    
    # Amount the fire score INCREASED due to having fire itself
    def fire_score_intensify(self): 
        fire_score_intensify = self.intensify_rate*self.prev_fire_score 
        return fire_score_intensify

    # Amount of fire score INCREASED due to having neighbors that have fire 
    def fire_score_spread(self):
        fire_score_spread = self.spread_rate*self.prev_neighbor_score
        return fire_score_spread

    # Amount of fire score DECREASED due to the presence of firefighting vehicle and its type
    def fire_score_mitigate(self):
        fire_score_mitigate = -self.vehicle_eff*self.vehicle_cap 
        return fire_score_mitigate

    # Calculate new fire score 
    def update_fire(self):
        nat_fire_score = self.get_nat_fire_score()
        print(nat_fire_score)
        # For cell doesn't have a fire, determine ignition conditions  
        if self.prev_fire_score == nat_fire_score: 
            ign_prob = self.get_ign_prob()
            # If probability meets required threshold and there's human activity/lightning, ignite
            if ign_prob >= self.ign_thres and self.spark == 1: 
                self.fire_score += self.prev_fire_score
                self.state = 'ignited'
            else: 
                self.fire_score = self.prev_fire_score
                self.state = 'intact'
        
        # For cell that has a fire, calculate fire score due to surrounding factors (neighbors and firefighting)
        elif self.prev_fire_score > nat_fire_score:
            ign_prob = 0
            intensified_score = self.fire_score_intensify()
            spread_score = self.fire_score_spread()
            mitigated_score = self.fire_score_mitigate()
            self.fire_score = self.prev_fire_score + intensified_score + spread_score + mitigated_score
            self.state = 'burning'

        # For cell in which fire got extinguished, it cannot ignite or burn again
        else: 
            ign_prob = 0
            self.fire_score = 0
            self.state = 'charred'
        
        return ign_prob, self.fire_score, self.state
        
    def color_cell(self):
        if self.fire_score < self.init_fire_score:
            self.color = [0, 0, 0] # cell is black if fire_score decreases to below "natural" score
        # determine different ranges of fire score to color accordingly for other cases 
        return self.color 

    def sign(self): 
        self.smoke = 10* self.fire_score
        self.heat = 10*self.fire_score
        return self.smoke, self.heat 

    def value(self):
        if self.state == 'burning' or self.state == 'charred':
            if self.fuel == 0: 
                lost = 10
            elif self.fuel == 1: 
                lost = 20
            else:
                lost = 30
        else: 
            lost = 0 
        return lost
    
# Test
c1 = FireCell(600, 600, 100, 1, 1)


# for t in range (0, 20):
#     c1 = FireCell(600, 600, 100, 1, t)
#     ign, newscore, state = c1.update_fire()
#     score = newscore
#     #print('Values are', ign, newscore, state)

