# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 17:55:03 2018

@author: assae
"""

import state as st
import numpy as np
import itertools
import heuristic_2 as hc
import time

def allowed_directions(x, y, w, h):
    if x >= w or y >= h:
        print("Position error")
    elif (x == 0 and y == 0):
        return [[0,-1], [1,-1], [1,0]]
    elif (x == w-1 and y == 0):
        return [[-1,0], [-1,1], [0,-1]]
    elif (x == 0 and y == h-1):
        return [[0,1], [1,1], [1,0]]
    elif (x == w-1 and y == h-1):
        return [[-1,0], [-1,1], [0,1]]
    elif (x == 0 and y != 0 and y != h-1):
        return [[-1,0], [-1,-1], [0,-1], [1,-1], [1,0]]
    elif (x == w-1 and y != 0 and y != h-1):
        return [[-1,0], [-1,1], [0,1], [1,1], [1,0]]
    elif (x != 0 and x != w-1 and y == 0):
       return [[0,1], [1,1], [1,0], [1,-1], [0,-1]]
    elif (x != 0 and x != w-1 and y == h-1):
       return [[0,1], [-1,1], [-1,0], [-1,-1], [0,-1]]
    else:
        return [[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]]
    
    
    
def compute_successors(s, player):
    humans_list = s.get_humans_list()
    vampires_list = s.get_vampires_list()
    werewolves_list = s.get_werewolves_list()
    nb_groups_humans = len(humans_list)
    nb_groups_vampires = len(vampires_list)
    nb_groups_werewolves = len(werewolves_list)
    nb_humans =  s.get_nb_humans()
    nb_vampires = s.get_nb_vampires()
    nb_werewolves = s.get_nb_werewolves()
    width = s.width
    height = s.height
    
    if player == "vampires":      
        possible_directions = []
        moves = []
        if nb_werewolves <= 0.5* nb_vampires:
            if nb_groups_vampires >= 2:
                #si on a deja 2 groupes on ne separe pas
                nb_separations = 1
            else:
                nb_separations = 2           
        else : 
            #pas de séparation
            nb_separations = 1
            
        for group in vampires_list:
            possible_directions = allowed_directions(group[0], group[1], width, height)
            """We add as the first term the possible directions so that we can easily have it afterwards, 
            so, in the state some elements will have 6 elements, the first being the direction.
            To remove for calculations and add back afterwards."""
#            moves.append([[[possible_directions[j][0], possible_directions[j][1]], group[0], group[1], group[2], group[0]+ possible_directions[j][0], 
#                           group[1]- possible_directions[j][1]] for j in range(len(possible_directions))])
            moves.append([[group[0], group[1], group[2], group[0]+ possible_directions[j][0],
                           group[1]- possible_directions[j][1]] for j in range(len(possible_directions))])
        moves = cartesian_product(*moves)
        new_states = []
        for i in range(len(moves)):
#            new_states.append(compute_states_after_moves(s, moves[i], player))
            new_states.append(s.new_state(moves[i]))
        return new_states
    
    elif player == "werewolves":      
        possible_directions = []
        moves = []
        if nb_vampires <= 0.5* nb_werewolves:
            if nb_groups_vampires >= 2:
                #si on a deja 2 groupes on ne separe pas
                nb_separations = 1
            else:
                nb_separations = 2           
        else : 
            #pas de séparation
            nb_separations = 1
        for group in werewolves_list:
            possible_directions = allowed_directions(group[0], group[1], width, height)
#            moves.append([[[possible_directions[j][0], possible_directions[j][1]], group[0], group[1], group[2], group[0]+ possible_directions[j][0], 
#                           group[1]- possible_directions[j][1]] for j in range(len(possible_directions))])
        moves.append([[group[0], group[1], group[2], group[0]+ possible_directions[j][0],
                       group[1]- possible_directions[j][1]] for j in range(len(possible_directions))])
        moves = cartesian_product(*moves)
        new_states = []
        for i in range(len(moves)):
#            new_states.append(compute_states_after_moves(s, moves[i], player))
            new_states.append(s.new_state(moves[i]))
        return new_states

            


def compute_states_after_moves(state, moves, player):
    
    """Have to designed a function which take a state and list of moves 
    [[direction], x, y, nb, new x, new y] and return the new state"""
    
    w = state.width
    h = state.height
    s = state.state_list
    moves = list(moves)
    
    if player == "vampires":
        modif = []
        move_to_remove = []
        for i in range(len(moves)):
            for j in range(len(s)):
                if moves[i][3] == s[j][0] and moves[i][4] == s[j][1]:
                    origin = look_for_case(s, moves[i][0], moves[i][1])
                    s[origin] = [s[origin][0], s[origin][1], s[origin][2], s[origin][3] - moves[i][2], s[origin][4]]
                    modif.append(result(s[j], moves[i][2], player))
                    move_to_remove.append(moves[i])
                    
        for m in move_to_remove:
            moves.remove(m)
        
        for i in range(len(moves)):
            
            origin = look_for_case(s, moves[i][0], moves[i][1])
            s[origin] = [s[origin][0], s[origin][1], s[origin][2], s[origin][3] - moves[i][2], s[origin][4]]
            modif.append([moves[i][3], moves[i][4], 0, moves[i][2], 0])
            
        state = st.State(s,w,h)
        new_state = state.new_state(modif)
        return new_state
    
    elif player == "werewolves":
        modif = []
        move_to_remove = []
        for i in range(len(moves)):
            for j in range(len(s)):
                if moves[i][3] == s[j][0] and moves[i][4] == s[j][1]:
                    origin = look_for_case(s, moves[i][0], moves[i][1])
                    s[origin] = [s[origin][0], s[origin][1], s[origin][2], s[origin][3], s[origin][4] - moves[i][2]]
                    modif.append(result(s[j], moves[i][2], player))
                    move_to_remove.append(moves[i])
                    
        for m in move_to_remove:
            moves.remove(m)
        
        for i in range(len(moves)):
            origin = look_for_case(s, moves[i][0], moves[i][1])
            s[origin] = [s[origin][0], s[origin][1], s[origin][2], s[origin][3], s[origin][4] - moves[i][2]]
            modif.append([moves[i][3], moves[i][4], 0, 0,  moves[i][2]])
            
        state = st.State(s,w,h)
        new_state = state.new_state(modif)
        return new_state
                    
                    
                    
        
    
def result(case, nb_player_moved, player):
    """ we have a case [x, y nb_h, nb_v, nb_w] and we move nb_player_moved of 
    monsters of categories player in this case: this function return the new case"""
    if player == "vampires":
        modif = []
        if case[2]!=0 and case[3]!= 0 and case[4]!= 0:
            nb_vampires1, nb_humans = expected_gain_humans(nb_player_moved + case[3], case[2])
            nb_vampires2, nb_werewolves = expected_gain_monsters(nb_player_moved + case[3], case[4])
            modif.append([case[0], case[1], nb_humans, (nb_vampires1 + nb_vampires2)/2, nb_werewolves])
        elif case[2]!=0 and case[4]!= 0:
            nb_vampires1, nb_humans = expected_gain_humans(nb_player_moved, case[2])
            nb_vampires2, nb_werewolves = expected_gain_monsters(nb_player_moved, case[4])
            modif.append([case[0], case[1], nb_humans, (nb_vampires1 + nb_vampires2)/2, nb_werewolves])                                        
        elif case[2]!=0 and case[3]!= 0:
            nb_vampires1, nb_humans = expected_gain_humans(nb_player_moved + case[3], case[2])
            modif.append([case[0], case[1], nb_humans, nb_vampires1, 0])
        elif case[3]!=0 and case[4]!= 0:
            nb_vampires2, nb_werewolves = expected_gain_monsters(nb_player_moved + case[3], case[4])
            modif.append([case[0], case[1], 0, nb_vampires2, nb_werewolves])
        elif case[2]!=0:
            nb_vampires1, nb_humans = expected_gain_humans(nb_player_moved, case[2])
            modif.append([case[0], case[1], nb_humans, nb_vampires1, 0])
        elif case[3]!=0:
            modif.append([case[0], case[1], 0, case[3] + nb_player_moved, 0])
        elif case[4]!=0:
            nb_vampires2, nb_werewolves = expected_gain_monsters(nb_player_moved, case[4])
            modif.append([case[0], case[1], 0, nb_vampires2, nb_werewolves])
        else:
            modif.append([case[0], case[1], 0, nb_player_moved, 0])
        return modif[0]
    
    elif player == "werewolves":
        modif = []
        if case[2]!=0 and case[3]!= 0 and case[4]!= 0:
            nb_werewolves1, nb_humans = expected_gain_humans(nb_player_moved + case[4], case[2])
            nb_werewolves2, nb_vampires = expected_gain_monsters(nb_player_moved + case[4], case[3])
            modif.append([case[0], case[1], nb_humans, nb_vampires, (nb_werewolves1 + nb_werewolves2)/2])
        elif case[2]!=0 and case[3]!= 0:
            nb_werewolves1, nb_humans = expected_gain_humans(nb_player_moved, case[2])
            nb_werewolves2, nb_vampires = expected_gain_monsters(nb_player_moved, case[3])
            modif.append([case[0], case[1], nb_humans, nb_vampires, (nb_werewolves1 + nb_werewolves2)/2])                                       
        elif case[2]!=0 and case[4]!= 0:
            nb_werewolves, nb_humans = expected_gain_humans(nb_player_moved + case[4], case[2])
            modif.append([case[0], case[1], nb_humans, 0, nb_werewolves])
        elif case[3]!=0 and case[4]!= 0:
            nb_werewolves2, nb_vampires = expected_gain_monsters(nb_player_moved + case[4], case[3])
            modif.append([case[0], case[1], 0, nb_vampires, nb_werewolves2])
        elif case[2]!=0:
            nb_werewolves1, nb_humans = expected_gain_humans(nb_player_moved, case[2])
            modif.append([case[0], case[1], nb_humans, 0, nb_werewolves1])
        elif case[4]!=0:
            modif.append([case[0], case[1], 0, 0, case[4] + nb_player_moved])
        elif case[3]!=0:
            nb_werewolves2, nb_vampires = expected_gain_monsters(nb_player_moved, case[3])
            modif.append([case[0], case[1], 0, nb_vampires, nb_werewolves2])
        else:
            modif.append([case[0], case[1], 0, 0, nb_player_moved])
        return modif[0]
            

    


def look_for_case(state_liste, x, y):
    for i in range(len(state_liste)):
        if state_liste[i][0] == x and state_liste[i][1] == y:
            return i
            

def cartesian_product(*arrays):
    cart_prod = []
    for element in itertools.product(*arrays):
        cart_prod.append(element)
    return cart_prod



def expected_gain_humans(E1,E2):
    """Give number of attackers E1 and defenseur E2 remaining in case of E1 monster attacking humans"""
    if(E1 >= E2):
        expected_number_of_monsters = E2+E1
        expected_number_of_humans = 0
    else:
        expected_number_of_monsters =  ((E1/(2*E2))**2) * (E1 + E2)
        expected_number_of_humans = ((1-(E1/(2*E2)))**2) * E2
    return expected_number_of_monsters, expected_number_of_humans


def expected_gain_monsters(E1,E2):
    """Give number of attackers E1 and defenseur E2 remaining in case of E1 monster attacking monster"""
    if(E1 >= 1.5*E2):
        expected_number_of_E1 = E1
        expected_number_of_E2 = 0
    elif(E1 <= 0.666 * E2):
        expected_number_of_E1 = 0
        expected_number_of_E2 = E2
    elif(E1 == E2):
        expected_number_of_E1 = (0.5**2)*E1
        expected_number_of_E2 = (0.5**2)*E2
    elif(E1 < E2):
        expected_number_of_E1 = ((E1/(2*E2))**2) * E1
        expected_number_of_E2 = ((1-(E1/(2*E2)))**2) * E2
    elif(E1 > E2):
        expected_number_of_E1 = (((E1/E2)-0.5)**2) * E1
        expected_number_of_E2 = ((1-((E1/E2)-0.5))**2) * E2
    return expected_number_of_E1, expected_number_of_E2


def max_value(state, alpha, beta, player, depth, depth_max):
    w = state.width
    h = state.height
    if player == "vampires":
        if depth == depth_max:
            """we kept the directions in the states so that they are easy to 
            find, we have to remove them to compute the heuristic"""
            return heuristic(state, player)
        depth +=1
        v = -10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mn = min_value(state, alpha, beta, "werewolves", depth, depth_max)
            v = max(v, mn)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v
    elif player == "werewolves":
        if depth == depth_max:
            return heuristic(state, player)
        depth+=1
        v = -10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mn = min_value(state, alpha, beta, "vampires", depth, depth_max)
            v = max(v, mn)
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

               
def min_value(state, alpha, beta, player, depth, depth_max):
    w = state.width
    h = state.height
    
    if player == "vampires":
        if depth == depth_max:
            return heuristic(state, player)
        depth+=1
        v = +10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mx = max_value(state, alpha, beta, "vampires", depth, depth_max)
            v = min(v, mx)
            if v >= beta:
                return v
            beta = min(beta, v)
        return v
    
    elif player == "werewolves":
        if depth == depth_max:
            return heuristic(state, player)
        depth+=1
        v = +10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mx = max_value(state, alpha, beta, "werewolves", depth, depth_max)
            v = min(v, mx)
            if v >= beta:
                return v
            beta = min(beta, v)
        return v
    

def heuristic(state, player):
    if player == "vampires":
        return state.get_nb_vampires() - state.get_nb_werewolves()
    elif player == "werewolves":
        return state.get_nb_werewolves() - state.get_nb_vampires()
        

def return_movements(new_state, old_state, player):
    """return movements to go from the old state to the new state"""
    h = old_state.height
    w = old_state.width
    new_list = new_state.state_list
    new_length = len(new_list)
    old_list = old_state.state_list
    old_length = len(old_list)
    modif_new = []
    can_move = []
    
    if player == "vampires":
        modif_new = [new_list[i] for i in range(new_length) if new_list[i] not in old_list]
        can_move = [old_list[i] for i in range(old_length) if old_list[i] not in new_list and old_list[i][3]!=0]
        return can_move, modif_new
    
        for i in range(len(can_move)):
            possible_directions = allowed_directions(can_move[i][0], can_move[i][1], w, h)
         
    
    
    
    elif player == "werewolves":
        modif_new = [new_list[i] for i in range(new_length) if new_list[i] not in old_list]
        can_move = [old_list[i] for i in range(old_length) if old_list[i] not in new_list and old_list[i][4]!=0]
        return can_move, modif_new
    
def find_movements(can_move, has_been_modified, w, h):
    for i in range(can_move):
        pass
                



t1 = time.time()
alpha = -10**99
beta = 10**99  
state = st.State([[9, 0, 2, 0, 0], [4, 1, 0, 0, 7], [4, 2, 5, 0, 0], [2, 3, 0, 7, 0], [9, 4, 0, 0, 6], [1, 4, 0, 4, 0]], 10, 5)           
state2 = st.State( [[9, 0, 2, 0, 0], [4, 2, 0, 4, 0], [2, 2, 0, 11, 0], [9, 4, 2, 0, 0], [1, 4, 0, 4, 0] ] , 10, 5)           
player = "vampires"
moves  = [[4,1,4,4,2], [2,3,7,2,4], [1,4,2,1,5]]
#a = compute_successors(state, player)
#print(a)
depth = 0
depth_max = 4
b = max_value(state, alpha, beta, player, depth, depth_max) 
print(b)
t2 = time.time()
print(t1-t2)