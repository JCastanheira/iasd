#!/usr/bin/env python3
from sys import argv
import copy

class Strategy:
    
    def __init__(self):
        if argv[1]=='-i':
            print("informed")
        elif argv[1]=='-u':
            print("uninformed")
        else:
            print("\nERROR: Choose '-i'  or '-u' for informed or uninformed search")
            exit(0)
        self.strat=argv[1]  
        
    def returnDic():
        return v_dict, l_dict
    def nextnode(self,opennodes):
        if self.strat == '-i':
            print("not implemented yet....")
            exit(0)
        elif self.strat =='-u':
            return opennodes.get()

class Vertice:
    
    def __init__(self,label='',weight=0):
        self.label=label
        self.weight=float(weight)
        self.neighbors=[]

    def __repr__(self):
        return self.label + ' ' + str(self.weight) + ' '+ str(self.neighbors)
    
    def add_neighbor(self,neighbor):
        if isinstance(neighbor, Vertice):
            self.neighbors.append(neighbor.label)
            neighbor.neighbors.append(self.label)
        else:
            print("not a vertice")

class Launch:
    
    def __init__(self,date,pl,fc,vc):
        self.date=date
        self.payload=float(pl)
        self.fixedc=float(fc)
        self.varc=float(vc)
        self.first=False
    def __repr__(self):
        return self.date + ' ' + str(self.payload) + ' ' + str(self.fixedc) + ' ' + str(self.varc)

def returnDic():
    return v_dict, l_dict

def readfile():
    '''opens file containing problem domain''' 
    global v_dict 
    global l_dict

    v_dict = {}
    l_dict = {}
    e_list=[]
    
    with open(argv[2]) as openfileobject:
        for line in openfileobject:
            if line[0]=='V':
                label,weight = line.split()
                v=Vertice(label,weight)
                v_dict[label]=v
            if line[0]=='E':      
                lixo,v1,v2 =line.split()
                e_list.append((v1,v2))
            if line[0]=="L":
                lixo,date,pl,fc,vc = line.split()
                l=Launch(date,pl,fc,vc)
                l_dict[l.date]=l
    for x in e_list:
        v_dict[x[0]].add_neighbor(v_dict[x[1]])
    
def successor(parent,operator):
    
    launch=parent.label
    vertice=operator
    orbit=parent.state[0].copy()
    rpay=copy.deepcopy(parent.state[1])
    rver=parent.state[2].copy()

    #check if no node in orbit
    if not orbit:
        if rpay[launch].payload-v_dict[vertice].weight>=0:
            rpay[launch].payload=rpay[launch].payload-v_dict[vertice].weight
            orbit[vertice]=launch
            rver.remove(vertice)
            return orbit, rpay, rver
        else:
            #no node in orbit but exceeds vertex payload
            return False
      
    s1=set(v_dict[vertice].neighbors)
    s2=set(orbit.keys())

    # check if operation is possible, i.e if it has neighbor in orbit
    if not s1.isdisjoint(s2):
        if rpay[launch].payload-v_dict[vertice].weight>=0:
            rpay[launch].payload=rpay[launch].payload-v_dict[vertice].weight
            orbit[vertice]=launch
            rver.remove(vertice)
            return orbit, rpay, rver
        else:
            # has neighbor but payload for launch already exceeded
            return False
    else:
        # no neighbor in orbit
        return False

def isGoal(state):

    if len(state[0].keys()) == len(v_dict.keys()):
        print("goal achieved")
        return True
    else:
        return False

def gfunction(node,operator):
    
    launch=node.label
    vertice=operator
    rpay=node.state[1]
    cost=node.path_cost
    
    if not rpay[launch].first:
        cost=rpay[launch].fixedc+ cost+v_dict[vertice].weight * l_dict[launch].varc
        rpay[launch].first = True
    else:
        cost=cost+v_dict[vertice].weight * l_dict[launch].varc
    return cost

def print_Solution(node,all_launches):
    
    flag=False
    all_launches.reverse()
    
    for l in all_launches:
        str=l+'     '
        launch_cost=0
        for vertice in node.state[0].keys():
            if l in node.state[0][vertice]:
                str= str + ' '+  vertice
                flag=True
                launch_cost=launch_cost+v_dict[vertice].weight*l_dict[l].varc
        launch_cost=launch_cost + l_dict[l].fixedc 
        if flag:
            print(str + '   ', launch_cost)
            flag=False
    print(node.path_cost)
    print("depth: ", node.depth)
