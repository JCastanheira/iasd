#!/usr/bin/env python3

import copy
import problem2 as problem

class Node:
    
    def __init__(self, state=({},{},{}), cost=0, id=('01011900','')):  
        self.state=state
        self.cost=cost
        self.id=id
    def __repr__(self):
        return str(self.id)

def generalSearch(problem, strategy):
    opennodes=[]
    v_dict,l_dict=problem.returnDic()

    opennodes.append(Node(({},copy.deepcopy(l_dict),copy.deepcopy(v_dict))))
    while True:
        if not opennodes:
            print("No solution found for problem")
            return 
       
        node=strategy.nextnode(opennodes)
        if problem.isGoal(node.state):
            print('solution achieved')
            print([str(key) + ":" + str(node.state[0][key]) for key in node.state[0].keys()])
            print(node.cost)
            return 
        else:
            for lkey in node.state[1].keys():
                for vkey in node.state[2].keys():
                    operator = lkey, vkey
                    newstate= problem.successor(node,operator)
                    if not newstate: 
                        print("didn't add")
                        continue #operator doesn't produce new node
                    childnode=Node(newstate,node.cost,operator)
                    t_cost=problem.gfunction(childnode.state[1] ,childnode.cost,operator)
                    childnode.cost=t_cost
                    print(childnode.cost)
                    opennodes.append(childnode)
        
if __name__ == '__main__':
    try:
        problem.readfile()
        strat=problem.Strategy()
        generalSearch(problem,strat)

    except IOError:
        print("Can't open file")


