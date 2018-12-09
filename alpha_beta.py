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
        moves_fin = []
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
            moves.append([[[possible_directions[j][0], possible_directions[j][1]], group[0], group[1], group[2], group[0]+ possible_directions[j][0], 
                           group[1]- possible_directions[j][1]] for j in range(len(possible_directions))])
        moves = cartesian_product(*moves)
        print(moves)
        new_states = []
        for i in range(len(moves)):
#            new_states.append(compute_states_after_moves(s, moves[i][1:5], player))
            new_states.append(s.new_state(moves[i][1:6]))
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
            moves.append([[[possible_directions[j][0], possible_directions[j][1]], group[0], group[1], group[2], group[0]+ possible_directions[j][0], 
                           group[1]- possible_directions[j][1]] for j in range(len(possible_directions))])
        moves = cartesian_product(*moves)
        new_states = []
        for i in range(len(moves)):
            new_states.append(compute_states_after_moves(s, moves[i][1:5], player))
        return new_states

            


def compute_states_after_moves(state, moves, player):
    
    """Have to designed a function which take a state and list of moves 
    [[direction], x, y, nb, new x, new y] and return the new state"""
    
    w = state.width
    h = state.height
    s = state.state_list
    
    if player == "vampires":
        modif = []
        for i in range(len(moves)):
            for j in range(len(s)):
                print(i)
                print(j)
                if moves[i][3] == s[j][0] and moves[i][4] == s[j][1] and (s[j][2] != 0 or s[j][3] != 0 or s[j][4] != 0):
                    ### il y a bataille
                    ##### regarder si pas deja la case....
                    if s[j][2]!=0 and s[j][3]!= 0 and s[j][4]!= 0:
                        nb_vampires1, nb_humans = expected_gain_humans(moves[i][2] + s[j][3], s[j][2])
                        nb_vampires2, nb_werewolves = expected_gain_monsters(moves[i][2] + s[j][3], s[j][4])
                        modif.append([moves[i][3], moves[i][4], nb_humans, (nb_vampires1 + nb_vampires2)/2, nb_werewolves])
                        moves.remove(moves[i])
                    elif s[j][2]!=0 and s[j][4]!= 0:
                        nb_vampires1, nb_humans = expected_gain_humans(moves[i][2], s[j][2])
                        nb_vampires2, nb_werewolves = expected_gain_monsters(moves[i][2], s[j][4])
                        modif.append([moves[i][3], moves[i][4], nb_humans, (nb_vampires1 + nb_vampires2)/2, nb_werewolves])                       
                        moves.remove(moves[i])
                    elif s[j][2]!=0 and s[j][3]!= 0:
                        nb_vampires1, nb_humans = expected_gain_humans(moves[i][2] + s[j][3], s[j][2])
                        modif.append([moves[i][3], moves[i][4], nb_humans, nb_vampires1, 0])
                        moves.remove(moves[i])
                    elif s[j][3]!=0 and s[j][4]!= 0:
                        nb_vampires2, nb_werewolves = expected_gain_monsters(moves[i][2] + s[j][3], s[j][4])
                        modif.append([moves[i][3], moves[i][4], 0, nb_vampires2, nb_werewolves])
                        moves.remove(moves[i])
                    elif s[j][2]!=0:
                        nb_vampires1, nb_humans = expected_gain_humans(moves[i][2], s[j][2])
                        modif.append([moves[i][3], moves[i][4], nb_humans, nb_vampires1, 0])
                        moves.remove(moves[i])
                    elif s[j][3]!=0:
                        modif.append([moves[i][3], moves[i][4], 0, s[j][3], 0])
                        moves.remove(moves[i])
                    else:
                        nb_vampires2, nb_werewolves = expected_gain_monsters(moves[i][2], s[j][4])
                        modif.append([moves[i][3], moves[i][4], 0, nb_vampires2, nb_werewolves])
                        moves.remove(moves[i])
        for i in range(len(moves)):
            modif.append([moves[i][3], moves[i][4], 0, moves[i][2], 0])
        new_state = state.new_state(modif)
        return new_state
                    
 
    elif player == "werewolves":
        to_remove = []
        for i in range(len(moves)):
            for j in range(len(s)):
                if moves[i][3] == s[j][0] and moves[i][4] == s[j][1] and (s[j][2] != 0 or s[j][3] != 0):
                    if s[j][2]!=0 and s[j][3]!= 0:
                        nb_werewolves1, nb_humans = expected_gain_humans(moves[i][2] + s[j][4], s[j][2])
                        nb_werewolves2, nb_vampires = expected_gain_monsters(moves[i][2] + s[j][4], s[j][3])
                        s[j] = [moves[i][3], moves[i][4], nb_humans, nb_vampires, (nb_werewolves1 + nb_werewolves2)/2]                        
                    elif s[j][2]!= 0:
                        nb_werewolves1, nb_humans = expected_gain_humans(moves[i][2] + s[j][4], s[j][2])
                        s[j] = [moves[i][3], moves[i][4], nb_humans, 0, nb_werewolves1]
                    else:
                        nb_werewolves2, nb_vampires = expected_gain_monsters(moves[i][2] + s[j][4], s[j][3])
                        s[j] = [moves[i][3], moves[i][4], 0, nb_vampires, nb_werewolves2]
                elif moves[i][0] == s[j][0] and moves[i][1] == s[j][1]:
                    to_remove.append(s[j])      
                    s.append([moves[i][3], moves[i][4], 0, 0, moves[i][2]])
        new_state = [s[i] for i in range(len(s)) if s[i] not in to_remove] 
        return st.State(new_state, w, h)
                    
                    
                    
        
    




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
            sl = state.state_list
            s_for_h = []
            for i in range(len(sl)):
                if len(sl[i]) == 5:
                    s_for_h.append(sl[i])
                else:
                    s_for_h.append(sl[i][1:6])
            hstate = st.State(s_for_h, w, h)
            return [heuristic(hstate, player), state]
        depth +=1
        v = -10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mn = min_value(state, alpha, beta, "werewolves", depth, depth_max)
            v = max(v, mn[0])
            if v >= beta:
                return [v, suc]
            alpha = max(alpha, v)
        return [v, suc]
    elif player == "werewolves":
        if depth == depth_max:
            sl = state.state_list
            s_for_h = []
            for i in range(len(sl)):
                if len(sl[i]) == 5:
                    s_for_h.append(sl[i])
                else:
                    s_for_h.append(sl[i][1:6])
            hstate = st.State(s_for_h, w, h)
            return [heuristic(hstate, player), state]
        depth+=1
        v = -10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mn = min_value(state, alpha, beta, "vampires", depth, depth_max)
            v = max(v, mn[0])
            if v >= beta:
                return [v, suc]
            alpha = max(alpha, v)
        return [v, suc]

               
