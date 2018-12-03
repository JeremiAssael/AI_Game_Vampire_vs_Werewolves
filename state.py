# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 16:39:02 2018

@author: assae
"""

import random
import tree
import node


def split_in_chunks(flat_state_list):
    """Method which take a tuple (a state_list) with n*5 elements and return
    a list of n lists of 5 elements, these 5 elements being :
    (position x, position y, nb_humans, nb_vampires, nb_werewolves)"""
    state_in_chunk = []
    for i in range(0, len(flat_state_list), 5):
        state_in_chunk.append(list(flat_state_list[i:i+5]))
    return state_in_chunk

        

class State():
    """This class represents a state, as in a grid configuration.
    It is a list of lists of 5 numbers.
    Each chunk of 5 numbers reprensents a non-empty cell of the grid 
    (position x, position y, nb_humans, nb_vampires, nb_werewolves).
    height and width are the dimensions of the grid"""

    def __init__(self, state_list, width, height):
        self.state_list = state_list
        self.width = width
        self.height = height
         
    def __repr__(self):
        """Special method to print a state in a pretty way"""
        return str(self.state_list)


    def new_state(self, modifications):
        """Methods which takes a state and a set of modifications, being a list of lists 
        of 5 elements reprenting cells which have been modified. It updates the state into a new one,
        taking into account these modifications"""
        old_state = self.state_list
        old_length = len(old_state)
        modif_to_delete = []
        new_state_to_delete = []
        new_state_to_add = []
        new_state = old_state.copy()
        modif_length = len(modifications)
        for i in range(modif_length):
            for j in range(old_length):
                if modifications[i][0] == old_state[j][0] and modifications[i][1] == old_state[j][1]:
                    new_state_to_delete.append(old_state[j])
                    new_state_to_add.append(modifications[i])
                    modif_to_delete.append(modifications[i])
        new_state.extend(new_state_to_add)
        new_state = [ns for ns in new_state if ns not in new_state_to_delete]
        remaining_modifs = [modif for modif in modifications if modif not in modif_to_delete]
        new_state.extend(remaining_modifs)
        ns = new_state.copy()
        for i in range(len(new_state)):
            if new_state[i][2] == 0 and new_state[i][3] == 0 and new_state[i][4] == 0:
                ns.pop(i)
        new_state = ns
        return State(new_state, self.width, self.height)
    
    def random_moves(self, player):
        h = self.height
        w = self.width
        moves_list = []
        if player == "vampires":
            vampires_list = self.get_vampires_list()
            x = vampires_list[0][0]
            y = vampires_list[0][1]
            nb_players = vampires_list[0][2]
            if x >= w or y >= h:
                print("Position error")
            elif (x == 0 and y == 0):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x+1, y+1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == w-1 and y == 0):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x-1, y+1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == 0 and y == h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y-1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == w-1 and y == h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y-1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == 0 and y != 0 and y != h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y ], [x, y, nb_players, x+1, y-1], [x, y, nb_players, x+1, y+1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            elif (x == w-1 and y != 0 and y != h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y-1], [x, y, nb_players, x-1, y+1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            elif (x != 0 and x != w-1 and y == 0):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x+1, y], [x, y, nb_players, x+1, y+1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y+1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            elif (x != 0 and x != w-1 and y == h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            else:
                moves_list.extend([[x, y, nb_players, x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x, y+1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x+1, y+1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1], [x, y, nb_players,x-1, y+1]])
                choice = random.randint(1,8)
                return list(moves_list[choice])
        elif player == "werewolves":
            werewolves_list = self.get_werewolves_list()
            x = werewolves_list[0][0]
            y = werewolves_list[0][1]
            nb_players = werewolves_list[0][2]
            if x >= w or y >= h:
                print("Position error")
            elif (x == 0 and y == 0):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x+1, y+1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == w-1 and y == 0):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x-1, y+1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == 0 and y == h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y-1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == w-1 and y == h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y-1]])
                choice = random.randint(1,3)
                return list(moves_list[choice])
            elif (x == 0 and y != 0 and y != h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y ], [x, y, nb_players, x+1, y-1], [x, y, nb_players, x+1, y+1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            elif (x == w-1 and y != 0 and y != h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y-1], [x, y, nb_players, x-1, y+1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            elif (x != 0 and x != w-1 and y == 0):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x+1, y], [x, y, nb_players, x+1, y+1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y+1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            elif (x != 0 and x != w-1 and y == h-1):
                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1]])
                choice = random.randint(1,5)
                return list(moves_list[choice])
            else:
                moves_list.extend([[x, y, nb_players, x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x, y+1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x+1, y+1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1], [x, y, nb_players,x-1, y+1]])
                choice = random.randint(1,8)
                return list(moves_list[choice])
            
            
    
        
    
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
    
    def compute_movement_score(self, move, player):
        """Method which take a state and return the associated heuristic"""
        score = 100
        if player == "vampires":
            v_list = self.get_vampires_list()
            part_1 = self.get_nb_vampires() - self.get_nb_werewolves()
            w_list = self.get_werewolves_list()
            h_list = self.get_humans_list()
            list_vectors_werewolves = []
            list_vectors_humans = []
            list_ps_werewolves = []
            list_ps_humans = []
            for i in range(len(w_list)):
                vect = [w_list[i][0]-move[0][3], w_list[i][1]-move[0][4]]
                list_vectors_werewolves.append(vect)
            for h in range(len(h_list)):
                vect = [h_list[h][0]-move[0][3], h_list[h][1]-move[0][4]]
                list_vectors_humans.append(vect)
            for i in range(len(list_vectors_humans)):
                vect = 3
                
            
        elif player == "werewolves":
            part_1 =  self.get_nb_werewolves() - self.get_nb_vampires()
        


#    def moves(self, player):
#        h = self.height
#        w = self.width
#        moves_list = []
#        if player == "vampires":
#            vampires_list = self.get_vampires_list()
#            x = vampires_list[0][0]
#            y = vampires_list[0][1]
#            nb_players = vampires_list[0][2]
#            if x >= w or y >= h:
#                print("Position error")
#            elif (x == 0 and y == 0):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x+1, y+1]])
#                return moves_list[1:4]
#            elif (x == w-1 and y == 0):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x-1, y+1]])
#                return moves_list[1:4]
#            elif (x == 0 and y == h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y-1]])
#                return moves_list[1:4]
#            elif (x == w-1 and y == h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y-1]])
#                return moves_list[1:4]
#            elif (x == 0 and y != 0 and y != h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y ], [x, y, nb_players, x+1, y-1], [x, y, nb_players, x+1, y+1]])
#                return moves_list[1:6]
#            elif (x == w-1 and y != 0 and y != h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y-1], [x, y, nb_players, x-1, y+1]])
#                return moves_list[1:6]
#            elif (x != 0 and x != w-1 and y == 0):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x+1, y], [x, y, nb_players, x+1, y+1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y+1]])
#                return moves_list[1:6]
#            elif (x != 0 and x != w-1 and y == h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1]])
#                return moves_list[1:6]
#            else:
#                moves_list.extend([[x, y, nb_players, x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x, y+1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x+1, y+1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1], [x, y, nb_players,x-1, y+1]])
#                return moves_list[1:9]
#        elif player == "werewolves":
#            werewolves_list = self.get_werewolves_list()
#            x = werewolves_list[0][0]
#            y = werewolves_list[0][1]
#            nb_players = werewolves_list[0][2]
#            if x >= w or y >= h:
#                print("Position error")
#            elif (x == 0 and y == 0):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x+1, y+1]])
#                return moves_list[1:4]
#            elif (x == w-1 and y == 0):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y+1], [x, y, nb_players, x-1, y+1]])
#                return moves_list[1:4]
#            elif (x == 0 and y == h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x+1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y-1]])
#                return moves_list[1:4]
#            elif (x == w-1 and y == h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x-1,y], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y-1]])
#                return moves_list[1:4]
#            elif (x == 0 and y != 0 and y != h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x+1, y ], [x, y, nb_players, x+1, y-1], [x, y, nb_players, x+1, y+1]])
#                return moves_list[1:6]
#            elif (x == w-1 and y != 0 and y != h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x, y-1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y-1], [x, y, nb_players, x-1, y+1]])
#                return moves_list[1:6]
#            elif (x != 0 and x != w-1 and y == 0):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players, x,y+1], [x, y, nb_players, x+1, y], [x, y, nb_players, x+1, y+1], [x, y, nb_players, x-1, y], [x, y, nb_players, x-1, y+1]])
#                return moves_list[1:6]
#            elif (x != 0 and x != w-1 and y == h-1):
#                moves_list.extend([[x, y, nb_players,x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1]])
#                return moves_list[1:6]
#            else:
#                moves_list.extend([[x, y, nb_players, x,y], [x, y, nb_players,x,y-1], [x, y, nb_players,x, y+1], [x, y, nb_players,x+1, y], [x, y, nb_players,x+1, y-1], [x, y, nb_players,x+1, y+1], [x, y, nb_players,x-1, y], [x, y, nb_players,x-1, y-1], [x, y, nb_players,x-1, y+1]])
#                return moves_list[1:9]


#    def get_basic_graph(self, player, depth):
#        """Build a complete graphe of depth 2. Depth 2: Me (=root), you, me"""
#        """Idée: pas creer d'arbre. Juste node et add childre. Arbre dans le dernier return"""
#        if depth != 0:
#            if player=="vampires":
#                print(1)
#                self_node = node.Node(self)
#                moves = self.moves("vampires")
#                states_list = []
#                for i in range(len(moves)):
#                    state_after_move = self.new_state([moves[i]])
#                    states_list.append(node.Node(state_after_move))
#                    self_node.add_children(states_list)
#                depth = depth - 1
#                for nde in self_node.children:
#                    nde.state.get_basic_graph("werewolves", depth)   
#        
#            elif player=="werewolves":
#                print(2)
#                self_node = node.Node(self)
#                moves = self.moves("werewolves")
#                states_list = []
#                for i in range(len(moves)):
#                    state_after_move = self.new_state([moves[i]])
#                    states_list.append(node.Node(state_after_move))
#                    self_node.add_children(states_list)
#                depth = depth - 1
#                for nde in self_node.children:
#                    nde.state.get_basic_graph("vampires", depth)
#        else:
#            game_tree = tree.Tree()
#            game_tree.add_nodes(node.Node(self))
#            return game_tree
                
                

                
            
        
    
            
    

