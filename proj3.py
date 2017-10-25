#!/usr/bin/env python3

import copy
import problem3 as problem
from datetime import datetime
from timeit import default_timer as timer

class Node:
    
    def __init__(self, state=({},{},{}), l_sorted=[],id='',path_cost=0, evaluation_cost=100):  
        self.state=state
        self.path_cost=path_cost
        self.id=id
        self.l_sorted=l_sorted
    def __repr__(self):
        return str(self.id)

def generalSearch(problem, strategy):
    opennodes=[]
    v_dict,l_dict=problem.returnDic()

    #sort launches by date
    sorted_l= list(l_dict.keys())
    sorted_l.sort(key= lambda x: datetime.strptime(x,'%d%m%Y'),reverse=True)

    print("SORTED:" ,sorted_l)
    #create initial empty node
    opennodes.append(Node(({},copy.deepcopy(l_dict),copy.deepcopy(v_dict)),sorted_l,sorted_l.pop()))
    while True:
        if not opennodes:
            print("No solution found for problem")
            return
        #get next node to be explored according to strategy
        node=strategy.nextnode(opennodes)
        if problem.isGoal(node.state):
            print('solution achieved')
            print([str(key) + ":" + str(node.state[0][key]) for key in node.state[0].keys()])
            print(node.cost)
            return 
        else:
            #opens node, creates empty childnode that represents skipping launch 
            newsorted=node.l_sorted.copy()
            if newsorted: 
                print("in orbit: ",node.state[0]) 
                newid=newsorted.pop()
                childnode=Node(node.state,newsorted,newid,node.cost)
                opennodes.append(childnode)
                print("Added empty node for launch: ",node.id )
            else: #case no more launches then doesn't create empty launch
                print("in orbit: ",node.state[0])
                print("no more launches")
                print(node.id)
            for vkey in node.state[2]: # from the launches still not in orbit checks if can be a child
                operator = vkey
                newstate= problem.successor(node,operator)
                if not newstate: 
                    print("didn't add")
                    continue #operator doesn't produce new node
                childnode=Node(newstate,node.l_sorted,node.id,node.cost)
                t_cost=problem.gfunction(childnode,operator)
                childnode.cost=t_cost
                print(childnode.cost)
                opennodes.append(childnode)
            

    
if __name__ == '__main__':
    try:
        start= timer()
        problem.readfile()
        strat=problem.Strategy()
        generalSearch(problem,strat)
        end=timer()
        print(end-start)
        print((end-start)/60)
    except IOError:
        print("Can't open file")
    except IndexError:
        print("Insuficient number of arguments")


