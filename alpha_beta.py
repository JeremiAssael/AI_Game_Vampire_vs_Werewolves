# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 14:58:03 2019

@author: assae
"""

import compute_successors as cs
import state as st
import random
import time
import heuristic




#def heuristic(state, player):
#    return random.randint(0, 100)

def max_value(state, alpha, beta, player, depth, depth_max, best_direction=None, best_state=None):
    """let's do alpha beta knowing the particular way of describing a state succesor"""
    if player == "vampires":
        if depth == depth_max:
            """we kept the directions in the states so that they are easy to 
            find, we have to remove them to compute the heuristic"""
            return [state[0]*heuristic.compute_score_state(state[2], player), state[1], state[2]]
#            return [state[0]*random.randint(0, 100), state[1], state[2]]
        depth +=1
        v = -10**99
        successors = cs.compute_successors(state[2], player)
        memory = []
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            min_list = min_value(suc, alpha, beta, "werewolves", depth, depth_max, considered_direction, considered_state)
            memory.append([min_list[0], suc[1], suc[2]])
            if min_list[0] > v:
                v = min_list[0]
            if v >= beta:
                if depth == 1:
                    print("Cut", depth, sort_by_first(memory))
                    #print("Cut", heuristic.compute_score_state(best_state, player, print_heuristic = True))
                return sort_by_first_return(memory)
            alpha = max(alpha, v)
#        print(best_direction)
        if depth == 1:
            print("End", depth, sort_by_first(memory)) 
        return sort_by_first_return(memory)
    
    elif player == "werewolves":
        if depth == depth_max:
            return [state[0]*heuristic.compute_score_state(state[2], player), state[1], state[2]]
#            return [state[0]*random.randint(0, 100), state[1], state[2]]
        depth+=1
        v = -10**99
        successors = cs.compute_successors(state[2], player)
        memory = []
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            min_list = min_value(suc, alpha, beta, "vampires", depth, depth_max, considered_direction, considered_state)
            memory.append([min_list[0], suc[1], suc[2]])
            if min_list[0] > v:
                v = min_list[0]
            if v >= beta:
                print(sort_by_first_return(memory))
                return sort_by_first_return(memory)
            alpha = max(alpha, v)
#        print(best_direction)
        print(sort_by_first_return(memory))
        return sort_by_first_return(memory)

               
def min_value(state, alpha, beta, player, depth, depth_max, best_direction=None, best_state=None):
    
    if player == "vampires":
        if depth == depth_max:
            return [state[0]*heuristic.compute_score_state(state[2], player), state[1], state[2]]
#            return [state[0]*random.randint(0, 100), state[1], state[2]]
        depth+=1
        v = +10**99
        successors = cs.compute_successors(state[2], player)
        memory = []
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            max_list = max_value(suc, alpha, beta, "werewolves", depth, depth_max, considered_direction, considered_state)
            memory.append([max_list[0], suc[1], suc[2]])
            if max_list[0] < v:
                v = max_list[0]
            if alpha >= v:
                return sort_by_last_return(memory)
            beta = min(beta, v)
#        print(best_direction)
        return sort_by_last_return(memory)
    
    elif player == "werewolves":
        if depth == depth_max:
            return [state[0]*heuristic.compute_score_state(state[2], player), state[1], state[2]]
#            return [state[0]*random.randint(0, 100), state[1], state[2]]
        depth+=1
        v = +10**99
        successors = cs.compute_successors(state[2], player)
        memory = []
        for suc in successors:
            considered_direction = suc[1]
            considered_state = suc[2]
            max_list = max_value(suc, alpha, beta, "vampires", depth, depth_max, considered_direction, considered_state)
            memory.append([max_list[0], suc[1], suc[2]])
            if max_list[0] < v:
                v = max_list[0]
            if alpha >= v:
                return sort_by_last_return(memory)
            beta = min(beta, v)
        return sort_by_last_return(memory)



def sort_by_first_return(liste):
    def takeFirst(liste):
        return(liste[0])
        
        
    liste = sorted(liste, reverse=True, key=takeFirst)
    
    return liste[0]


def sort_by_first(liste):
    def takeFirst(liste):
        return(liste[0])
        
        
    liste = sorted(liste, reverse=True, key=takeFirst)
    
    return liste


def sort_by_last_return(liste):
    def takeFirst(liste):
        return(liste[0])
        
        
    liste = sorted(liste, reverse=True, key=takeFirst)
    
    return liste[-1]


def sort_by_last(liste):
    def takeFirst(liste):
        return(liste[0])
        
        
    liste = sorted(liste, reverse=True, key=takeFirst)
    
    return liste


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
    alph_bet = max_value(st_pre, alpha, beta, player, depth, depth_max, best_direction=None, best_state=None) 
    final = from_direction_to_move(alph_bet, state, player)
    return final
 


def direction_only_zero(state, player):
    def takeFirst(elem):
        return elem[0]
    
    suc = cs.compute_successors(state, player)
    list_proposition = []
    for s in suc:
        list_proposition.append([s[0]*heuristic.compute_score_state(s[2], player), s[1], s[2]])
    list_proposition = sorted(list_proposition, reverse=True, key=takeFirst)
#    print(list_proposition)
    print("SOLUTION:")
    print(heuristic.compute_score_state(list_proposition[0][2], player, print_heuristic = True))
    print(from_direction_to_move(list_proposition[0], state, player))
    return from_direction_to_move(list_proposition[0], state, player)
    
    
#    
#t1 = time.time()
#alpha = -10**99
#beta = 10**99  
#state = st.State([[4, 1, 0, 9, 0], [9, 0, 3, 0, 0], [2, 3, 4, 0, 0], [9, 4, 0, 4, 0], [1, 4, 0, 0, 4]], 10, 5)           
#state2 = st.State( [[9, 0, 2, 0, 0], [4, 2, 0, 4, 0], [2, 2, 0, 11, 0], [9, 4, 2, 0, 0], [1, 4, 0, 4, 0] ] , 10, 5)           
#player = "vampires"
#moves  = [[[1, 0], [6,7,4,7,7]], [[0, 1], [4,2,5,4,1]], [[0, -1],[1,4,2,1,5]]]
#modifs = [[[0.75, [4, 1, 0, 4, 0]], [0.25, [4, 1, 0, 0, 1]]], [[0.65, [4, 1, 0, 4, 0]], [0.35, [4, 1, 0, 0, 1]]], [1, [7, 7, 0, 4, 0]], [1, [1, 5, 0, 2, 0]], [1, [4, 1, 0, 0, 4]], [1, [2, 3, 4, 0, 0]], [1, [5, 8, 0, 4, 0]], [1, [1, 4, 0, 2, 0]]]
#depth = 0
#depth_max = 2
#b = compute_best_direction(state, alpha, beta, player, depth, depth_max)
#print(b)
#t2 = time.time()
#print(t2-t1)