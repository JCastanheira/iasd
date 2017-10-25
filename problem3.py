#!/usr/bin/env python3
from sys import argv
import copy
from datetime import datetime

class Strategy:
    
    def __init__(self):
        if argv[1]=='-i':
            print("informed")
        elif argv[1]=='-u':
            print("uinformed")
        else:
            print("\nERROR: Choose '-i'  or '-u' for informed or uninformed search")
            exit(0)
        self.strat=argv[1]                
    def returnDic():
        return v_dict, l_dict
    def nextnode(self,opennodes):
        if self.strat == '-i':
            informed
        elif self.strat =='-u':
            opennodes.sort(key= lambda x: x.cost,reverse=True)
            return opennodes.pop()

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
    global v_dict 
    global l_dict

    v_dict = {}
    l_dict = {}
    e_list=[]
    with open(argv[2]) as openfileobject:
        for line in openfileobject:
            print(line)
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
    
    print([str(key) + ":" + str(v_dict[key]) for key in v_dict.keys()])
    print([str(key) + ":" + str(l_dict[key]) for key in l_dict.keys()])   

def successor(parent,operator):
    
    launch=parent.id
    vertice=operator
    orbit=parent.state[0].copy()
    rpay=copy.deepcopy(parent.state[1])
    rver=copy.deepcopy(parent.state[2])

    print(vertice +' ' + launch)
    print("in orbit", orbit)

    if not orbit:
        if rpay[launch].payload-v_dict[vertice].weight>=0:
            rpay[launch].payload=rpay[launch].payload-v_dict[vertice].weight
            print("no vertex in orbit. Added vertex: " + vertice)
            orbit[vertice]=launch
            rver.pop(vertice,None)
            return orbit, rpay, rver
        else:
            print("nothing in orbit but vertex exceeds payload")
            return False
    if vertice in orbit:
        print("vertex already in orbit")
        return False        
    s1=set(v_dict[vertice].neighbors)
    s2=set(orbit.keys())

    if not s1.isdisjoint(s2):
        if rpay[launch].payload-v_dict[vertice].weight>=0:
            rpay[launch].payload=rpay[launch].payload-v_dict[vertice].weight
            orbit[vertice]=launch
            print("neighbor in orbit. Added vertex: " + vertice)
            rver.pop(vertice,None)
            return orbit, rpay, rver
        else:
            print("payload for launch already exceeded")
            return False
    else:
        print("no neighbor in orbit")
        return False
'''
def r_launch(rpay, launch):
    unwanted=[]
    for x in rpay.keys():
        if datetime.strptime(x,'%d%m%Y')<datetime.strptime(launch,'%d%m%Y'):
            unwanted.append(x)
            
    for y in unwanted:
        rpay.pop(y,None)
        print("popped")
'''
def isGoal(state):
    s1=set(state[0].keys())
    s2=set(v_dict.keys())

    if s1.issuperset(s2):
        print("goal achieved")
        return True
    else:
        return False

def gfunction(node,operator):
    launch=node.id
    vertice=operator
    rpay=node.state[1]
    cost=node.cost
    if not rpay[launch].first:
        cost=rpay[launch].fixedc+ cost+v_dict[vertice].weight * l_dict[launch].varc
        rpay[launch].first = True
    else:
        cost=cost+v_dict[vertice].weight * l_dict[launch].varc   
    return cost
