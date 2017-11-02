#!/usr/bin/env python3

from datetime import datetime
from timeit import default_timer as timer
from queue import PriorityQueue
import problem5 as problem
import numpy as np

class Node:
    
    def __init__(self, state=({},{},[]), l_sorted=[],label='',path_cost=0, depth=0, action=''):  

        self.state=state
        self.path_cost=path_cost
        self.label=label
        self.l_sorted=l_sorted
        self.depth=depth
        self.action=action

    def __repr__(self):
        return str(self.label)
    def __lt__(self, other):
        return self.label < other.label

def generalSearch(problem, strategy):
    '''runs problem independent general search'''
    
    opennodes=PriorityQueue()
    v_dict,light_ldict=problem.returnDic()
    n_explored=0 #total number of explored nodes
    
    #sort launches by date
    sorted_l= list(light_ldict.keys())
    sorted_l.sort(key= lambda x: datetime.strptime(x,'%d%m%Y'),reverse=True)
    all_launches=sorted_l.copy()

    #create initial empty node
    root=Node(({},light_ldict.copy(),list(v_dict.keys())),sorted_l,sorted_l.pop(),0,0,'empty')
    opennodes.put((root.path_cost,root))

    while True:
        if opennodes.empty():
            print("No solution found for problem")
            print("Total nodes explored: ", n_explored)
            return
        #get next node to be explored according to strategy
        lixo, node=strategy.nextnode(opennodes)
        n_explored=n_explored+1
        if problem.isGoal(node.state):
            problem.print_Solution(node, all_launches) 
            print("Total nodes explored: ", n_explored)
            calculate_EBF(n_explored, node.depth)
            return 
        else:
            # opens node, creates empty childnode that represents skipping launch 
            newsorted=node.l_sorted.copy()
            if newsorted:       #create empty node which means skips launch 
                newlabel=newsorted.pop()
                childnode=Node(node.state,newsorted,newlabel,node.path_cost, node.depth+1,'empty')
                opennodes.put((problem.evaluation(childnode,'empty',node.action),childnode))

            for vkey in node.state[2]:      # from the launches still not in orbit checks if can be a child
                operator = vkey
                newstate= problem.successor(node,operator)
                if not newstate:            # operator doesn't produce new node
                    continue 
                childnode=Node(newstate,node.l_sorted,node.label,node.path_cost,node.depth+1,'vertex')
                childnode.path_cost=problem.gfunction(childnode,operator,node.action)
                
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
    print("Effective branching factor:  %f"%ebf.real)
       
if __name__ == '__main__':
    
    try:
        start= timer()
        problem.readfile()
        strat=problem.Strategy()
        print("Started search...")
        
        generalSearch(problem,strat)
        end=timer()

        print("Elapsed time in sec: ", end-start)
        print("Elapsed time in min: ",(end-start)/60)
    except IOError:
        print("Can't open file")
    except ValueError:
        print("Choose '-i'  or '-u' for informed or uninformed search")
   # except IndexError:
       # print("Insuficient number of arguments")


