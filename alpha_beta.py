# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:58:03 2019

@author: assae
"""

import compute_successors as cs
import state as st
import random
import time


def heuristic(state, player):
    return random.randint(0, 100)

def max_value(state, alpha, beta, player, depth, depth_max):
    """let's do alpha beta knowing the particular way of describing a state succesor"""

    
    if player == "vampires":
        if depth == depth_max:
            """we kept the directions in the states so that they are easy to 
            find, we have to remove them to compute the heuristic"""
            return [state[0]*heuristic(state[2], player), state[1], state[2]]
        depth +=1
        v = -10**99
        best_direction = None
        best_state = None
        successors = cs.compute_successors(state[2], player)
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            min_list = min_value(suc, alpha, beta, "werewolves", depth, depth_max)
            if min_list[0] > v:
                v = min_list[0]
                best_direction = considered_direction
                best_state = considered_state
            if v >= beta:
                return [v, best_direction, best_state]
            alpha = max(alpha, v)
        return [v, best_direction, best_state]
    
    elif player == "werewolves":
        if depth == depth_max:
            return [state[0]*heuristic(state[2], player), state[1], state[2]]
        depth+=1
        v = -10**99
        best_direction = None
        best_state = None
        successors = cs.compute_successors(state[2], player)
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            min_list = min_value(suc, alpha, beta, "vampires", depth, depth_max)
            if min_list[0] > v:
                v = min_list[0]
                best_direction = considered_direction
                best_state = considered_state
            if v >= beta:
                return [v, best_direction, best_state]
            alpha = max(alpha, v)
        return [v, best_direction, best_state]


               
def min_value(state, alpha, beta, player, depth, depth_max):
    
    
    if player == "vampires":
        if depth == depth_max:
            return [state[0]*heuristic(state[2], player), state[1], state[2]]
        depth+=1
        v = +10**99
        best_direction = None
        best_state = None
        successors = cs.compute_successors(state[2], player)
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            max_list = max_value(suc, alpha, beta, "werewolves", depth, depth_max)
            if max_list[0] < v:
                v = max_list[0]
                best_direction = considered_direction
                best_state = considered_state
            if v >= beta:
                return [v, best_direction, best_state]
            beta = min(beta, v)
        return [v, best_direction, best_state]
    
    elif player == "werewolves":
        if depth == depth_max:
            return [state[0]*heuristic(state[2], player), state[1], state[2]]
        depth+=1
        v = +10**99
        best_direction = None
        best_state = None
        successors = cs.compute_successors(state[2], player)
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            max_list = max_value(suc, alpha, beta, "vampires", depth, depth_max)
            if max_list[0] < v:
                v = max_list[0]
                best_direction = considered_direction
                best_state = considered_state
            if v >= beta:
                return [v, best_direction, best_state]
            beta = min(beta, v)
        return [v, best_direction, best_state]


def preprocessing_before_alphabeta(state):
    return [1,1, state]
    
    
def from_direction_to_move(alpha_beta_result, intermediary_state, player):
    directions = alpha_beta_result[1]
    final = []
    if player == "vampires":
        vamp_list = intermediary_state.get_vampires_list()
        for i in range(len(vamp_list)):
            final.append([vamp_list[i][0], vamp_list[i][1], vamp_list[i][2], vamp_list[i][0]+directions[i][0], vamp_list[i][1]-directions[i][1]])
        return final
    elif player == "werewolves":
        were_list = intermediary_state.get_werewolves_list()
        for i in range(len(were_list)):
            final.append([were_list[i][0], were_list[i][1], were_list[i][2], were_list[i][0]+directions[i][0], were_list[i][1]-directions[i][1]])
        return final
 
       
def compute_best_direction(state, alpha, beta, player, depth, depth_max):
    st_pre = preprocessing_before_alphabeta(state)
    alph_bet = max_value(st_pre, alpha, beta, player, depth, depth_max) 
    final = from_direction_to_move(alph_bet, state, player)
    return final
    
    
    
t1 = time.time()
alpha = -10**99
beta = 10**99  
state = st.State([[4, 1, 0, 9, 0], [9, 0, 3, 0, 0], [2, 3, 4, 0, 0], [9, 4, 0, 4, 0], [1, 4, 0, 0, 4]], 10, 5)           
state2 = st.State( [[9, 0, 2, 0, 0], [4, 2, 0, 4, 0], [2, 2, 0, 11, 0], [9, 4, 2, 0, 0], [1, 4, 0, 4, 0] ] , 10, 5)           
player = "vampires"
moves  = [[[1, 0], [6,7,4,7,7]], [[0, 1], [4,2,5,4,1]], [[0, -1],[1,4,2,1,5]]]
modifs = [[[0.75, [4, 1, 0, 4, 0]], [0.25, [4, 1, 0, 0, 1]]], [[0.65, [4, 1, 0, 4, 0]], [0.35, [4, 1, 0, 0, 1]]], [1, [7, 7, 0, 4, 0]], [1, [1, 5, 0, 2, 0]], [1, [4, 1, 0, 0, 4]], [1, [2, 3, 4, 0, 0]], [1, [5, 8, 0, 4, 0]], [1, [1, 4, 0, 2, 0]]]
depth = 0
depth_max = 4
b = compute_best_direction(state, alpha, beta, player, depth, depth_max)
print(b)
t2 = time.time()
print(t2-t1)