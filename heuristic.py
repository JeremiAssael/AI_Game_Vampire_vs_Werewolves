# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 00:57:47 2019

@author: Lollo
"""

import numpy as np
import compute_successors as cs

# --------------------------------- DEFINITION OF AUXILIARS FUNCTIONS

# for indexing
# List of possible directions
# FOR CONVENTION we'll use the map: direction ---> index of the list is the following
# this is a smart map:   phi_i : (d_x,d_y) --> 3*d_x + d_y + 4
# For d_x : -1 (left), 0 (center), 1 (right)
# For d_y : -1 (down), 0 (middle), 1 (up)
# it maps direction in the following way:
# (-1,-1) -> 0, (-1,0) -> 1 , (-1,1) -> 2, (0,-1) -> 3
# (0,0) -> 4, (0,1) -> 5, (1,-1) -> 6, (1,0) -> 7 , (1,1) -> 8

def dir_index_map(d_x,d_y):
    return 3*d_x + d_y + 4

def inv_index_map(val):
    if(val == 0):
        return [-1,-1]
    elif(val == 1):
        return [-1,0]
    elif(val == 2):
        return [-1,1]
    elif(val == 3):
        return [0,-1]
    elif(val == 4):
        return [0,0]
    elif(val == 5):
        return [0,1]
    elif(val == 6):
        return [1,-1]
    elif(val == 7):
        return [1,0]
    else:
        return [1,1]

# for geometry  
def distance_between_groups_principal_axis(x_1,y_1,x_2,y_2):
    if(x_1 == x_2):
        return abs(y_2-y_1) - 1
    elif(y_1 == y_2):
        return abs(x_2-x_1) - 1
    else:
        return -1
    
def distance_between_groups_diagonals(x_1,y_1,x_2,y_2):
    dist = abs(x_1 - x_2) 
    if(dist == abs(y_1 - y_2)):
        return dist - 1
    else:
        return -1

def distance_between_groups(x_1,y_1,x_2,y_2, adj_0 = False):
    d = distance_between_groups_principal_axis(x_1,y_1,x_2,y_2)
    if adj_0:
        if (d != -1):
            return d
        else:
             # we're not in the principal axis
             # check whether is right adjacent
            d = distance_between_groups_diagonals(x_1,y_1,x_2,y_2)
            if(d != -1):
                return d
            # this case is never evaluated in practice, but for the sake of clarity...
            elif(x_1 == x_2 and y_1 == y_2):
                return -1
            else: 
                #here is try to move in a position that belongs to the diagonal or to a principal axis
                # we're looking where the g2 is
                d = 1
                d_x = 0
                d_y = 0
                c_d_x = x_1
                c_d_y = y_1
                while(True):
                    # get the direction in which we have to point towards
                    if( x_2 > c_d_x):
                        d_x = 1
                    else:
                        d_x = -1
                    if( c_d_y > y_2):
                        d_y = 1
                    else:
                        d_y = -1                
                    # Update the coordinates
                    c_d_x += + d_x
                    c_d_y += - d_y
                    # Notice that the event diagonals and principal axis are partitions of events
                    dist = max(distance_between_groups_principal_axis(c_d_x,c_d_y,x_2,y_2),distance_between_groups_diagonals(c_d_x,c_d_y,x_2,y_2))
                    if(dist != -1):
                        return d + dist + 1
                    # otherwise i increase the distance
                    d += 1  
    else:
        if (d != -1):
            return d + 1
        else:
             # we're not in the principal axis
             # check whether is right adjacent
            d = distance_between_groups_diagonals(x_1,y_1,x_2,y_2)
            if(d != -1):
                return d + 1
            # this case is never evaluated in practice, but for the sake of clarity...
            elif(x_1 == x_2 and y_1 == y_2):
                return 0
            else: 
                #here is try to move in a position that belongs to the diagonal or to a principal axis
                # we're looking where the g2 is
                d = 1
                d_x = 0
                d_y = 0
                c_d_x = x_1
                c_d_y = y_1
                while(True):
                    # get the direction in which we have to point towards
                    if( x_2 > c_d_x):
                        d_x = 1
                    else:
                        d_x = -1
                    if( c_d_y > y_2):
                        d_y = 1
                    else:
                        d_y = -1                
                    # Update the coordinates
                    c_d_x += + d_x
                    c_d_y += - d_y
                    # Notice that the event diagonals and principal axis are partitions of events
                    dist = max(distance_between_groups_principal_axis(c_d_x,c_d_y,x_2,y_2),distance_between_groups_diagonals(c_d_x,c_d_y,x_2,y_2))
                    if(dist != -1):
                        return d + dist + 1
                    # otherwise i increase the distance
                    d += 1  
                    
def get_the_direction(xm,ym,xh,yh):
    # Geometry: just see where humans are wrt us
    # Set the initial directions to -1

    d_x = -1
    d_y = -1 
                       
    # For x
    if xm == xh:
        d_x = 0
    elif xh > xm:
        d_x = 1
    # For y
    if ym == yh:
        d_y = 0
    elif ym > yh:
        d_y = 1

    return d_x,d_y

# for battles                   
def expected_gain_humans(E1,H1): 
    #normalized to one
    P = E1/H1
    if P >= 1:
        expected_number_of_humans_converted = 1
    else: # we do not consider the tem that converns the monsters in the conditional expectation
        expected_number_of_humans_converted = (P/2)**2
    #return a function of E2 (here alctually we have to introduce another parameter, alpha)
    return expected_number_of_humans_converted

def expected_gain_monster(E1,E2,alpha): 
    #alpha_m: how I want to be aggressive towards monster--> must augment during the game
    # different from alpha and beta at the begging.. its not the importance of monster it self
    #normalized to one
    E12 = E1/E2
    E21 = E2/E1
    
    # analyzing our monster
    if E12 >= 1.5:
        P12 = 1
        our_alive_monsters = 1
    elif E12 >= 1:
        P12 = E12 - 0.5
        our_alive_monsters = P12**2
    else:
        P12 = 0.5*E12
        our_alive_monsters = P12**2
        
    their_alive_monsters = (1-P12)**2 * E21
    
    return our_alive_monsters + (1-alpha)*their_alive_monsters

# for the heuristics 
def activation_function_humans(value,par = 15): # par is a function of to_hg (the higher to_hg the higher par)
    return value**par

def activation_function_monsters(value,par = 10): # par is a function of to_hg (the higher to_mg the higher par)
    return value**par

def compute_score(heuristic,index_possible_directions):
    sum_partial_scores = 0
    for i in index_possible_directions:
        sum_partial_scores += heuristic[i]
    return sum_partial_scores


def compute_score_state_player(our_monsters_list, their_monsters_list, humans_list, our_monsters_nb_groups, their_monsters_nb_groups, nb_groups_humans, nb_our_monsters, width, height, MAX_DIST, MAX_NB_HUMANS, INF, lam_h = 0.5, alpha = 0.7, to_gh = 3, to_gm = 3):
    # extreme situations
    if(len(our_monsters_list) == 0):
        return -INF
    if(len(our_monsters_list) == 0):
        return +INF 
    
    # compute some useful constants
    if(their_monsters_nb_groups == 0):
        MAX_NB_OTHER_MONSTERS = -1
    else:
        MAX_NB_OTHER_MONSTERS = np.max([elem[2] for elem in their_monsters_list])
    
    # Current positions
    x_us = our_monsters_list[0][0]
    y_us = our_monsters_list[0][1]
    
    #----------------------------------------------------HEURISTIC MESURES
    
    heuristic_humans = np.zeros((9,))
    heuristic_monsters = np.zeros((9,))
    
    compute_battles_score_humans = 0
    compute_battles_score_monsters = 0     
    
    #----------------------------------------------------ADMISSIBLE POSITIONS
    
    possible_directions = cs.allowed_directions(x_us,y_us,width,height)
    nb_possible_directions = len(possible_directions)
    index_possible_directions = []
    for p in range(0,nb_possible_directions):
        index_possible_directions.append(dir_index_map(possible_directions[p][0],possible_directions[p][1]))
    
    #----------------------------------------------------ADMISSIBLES GROUPS OF HUMANS
    
    #Compute all the distances between the gruop of monsters and the humans and store them in distances_humans
    distances_humans = []
    
    for i in range(nb_groups_humans):
        
        # Get the position of the first human group
        x_h = humans_list[i][0]
        y_h = humans_list[i][1]
        
        # Normally I compute the distance. 
        # BUT: if there are more humans than monsters d = MAX_DIST so that this solution won't be choosen
        # OR: if there exists an adversary that is nearer  than us to the group of humans is worthless to go towards that direction d = MAX_DIST
        # NOTE: limitation of the second case: see notes
        
        if humans_list[i][2] <= nb_our_monsters:
            
            dh_pivot = distance_between_groups(x_us,y_us,x_h,y_h)
            # If also i'm nearer
            im_nearer = True
            for i_tm in range(their_monsters_nb_groups):
                if(distance_between_groups(their_monsters_list[i_tm][0],their_monsters_list[i_tm][1],x_h,y_h) < dh_pivot):
                    im_nearer = False
                    break;
            if im_nearer:
                distances_humans.append(dh_pivot)
            else:
                distances_humans.append(MAX_DIST)
        else:
            distances_humans.append(MAX_DIST)

    # Normalize distances 
    to_nb_groups_humans_considered = min(to_gh,nb_groups_humans)
    normalized_distances_humans = [d/(MAX_DIST*to_nb_groups_humans_considered) for d in distances_humans]
    
    # And take the nearest groups 
    index_least_distances = np.argsort(normalized_distances_humans)[0:to_nb_groups_humans_considered]
    
    #----------------------------------------------------Part I: ILTD "I like this direction"
    
    for i in index_least_distances:
        # Get the number of humans in that specific position
        current_nb_humans = humans_list[i][2]
        
        # Get the position of the first human group
        x_h = humans_list[i][0]
        y_h = humans_list[i][1]
        
        d_m_h = distances_humans[i]
        d_x, d_y = get_the_direction(x_us,y_us,x_h,y_h)
        direction_index = dir_index_map(d_x,d_y)
        
        EGH = expected_gain_humans(nb_our_monsters,current_nb_humans) # in this case will be always = 1
       
        # If there is a battle
        if d_m_h == 0:
            compute_battles_score_humans += EGH
            
        if(direction_index in index_possible_directions):
            heuristic_humans[direction_index] += EGH * (current_nb_humans/MAX_NB_HUMANS) * activation_function_humans(1-normalized_distances_humans[i])

    #----------------------------------------------------ADMISSIBLES GROUPS OF MONSTERS
    #Compute all the distances between the group of vampires and the warewolves
    distances_their_monsters = []
    
    for i in range(their_monsters_nb_groups):
        
        x_them = their_monsters_list[i][0]
        y_them = their_monsters_list[i][1]
        
        # Normally I compute the distance. 
        # BUT: if the other are more than us than monsters d = MAX_DIST so that this solution won't be choosen
        if their_monsters_list[i][2] <= 1.5 * nb_our_monsters:
            dm_pivot = distance_between_groups(x_us,y_us,x_them,y_them)
            distances_their_monsters.append(dm_pivot)
        else:
            distances_their_monsters.append(MAX_DIST)
    # Normalize distances 
    to_nb_groups_their_monsters_considered = min(to_gm,their_monsters_nb_groups)
    normalized_distances_their_monsters = [d/(MAX_DIST*to_nb_groups_their_monsters_considered) for d in distances_their_monsters]
    
    # And take the nearest groups 
    index_least_distances_their_monsters = np.argsort(normalized_distances_their_monsters)[0:to_nb_groups_their_monsters_considered]
    
    for i in index_least_distances_their_monsters:
        # Get the number of humans in that specific position
        current_nb_their_monsters = their_monsters_list[i][2]
        
        # Get the position of the first human group
        x_them = their_monsters_list[i][0]
        y_them = their_monsters_list[i][1]
        
        d_m_m = distances_their_monsters[i]
        d_x, d_y = get_the_direction(x_us,y_us,x_them,y_them)
        
        # Compute the relative index
        direction_index = dir_index_map(d_x,d_y)
    
        EGM = expected_gain_monster(nb_our_monsters,current_nb_their_monsters,alpha) # in this case will be always = 1
        
        # If there is a battle
        if d_m_m == 0:
            compute_battles_score_monsters += EGM
        
        if(direction_index in index_possible_directions):
            heuristic_monsters[direction_index] += activation_function_monsters(1-normalized_distances_their_monsters[i])*activation_function_monsters(EGM)*(current_nb_their_monsters/MAX_NB_OTHER_MONSTERS)
    
    
    return lam_h*(compute_score(heuristic_humans,index_possible_directions) + compute_battles_score_humans) + (1 - lam_h)*(compute_score(heuristic_monsters,index_possible_directions) + compute_battles_score_monsters)

              
def compute_score_state(s,alpha_m, alpha_h, beta_m, beta_h, player, mode):
    
    ## Get the list
    humans_list = s.get_humans_list()
    vampires_list = s.get_vampires_list()
    werewolves_list = s.get_werewolves_list()
    
    ## Numbers of groups for each species
    nb_groups_humans = len(humans_list)
    nb_groups_vampires = len(vampires_list)
    nb_groups_werewolves = len(werewolves_list)
    
    ## Absolute number of
    nb_vampires = s.get_nb_vampires()
    nb_werewolves = s.get_nb_werewolves()
    
    # Grid parameter
    width = s.width
    height = s.height
    
    #constants
    INF = np.inf
    MAX_DIST = distance_between_groups(0,0,width-1,height-1)
    
    if(nb_groups_humans == 0):
        MAX_NB_HUMANS = -1
    else:
        MAX_NB_HUMANS = np.max([elem[2] for elem in humans_list])
       
    if (player == "vampires"):
        return compute_score_state_player(vampires_list, werewolves_list, humans_list, nb_groups_vampires, nb_groups_werewolves, nb_groups_humans, nb_vampires, width, height, MAX_DIST, MAX_NB_HUMANS, INF, lam_h = 0.5, alpha = 0.7, to_gh = 3, to_gm = 3)
    elif(player == "werewolves"): 
        return compute_score_state_player(werewolves_list, vampires_list, humans_list, nb_groups_werewolves, nb_groups_vampires, nb_groups_humans, nb_werewolves, width, height, MAX_DIST, MAX_NB_HUMANS, INF, lam_h = 0.5, alpha = 0.7, to_gh = 3, to_gm = 3)
    
    # NOTE: lam_h and alpha may vary depending on the situation. We will do an estimation procedure. But before we have to make several simulations
        