# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 00:35:43 2018

@author: assae
"""

def split_in_chunks(flat_state_list):
    """Method which take a tuple (a state_list) with n*5 elements and return
    a list of n lists of 5 elements, these 5 elements being :
    (position x, position y, nb_humans, nb_vampires, nb_werewolves)"""
    state_in_chunk = []
    for i in range(0, len(flat_state_list), 5):
        state_in_chunk.append(list(flat_state_list[i:i+5]))
    return state_in_chunk

def flat_list(liste):
    """Method which take a list of lists and return a flat list"""
    flat = [item for sublist in liste for item in sublist]
    return flat




class State():
    """This class represents a state, as in a grid configuration.
    It is a list of lists of 5 numbers.
    Each chunk of 5 numbers reprensents a non-empty cell of the grid 
    (position x, position y, nb_humans, nb_vampires, nb_werewolves)"""

    def __init__(self, state_list):
        self.state_list = state_list
         
    def __repr__(self):
        """Special method to print a state in a pretty way"""
        return str(self.state_list)


    def new_state(self, modifications):
        """Methods which takes a state and a set of modifications, being a list of lists 
        of 5 elements reprenting cells which have been modified. It updates the state into a new one,
        taking into account these modifications"""
        old_state = self.state_list
        old_length = len(old_state)
        new_state = old_state.copy()
        modif_length = len(modifications)
        
        for i in range(modif_length):
            for j in range(old_length):
                if modifications[i][0] == old_state[j][0] and modifications[i][1] == old_state[j][1]:
                    new_state[j] = modifications[i]
        return State(new_state)
    
    def get_humans_list(self):
        """Method which takes a state and return a list of lists of 3 elements being
        (position x, position y, nb_humans)"""
        humans_list = []
        for i in range(len(self.state_list)):
            if self.state_list[i][2] != 0:
                humans_list.append([self.state_list[i][0], self.state_list[i][1], self.state_list[i][2]])
        return humans_list
    
    def get_nb_humans(self):
        """Method which takes a state and return the number of humans on the board"""
        count = 0
        for i in range(len(self.state_list)):
            if self.state_list[i][2] != 0:
                count += self.state_list[i][2]
        return count
    
    def get_vampires_list(self):
        """Method which takes a state and return a list of lists of 3 elements being
        (position x, position y, nb_vampires)"""
        vampires_list = []
        for i in range(len(self.state_list)):
            if self.state_list[i][3] != 0:
                vampires_list.append([self.state_list[i][0], self.state_list[i][1], self.state_list[i][3]])
        return vampires_list
    
    def get_nb_vampires(self):
        """Method which takes a state and return the number of vampires on the board"""
        count = 0
        for i in range(len(self.state_list)):
            if self.state_list[i][3] != 0:
                count += self.state_list[i][3]
        return count
    
    def get_werewolves_list(self):
        """Method which takes a state and return a list of lists of 3 elements being
        (position x, position y, nb_werewolves)"""
        werewolves_list = []
        for i in range(len(self.state_list)):
            if self.state_list[i][4] != 0:
                werewolves_list.append([self.state_list[i][0], self.state_list[i][1], self.state_list[i][4]])
        return werewolves_list
    
    def get_nb_werewolves(self):
        """Method which takes a state and return the number of werewolves on the board"""
        count = 0
        for i in range(len(self.state_list)):
            if self.state_list[i][4] != 0:
                count += self.state_list[i][4]
        return count


    def compute_heuristic(self, player):
        """Method which take a state and return the associated heuristic"""
        if player == "vampires":
            return self.get_nb_vampires - self.get_nb_werewolves
        elif player == "werewolves":
            return self.get_nb_werewolves - self.get_nb_vampires
            
    
    
#Trials

#test = State([[9, 0, 2, 0, 0], [4, 1, 0, 0, 4],  [2, 2, 4, 0, 0],  [9, 2, 1, 0, 0],  [4, 3, 0, 4, 0], [9, 4, 2, 0, 0]] )  
#print(test.get_humans_list())
#print(test.get_nb_humans())
#print(test.get_vampires_list())
#print(test.get_nb_vampires())
#print(test.get_werewolves_list())
#print(test.get_nb_werewolves())
#test2 = test.new_state([[4, 1, 0, 0, 124],  [2, 2, 0, 60, 0]])
#print(test2)
#print(test2.get_nb_vampires())
#print(test2.get_nb_werewolves())

