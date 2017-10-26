#!/usr/bin/env python3

import copy
import problem3 as problem
from datetime import datetime
from timeit import default_timer as timer
from queue import PriorityQueue
import numpy as np

class Node:
    
    def __init__(self, state=({},{},[]), l_sorted=[],label='',path_cost=0, depth=0, evaluation_cost=100):  
        self.state=state
        self.path_cost=path_cost
        self.label=label
        self.l_sorted=l_sorted
        self.depth=depth

    def __repr__(self):
        return str(self.label)
    def __lt__(self, other):
        return self.label < other.label

def generalSearch(problem, strategy):
    '''runs problem independent general search'''
    opennodes=PriorityQueue()
    v_dict,l_dict=problem.returnDic()
    n_explored=0
    #sort launches by date
    sorted_l= list(l_dict.keys())
    sorted_l.sort(key= lambda x: datetime.strptime(x,'%d%m%Y'),reverse=True)
    
    all_launches=sorted_l.copy()
    print("SORTED:" ,sorted_l)
    #create initial empty node
    root=Node(({},copy.deepcopy(l_dict),list(v_dict.keys())),sorted_l,sorted_l.pop())
    opennodes.put((root.path_cost,root))
    while True:
        if not opennodes:
            print("No solution found for problem")
            return
        #get next node to be explored according to strategy
        lixo, node=strategy.nextnode(opennodes)
        n_explored=n_explored+1
        if problem.isGoal(node.state):
            print('solution achieved')
            print([str(key) + ":" + str(node.state[0][key]) for key in node.state[0].keys()])
            print(node.path_cost)
            print_Solution(node, all_launches)
            print("depth: ", node.depth)
            calculate_EBF(n_explored, node.depth)
            return 
        else:
            #opens node, creates empty childnode that represents skipping launch 
            newsorted=node.l_sorted.copy()
            if newsorted: 
                print("in orbit: ",node.state[0]) 
                newlabel=newsorted.pop()
                childnode=Node(node.state,newsorted,newlabel,node.path_cost, node.depth)
                childnode.depth=childnode.depth+1
                opennodes.put((childnode.path_cost,childnode))
                print("Added empty node for launch: ",node.label )
            else: #case no more launches then doesn't create empty launch
                print("in orbit: ",node.state[0])
                print("no more launches")
                print(node.label)
            for vkey in node.state[2]: # from the launches still not in orbit checks if can be a child
                operator = vkey
                newstate= problem.successor(node,operator)
                if not newstate: 
                    print("didn't add")
                    continue #operator doesn't produce new node
                childnode=Node(newstate,node.l_sorted,node.label,node.path_cost,node.depth)
                t_cost=problem.gfunction(childnode,operator)
                childnode.path_cost=t_cost
                print(childnode.path_cost)
                childnode.depth=childnode.depth+1
                opennodes.put((childnode.path_cost,childnode))

def calculate_EBF(explored, depth):
    """
    Calculate the effective branching factor
    explored: number of vertices visited
    depth: length of final path """
    
    coefs = [1 for power in range(depth)]
    coefs.append(-explored)
    poly = np.poly1d(coefs)
    roots = (root for root in poly.r if root.real >= 0)     # Discard negative roots
    ebf = min(roots, key=lambda root: abs(root.imag))       # Find root with imag == 0
    print("Effective branching factor:  %f"%ebf.real)
        
def print_Solution(node,all_launches):
    
    flag=False
    all_launches.reverse()
    
    for l in all_launches:
        str=l+'     '
        for vertice in node.state[0].keys():
            if l in node.state[0][vertice]:
                str= str + ' '+  vertice
                flag=True
        if flag:
            print(str)
            flag=False
            
if __name__ == '__main__':
    
    try:
        start= timer()
        problem.readfile()
        strat=problem.Strategy()
        generalSearch(problem,strat)
        end=timer()
        print("Execution time in sec: ", end-start)
        print("Execution time in min: ",(end-start)/60)
    except IOError:
        print("Can't open file")
    except IndexError:
        print("Insuficient number of arguments")


