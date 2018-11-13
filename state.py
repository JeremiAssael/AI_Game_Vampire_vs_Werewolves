# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 00:35:43 2018

@author: assae
"""
import itertools
import operator
#import math

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
    

#def helper_enumerate(nb_players, nb_cells):
#    """Propose a list of lists which are every manner to put nb_players players in nb_cells cells. """
##    nb_possibilities = int(math.factorial(nb_players + nb_cells -1)/(math.factorial(nb_players) * math.factorial(nb_cells-1)))
#    rng = list(range(nb_players + 1)) * nb_cells
#    permutations = list(set(i for i in itertools.permutations(rng, nb_cells) if sum(i) == nb_players))
#    return permutations



def helper_enumerate(nb_players, nb_cells):
    """Propose a list of lists which are every manner to put nb_players players in nb_cells cells. """
    def combinations_with_replacement_counts(nb_cells, nb_players):
        size = nb_cells + nb_players - 1
        for indices in itertools.combinations(range(size), nb_cells-1):
            starts = [0] + [index+1 for index in indices]
            stops = indices + (size,)
            yield tuple(map(operator.sub, stops, starts))
    return list(combinations_with_replacement_counts(nb_cells, nb_players))


def allowed_moves(position, width, height):
    """A function which return all cells which can be reached from the current one, including this one"""
    x = position[0]
    y = position[1]
    h = height
    w = width
    moves_list = []  
    if x >= w or y >= h:
        print("Position error")
        return None
    elif x == 0 and y == 0:
        moves_list.extend(((x,y), (x+1,y), (x, y+1), (x+1, y+1)))
        return moves_list
    elif x == w-1 and y == 0:
        moves_list.extend((((x,y), (x-1,y), (x, y+1), (x-1, y+1))))
        return moves_list
    elif x == 0 and y == h-1:
        moves_list.extend(((x,y), (x+1,y), (x, y-1), (x+1, y-1)))
        return moves_list
    elif x == w-1 and y == h-1:
        moves_list.extend(((x,y), (x-1,y), (x, y-1), (x-1, y-1)))
        return moves_list
    elif x == 0 and y != 0 and y != h-1:
        moves_list.extend(((x,y), (x,y+1), (x, y-1), (x+1, y), (x+1, y-1), (x+1, y+1)))
        return moves_list
    elif x == w-1 and y != 0 and y != h-1:
        moves_list.extend(((x,y), (x,y+1), (x, y-1), (x-1, y), (x-1, y-1), (x-1, y+1)))
        return moves_list
    elif x != 0 and x != w-1 and y == 0:
        moves_list.extend(((x,y), (x,y+1), (x+1, y), (x+1, y+1), (x-1, y), (x-1, y+1)))
        return moves_list
    elif x != 0 and x != w-1 and y == h-1:
        moves_list.extend(((x,y), (x,y-1), (x+1, y), (x+1, y-1), (x-1, y), (x-1, y-1)))
        return moves_list
    else:
        moves_list.extend(((x,y), (x,y-1), (x, y+1), (x+1, y), (x+1, y-1), (x+1, y+1), (x-1, y), (x-1, y-1), (x-1, y+1)))
        return moves_list


def moves_from_cell_players(nb_players, cell_position, width, height):
    """Function which returns all possibiities to put nb_players players from the current 
    cell in cell_position. Its a list of lists, each secondary list being a proposal.
    Each set is (positon x, positon y, nb_players there)"""
    moves = allowed_moves(cell_position, width, height)
    nb_cells = len(moves)
    possibilities = helper_enumerate(nb_players, nb_cells)
    possible_moves =[]
    for item in possibilities:
        new_item = [(moves[i][0], moves[i][1], item[i]) for i in range(nb_cells)]
        possible_moves.append(new_item)
    return possible_moves
    
        

class State():
    """This class represents a state, as in a grid configuration.
    It is a list of lists of 5 numbers.
    Each chunk of 5 numbers reprensents a non-empty cell of the grid 
    (position x, position y, nb_humans, nb_vampires, nb_werewolves)
    height and width are the dimensions of the grid"""

    def __init__(self, state_list, height, width):
        self.state_list = state_list
        self.height = height
        self. width = width
         
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
        return State(new_state, self.height, self.width)
    
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
    
    def get_all_children(self, player):
        """Method which takes a state and return all states deriving from this one
        It considers each cells where our players are and each possible combinations in available cells
        For instance if we have 3 players in an inside cell, there are 9 cells possible for these players, so
        9-1 among 9+3-1 possibilities"""
#        all_children = []
#        w = self.width
#        h = self.height
#        
#        if player == "vampires":
#            for cell in self.get_vampires_list():
#                if cell[0] == 0 and cell[1] == 0:
##                    4 cases
#                    pass
#                elif cell[0] == w-1 and cell[1] == 0:
##                    4 cases
#                    pass
#                elif cell[0] == 0 and cell[1] == h-1:
##                    4 cases
#                    pass
#                elif cell[0] == w-1 and cell[1] == h-1:
##                    4 cases
#                    pass
#                elif cell[0] == 0 and cell[1] != 0 and cell[1] != h-1:
##                    6 cases
#                    pass
#                elif cell[0] == w-1 and cell[1] != 0 and cell[1] != h-1:
##                    6 cases
#                    pass
#                elif cell[0] != 0 and cell[0] != w-1 and cell[1] == 0:
##                    6 cases   
#                    pass
#                elif cell[0] != 0 and cell[0] != w-1 and cell[1] == h-1:
##                    6 cases
#                    pass
#                else:
##                    9 cases
#                    pass
#                
#        elif player == "werwolves":
#            for cell in self.get_werewolves_list():
#                for i in range(cell[2]+1):
#                    pass
#        else:
#            print("vampires or werewolves must be provided as player")


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

