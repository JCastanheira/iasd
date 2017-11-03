#!/usr/bin/env python3

# Authors: 
# João Castanheira - 77206
# Francisco Azevedo - 78647

from timeit import default_timer as timer
from queue import PriorityQueue
import problem
import numpy as np
from sys import argv

def generalSearch(problem, strategy):
    '''runs problem independent general search
        n_explored: number of explored nodes
        opennodes: priority queue with nodes waiting to be explored'''
    
    opennodes=PriorityQueue()
    n_explored=0 
 
    #create initial empty node
    root=problem.Node()
    opennodes.put((problem.evaluation(root,'empty',root.action),root))

    while True:
        if opennodes.empty():
            print('0')
            return
        lixo,node=strategy.nextnode(opennodes)
        n_explored=n_explored+1
        if problem.isGoal(node.state):
            problem.print_Solution(node) 
            calculate_EBF(n_explored, node.depth)
            return 
        else:
            for operator in problem.operators(node):        
                newstate= problem.successor(node,operator)
                if not newstate:    # operator doesn't produce new node because doesnt' respect some problem constraint
                    continue 
                if operator is 'empty':
                    newlabel=newstate[3].pop()
                else: 
                    newlabel=node.label
                childnode=problem.Node(newstate,newlabel,node.path_cost,node.depth+1, operator)
                opennodes.put((problem.evaluation(childnode,operator,node.action),childnode))
                    

def calculate_EBF(explored, depth):
    """Calculates the effective branching factor
        explored: number of vertices visited
        depth: length of final path """

    coefs = [1 for power in range(depth)]
    coefs.append(-explored)
    poly = np.poly1d(coefs)
    roots = (root for root in poly.r if root.real >= 0)     # Discard negative roots
    ebf = min(roots, key=lambda root: abs(root.imag))       # Find root with imag == 0
    print("Total nodes explored: ", explored)
    print("depth: ", depth)
    print("Effective branching factor:  %f"%ebf.real)
       
if __name__ == '__main__':
    
    try:
       # start= timer()
        if len(argv)!=3:
            raise IndexError
        problem.readfile()
        strat=problem.Strategy()
        #print("Started search...")
        generalSearch(problem,strat)
       # end=timer()
        #print("Elapsed time in sec: ", end-start)
        #print("Elapsed time in min: ",(end-start)/60)
    except IOError:
        print("Can't open file")
    except ValueError:
        print("Choose '-i'  or '-u' for informed or uninformed search")
    except IndexError:
        print("Not enough or too many arguments")

