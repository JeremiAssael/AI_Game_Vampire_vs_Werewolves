# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 01:03:11 2018

@author: assae
"""

class Node():
    """Create a node of a tree, stating all of is child in a dictionary in which values
        are a tuple (cost of the branch toward this child, cost on the child node)"""
    
    def __init__(self, identif, heuristic = None):
        self.identif = identif
        self.heuristic = heuristic
        self.children = []
        
    def number_children(self):
        """Get the number of children of a node"""
        return len(self.children)
    
    def add_child(self, child):
        """Add a child to a node"""
        self.children.append(child)
        
    def display_children(self, depth = 0):
        """Method allowing to display all the chidren and further sucessors of a 
        specific node in a kind a tree-looking"""
        if len(self.children) != 0:
            depth += 1
            for nd in self.children:
                print(depth * "\t" + str(nd))
                nd.display_children(depth)
    
    def __repr__(self):
        """Special method to print a node in a pretty way"""
        return "{0} : {1}".format(self.identif, self.heuristic)