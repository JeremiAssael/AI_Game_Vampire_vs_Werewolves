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
            
    def display(self):
        """Display the tree in a pretty manner"""
        print(self.root)
        self.root.display_children()
                 
    def max_value(self, node, alpha, beta):
        pass
    
    def min_value(self, node, alpha, beta):
        pass
    
    
#    def __repr__(self):
#        """Special method to print a tree in a pretty way"""
#        return str(self.display())



#Trials
    
root = nde.Node("root", 0.45)
tree = Tree(root)
c= nde.Node("c", 2.34)
d= nde.Node("d", 56)
e= nde.Node("e", 87)
f= nde.Node("f", 78)
g = nde.Node("g", 67)
h = nde.Node("h", 698)
tree.add_node(c, root)
tree.add_node(d, c)
tree.add_node(e, root)
tree.add_node(f, e)
tree.add_node(g, c)
tree.add_node(h, d)


