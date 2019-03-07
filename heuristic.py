# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:07:14 2018

@author: Lorenzo
"""
import numpy as np

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
    
    
def compute_possible_directions(x,y,mode,width,height):
    if(x < 0 or x >= width or y < 0 or y >= height):
        return []
    else:
        possible_directions = []
        for d_x in range(-1,2,1):
            for d_y in range(-1,2,1):
                c_pos_x = x + d_x
                c_pos_y = y - d_y
                if(mode == "dynamic" and (d_x != 0 or d_y != 0)):
                    if((c_pos_x >= 0 and c_pos_x < width) and (c_pos_y >= 0 and c_pos_y < height) ):
                        possible_directions.append([d_x,d_y])
    return possible_directions

### Compute the distance between two groups
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

def distance_between_groups(x_1,y_1,x_2,y_2):
    d = distance_between_groups_principal_axis(x_1,y_1,x_2,y_2)
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
                
                #print("(d_x,d_y) " + "("+str(d_x) + str(d_y)+")")
                #print("(c_d_x,c_d_y) " + "("+str(c_d_x) + str(c_d_y)+")")
                # Notice that the event diagonals and principal axis are partitions of events
                dist = max(distance_between_groups_principal_axis(c_d_x,c_d_y,x_2,y_2),distance_between_groups_diagonals(c_d_x,c_d_y,x_2,y_2))
                if(dist != -1):
                    return d + dist
                # otherwise i increase the distance
                d += 1  
                
def is_battle(pos_x,pos_y,species_list,width,height):
    for h in range(len(species_list)):
        if(species_list[h][0] == pos_x and species_list[h][1] == pos_y):
            return species_list[h][2]
    return 0    


# Just to respect the notations of the cours: E1 attacks    
# we take the conditional expectation: it's the best guess that we can do
# Please see the images i've sent in fb for more details

def expected_gain_humans(E1,E2,alpha_h,beta_h):

    # If there are more monsters than humans
    if(E1 >= E2):
        expected_number_of_humans_converted = E2
        expected_number_of_monsters_added = 0
    else:
        expected_number_of_humans_converted =  E2 - (4*E2*E1 - E1**2)/(4*E2)
        expected_number_of_monsters_added =  (+E1**3 - E1**2 + 2*E1*E2)/(4*E1)

    #return a function of E2 (here alctually we have to introduce another parameter, alpha)
    return alpha_h*expected_number_of_humans_converted + beta_h*expected_number_of_monsters_added

#E1 attacks
def expected_gain_monsters(E1,E2,alpha_m,beta_m):
    if(E1 >= 1.5*E2):
        # E1 gains
        # E2_tot -= E2
        expected_number_of_survived_monsters_E1 = E1
        expected_number_of_killed_monsters_E2 = E2
    elif(E1 <= 0.666 * E2):
        #E1 loses, E1_tot -= E1
        expected_number_of_survived_monsters_E1 = 0
        expected_number_of_killed_monsters_E2 = 0
    # Random battle
    # Case I
    elif(E1 == E2):
        # E1_tot -= 0.75* E1
        # E2_tot -= 0.75* E2
        expected_number_of_survived_monsters_E1 = 0.75*E1
        expected_number_of_killed_monsters_E2 = 0.75*E2
    # Case II
    elif(E1 < E2):
        # E1_tot -= E1 - E_1**3/(4*E2)
        # E2_tot -= (4*E2**2 - E1**2 + 2 E1*E2)/(4*N_V)
        expected_number_of_survived_monsters_E1 = E1**3 / (4*E2**2)
        expected_number_of_killed_monsters_E2 = (4*E2**2 - E1**2 + 2*E1*E2)/(4*E2)
    # Case III
    elif(E1 > E2):
        # E1_tot -= E1 - 0.25 * E1**3 / E2**2
        # E2_tot -= 0.5*E2 + 2*E1 - (E1**2)/E2
        expected_number_of_survived_monsters_E1 = 0.25* (E1**3 / E2**2 )
        expected_number_of_killed_monsters_E2 = 0.25*E2 + 2*E1 - (E1**2)/E2
        
    # return any function of exp.... or any statistics that has been computed
    return alpha_m * expected_number_of_killed_monsters_E2 + beta_m * expected_number_of_survived_monsters_E1
 
def compute_score(heuristic,index_possible_directions):
    sum_partial_scores = 0
    for i in index_possible_directions:
        sum_partial_scores += heuristic[i]
    return sum_partial_scores

#### MAIN FUNCTIOKN
    

def compute_score_state(s,alpha_m, alpha_h, beta_m, beta_h, player, mode):
#def compute_score_state(s):
    
    ## Get the list
    humans_list = s.get_humans_list()
    vampires_list = s.get_vampires_list()
    werewolves_list = s.get_werewolves_list()
    ## Numbers of groups for each species
    nb_groups_humans = len(humans_list)
    nb_groups_vampires = len(vampires_list)
    nb_groups_werewolves = len(werewolves_list)
    ## Absolute number of
    nb_humans =  s.get_nb_humans()
    nb_vampires = s.get_nb_vampires()
    nb_werewolves = s.get_nb_werewolves()
    # Grid parameter
    #width = s.width
    #height = s.height
    # Grid parameter
    width = s.width
    height = s.height
    #width = 10
    #height = 5
    #alpha_m = 0.99
    #alpha_h = 0.02
    #beta_m = 1 - alpha_m
    #beta_h = 1- alpha_h
    #player = "vampires"
    #mode = "dynamic"
    
    if (player == "vampires"):
        if(len(vampires_list) == 0):
            return -5000000000000000
        if(len(werewolves_list) == 0):
            return +5000000000000000
        
        # Our current positions
        
        x_v = vampires_list[0][0]
        y_v = vampires_list[0][1]
        
        #♦print("----VAMPIRES----")
        #print("Position vampires x,y = {0},{1}".format(x_v,y_v))
        #print("Position vampires x,y = {0},{1}".format(x_v,y_v))
        #print("press to continue")
        #wait = input("PRESS ENTER TO CONTINUE.")
        #########                  Compute heuristic
        
        # The list that will contain the possible directions
        # This is a list of tuples (direction_index,score_for_that_direction)
        
        heuristic = np.zeros((9,)) 
        
        # We penalize the "impossible" directions        
        
        # List of possible directions
        possible_directions = compute_possible_directions(x_v,y_v,mode,width,height)
        nb_possible_directions = len(possible_directions)
        index_possible_directions = []
        #index_possible_directions = np.zeros((nb_possible_directions,))
        
        for p in range(0,nb_possible_directions):
            index_possible_directions.append(dir_index_map(possible_directions[p][0],possible_directions[p][1]))
            #index_possible_directions[p] = dir_index_map(possible_directions[p][0],possible_directions[p][1]) 
        #print(index_possible_directions)
        # FOR CONVENTION we'll use the map: direction ---> index of the list is the following
        # this is a smart map:   phi_i : (d_x,d_y) --> 3*d_x + d_y + 4
        # For d_x : -1 (left), 0 (center), 1 (right)
        # For d_y : -1 (down), 0 (middle), 1 (up)
        # it maps direction in the following way:
        # (-1,-1) -> 0, (-1,0) -> 1 , (-1,1) -> 2, (0,-1) -> 3
        # (0,0) -> 4, (0,1) -> 5, (1,-1) -> 6, (1,0) -> 7 , (1,1) -> 8
        
        ########  Here we take into account the humans
        
        ### Partie I: ILTD "I like this direction"
        for i in range(nb_groups_humans):

            # Group od humans
            consider_group_humans = True
            
            # Get the number of humans in that specific position
            current_nb_humans = humans_list[i][2]
            
            # Get the position of the first human group
            x_h = humans_list[i][0]
            y_h = humans_list[i][1]
            
            # Here we take into account the fact that if there exists an adversary that is nearer
            # than us to the group of humans is worthless to go towards that direction
            
            # Compute the distances
            d_v_h = distance_between_groups(x_v,y_v,x_h,y_h)
            for i_w in range(nb_groups_werewolves):
                if(distance_between_groups(werewolves_list[i_w][0],werewolves_list[i_w][1],x_h,y_h) < d_v_h):
                    consider_group_humans = False
                    break;
                    
            # if i'm nearer to that group of humans wrt to any group of werewolves
            if(consider_group_humans):
                
                # Set the initial directions to -1
                d_x = -1
                d_y = -1
                
                # Geometry: just see where humans are wrt us
                # For x
                if x_v == x_h:
                    d_x = 0
                elif x_h > x_v:
                    d_x = 1
                # For y
                if y_v == y_h:
                    d_y = 0
                elif y_v > y_h:
                    d_y = 1
                    
                # Compute the relative index
                direction_index = dir_index_map(d_x,d_y)
                
                if(current_nb_humans > nb_vampires):
                    lam = 1
                    heuristic[direction_index] += lam*(nb_vampires - current_nb_humans)
                else:
                    # Here there's a simple function but we can write any function 
                    #heuristic[direction_index] += alpha_h * (current_nb_humans)
                    #*np.exp(-d_v_h)
                    heuristic[direction_index] += alpha_h * ( current_nb_humans/ ((d_v_h)/2 + 1)**(0.2))
                # Sort of regularization: if there are more humans that monters it's not ok to go in that direction
                
                #print("HD: {}".format(d_v_h))
                #print("H. direction {0} = {1}".format(direction_index, heuristic[direction_index]))
        
                
        #print("H. Part")
        #print(heuristic)
        # Here we take into account the possible battles
        
        ### Partie II: HSIARN "How strong i am right now"
        
        for possible_direction in possible_directions:
            [d_x,d_y] = possible_direction
            direction_index = dir_index_map(d_x,d_y)
            #print("Direction_index: "+str(direction_index))
            #print("(d_x,d_y) " + "("+str(d_x) + str(d_y)+")"+","+"Score before the battle : "+str(heuristic[direction_index]))
            # Position at the next turn
            # Please note the minus convention because the axis are inverted
            f_x_v = x_v + d_x
            f_y_v = y_v - d_y
            # If there are humans, and how many
            h_b = is_battle(f_x_v,f_y_v,humans_list, width,height)
            m_b = is_battle(f_x_v,f_y_v,werewolves_list,width,height)
            #-------------------------------------------------------------DEBUG
            if(h_b > 0):
                heuristic[direction_index] += expected_gain_humans(nb_vampires,h_b,alpha_h,beta_h)
            if(m_b > 0):
                heuristic[direction_index] += expected_gain_monsters(nb_vampires,m_b,alpha_m,beta_m)
            #print("(d_x,d_y) " + "("+str(d_x) + str(d_y)+")"+","+"Score : "+str(heuristic[direction_index]))
        
        
        # Partie III: Inference: get the argmax
        #4print("M. Part")
        #print(heuristic)
        # get the best directions, given an index
        return compute_score(heuristic,index_possible_directions)
    
    elif(player == "werewolves"): 
        
        # Our current positions
        x_w = werewolves_list[0][0]
        y_w = werewolves_list[0][1]
        
        #########                  Compute heuristic
        
        # The list that will contain the possible directions
        # This is a list of tuples (direction_index,score_for_that_direction)
        
        heuristic = np.zeros((9,1)) 
        
        # List of possible directions
        possible_directions = compute_possible_directions(x_w,y_w,mode,width,height)
        nb_possible_directions = len(possible_directions)
        #index_possible_directions = np.zeros((nb_possible_directions,1))
        index_possible_directions = []
        
        for p in range(0,nb_possible_directions):
            index_possible_directions.append(dir_index_map(possible_directions[p][0],possible_directions[p][1]))
            
        #for p in range(0,nb_possible_directions):
        #    index_possible_directions[p] = dir_index_map(possible_directions[p][0],possible_directions[p][1]) 

        # FOR CONVENTION we'll use the map: direction ---> index of the list is the following
        # this is a smart map:   phi_i : (d_x,d_y) --> 3*d_x + d_y + 4
        # For d_x : -1 (left), 0 (center), 1 (right)
        # For d_y : -1 (down), 0 (middle), 1 (up)
        # it maps direction in the following way:
        # (-1,-1) -> 0, (-1,0) -> 1 , (-1,1) -> 2, (0,-1) -> 3
        # (0,0) -> 4, (0,1) -> 5, (1,-1) -> 6, (1,0) -> 7 , (1,1) -> 8
        
        ########  Here we take into account the humans
        
        ### Partie I: ILTD "I like this direction"
        print("----WAREVOLVES----")
        for i in range(nb_groups_humans):

            # Group od humans
            consider_group_humans = True
            
            # Get the number of humans in that specific position
            current_nb_humans = humans_list[i][2]
            
            # Get the position of the first human group #coordinates (top-left corner 0-0, bottom-right corner 9-9)
            x_h = humans_list[i][0]
            y_h = humans_list[i][1]
            
            # Here we take into account the fact that if there exists an adversary that is nearer
            # than us to the group of humans is worthless to go towards that direction
            
            # Compute the distances
            d_w_h = distance_between_groups(x_w,y_w,x_h,y_h)
            for i_v in range(nb_groups_vampires):
                if(distance_between_groups(vampires_list[i_v][0],vampires_list[i_v][1],x_h,y_h) < d_w_h):
                    consider_group_humans = False
                    break;
                    
            # if i'm nearer to that group of humans wrt to any group of werewolves
            if(consider_group_humans):
                # Set the initial directions to -1
                d_x = -1
                d_y = -1
                
                # Geometry: just see where humans are wrt us
                # For x
                if x_w == x_h:
                    d_x = 0
                elif x_h > x_w:
                    d_x = 1
                # For y
                if y_w == y_h:
                    d_y = 0
                elif y_w > y_h:
                    d_y = 1
                    
                # Compute the relative index
                direction_index = dir_index_map(d_x,d_y)
                
                # We have both direction, distance between the humans (d_v_h) and 
                # # of humans (current_nb_humans)
                
                #Here there's a simple function but we can write any function 
                heuristic[direction_index] += alpha_h * ( current_nb_humans/ ((d_w_h)/2 + 1)**(0.2))
                print("Monster postion: {0}, {1}".format(x_w, y_w))
                print("humans distance: {}".format(d_w_h))
                print("H.V. for {0} h and direction {1} = {2}".format(current_nb_humans,direction_index, heuristic[direction_index]))
    #else:
            # or any other function (i want to penalize this direction)
            #    heuristic[direction_index] -= alpha_h * current_nb_humans 
        
        # Here we take into account the possible battles
        
        ### Partie II: HSIARN "How strong i am right now"
        
        for possible_direction in possible_directions:
            [d_x,d_y] = possible_direction
            direction_index = dir_index_map(d_x,d_y)
            #print("Direction_index: "+str(direction_index))
            #print("(d_x,d_y) " + "("+str(d_x) + str(d_y)+")"+","+"Score before the battle : "+str(heuristic[direction_index]))
            # Position at the next turn
            # Please note the minus convention because the axis are inverted
            f_x_w = x_w + d_x
            f_y_w = y_w - d_y
            # If there are humans, and how many
            h_b = is_battle(f_x_w,f_y_w,humans_list, width,height)
            m_b = is_battle(f_x_w,f_y_w,vampires_list,width,height)
            if(h_b > 0):
                heuristic[direction_index] += expected_gain_humans(nb_werewolves,h_b,alpha_h,beta_h)
            if(m_b > 0):
                heuristic[direction_index] += expected_gain_monsters(nb_werewolves,m_b,alpha_m,beta_m)
            #print("(d_x,d_y) " + "("+str(d_x) + str(d_y)+")"+","+"Score : "+str(heuristic[direction_index]))
        
        
        # Partie III: Inference: get the argmax
        
        # get the best directions, given an index
        return compute_score(heuristic,index_possible_directions)