def min_value(state, alpha, beta, player, depth, depth_max):
    w = state.width
    h = state.height
    if player == "vampires":
        if depth == depth_max:
            sl = state.state_list
            s_for_h = []
            for i in range(len(sl)):
                if len(sl[i]) == 5:
                    s_for_h.append(sl[i])
                else:
                    s_for_h.append(sl[i][1:6])
            hstate = st.State(s_for_h, w, h)
            return [heuristic(hstate, player), state]
        depth+=1
        v = +10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mx = max_value(state, alpha, beta, "vampires", depth, depth_max)
            v = min(v, mx[0])
            if v >= beta:
                return [v, suc]
            beta = min(beta, v)
        return [v, suc]
    elif player == "werewolves":
        if depth == depth_max:
            sl = state.state_list
            s_for_h = []
            for i in range(len(sl)):
                if len(sl[i]) == 5:
                    s_for_h.append(sl[i])
                else:
                    s_for_h.append(sl[i][1:6])
            hstate = st.State(s_for_h, w, h)
            return [heuristic(hstate, player), state]
        depth+=1
        v = +10**99
        successors = compute_successors(state, player)
        for suc in successors:
            mx = max_value(state, alpha, beta, "werewolves", depth, depth_max)
            v = min(v, mx[0])
            if v >= beta:
                return [v, suc]
            beta = min(beta, v)
        return [v, suc]
    

def heuristic(state, player):
    if player == "vampires":
        return state.get_nb_vampires() - (state.get_nb_humans() + state.get_nb_werewolves())
    elif player == "werewolves":
        return state.get_nb_werewolves() - (state.get_nb_humans() + state.get_nb_vampires())
        

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
state = st.State([[9, 0, 2, 0, 0], [4, 1, 0, 4, 0], [4, 2, 5, 0, 0], [2, 3, 0, 7, 0], [9, 4, 2, 0, 0], [1, 4, 0, 4, 0]], 10, 5)           
state2 = st.State( [[9, 0, 2, 0, 0], [4, 2, 0, 4, 0], [2, 2, 0, 11, 0], [9, 4, 2, 0, 0], [1, 4, 0, 4, 0] ] , 10, 5)           
player = "vampires"
a = compute_successors(state, player)
#print(a)
depth = 0
depth_max = 4
#b = max_value(state, alpha, beta, player, depth, depth_max) 
#print(b)
t2 = time.time()
print(t1-t2)