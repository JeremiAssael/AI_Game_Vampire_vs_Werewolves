# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 13:07:38 2018

@author: assae
"""
 
import node as nde

class Tree():
    """Create a tree, defined by a list of nodes. The children of these nodes are 
    inside the node object"""
    
    def __init__(self, root):
        """A tree is build using just its roots. Nodes are added afterwards"""
        self.root = root
        self.nodes = [root]
        
    def add_node(self, node, parent):
        """Add a node to a tree, specifying the parent"""
        if parent in self.nodes:
            parent.add_child(node)
            self.nodes.append(node)
        else:
            print("An existing parent must be provided")
            
    def get_parent(self, node):
        """Get the parent of a specific node in a tree"""
        for nd in self.nodes:
            if node in nd.children:
                return nd
        return None
    
#    def is_leaf(self, node):
#        """Method stating if a node is a leaf of the tree"""
#        if node.number_children() == 0:
#            return True
#        else:
#            return False
            
    def display(self):
        """Display the tree in a pretty manner"""
        print(self.root)
        self.root.display_children()
                 
#    def max_value(self, node, alpha, beta):
#        if self.is_leaf(node):
#            return node.heuristic
#        v = -10**99
#        for cd in node.children:
#            v = max(v, self.min_value(node, alpha, beta))
#            if v >= beta:
#                return v
#            alpha = max(alpha, v)
#        return v
#                   
#    def min_value(self, node, alpha, beta):
#        if self.is_leaf(node):
#            return node.heuristic
#        v = +10**99
#        for cd in node.children:
#            v = min(v, self.max_value(node, alpha, beta))
#            if v >= beta:
#                return v
#            beta = max(beta, v)
#        return v


#Trials
    
#root = nde.Node("root", 0.45)
#tree = Tree(root)
#c= nde.Node("c", 2.34)
#d= nde.Node("d", 56)
#e= nde.Node("e", 87)
#f= nde.Node("f", 78)
#g = nde.Node("g", 67)
#h = nde.Node("h", 698)
#tree.add_node(c, root)
#tree.add_node(d, c)
#tree.add_node(e, root)
#tree.add_node(f, e)
#tree.add_node(g, c)
#tree.add_node(h, d)


