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
        self.children = {}
        
    def number_children(self):
        """Get the number of children of a node"""
        return len(self.children)
    
    def add_child(self, child, heuristic=None):
        """Add a child to a node"""
        self.children[child.identif] = child.heuristic
        
    def display_children(self, depth = 0):
        """Method allowing to display all the chidren and further sucessors of a 
        specific node in a kind a tree-looking"""
        if len(self.children) != 0:
            depth += 1
            for nd in self.children:
#                node = Node(nd, self.children[nd])
                print(depth * "\t" + nd)
                nd.display_children(depth)
    
    def __repr__(self):
        """Special method to print a node in a pretty way"""
        return "{0} : {1}".format(self.identif, self.heuristic)
    
#root = nde.Node("root", 0.45)
#c= nde.Node("c", 2.34)
#d= nde.Node("d", 56)
#e= nde.Node("e", 87)
#f= nde.Node("f", 78)
#g = nde.Node("g", 67)
#h = nde.Node("h", 698)
#root.add_child(c, 2.34)
#tree.add_node(d, c)
#tree.add_node(e, root)
#tree.add_node(f, e)
#tree.add_node(g, c)
#tree.add_node(h, d)