#!/usr/bin/env python3
from sys import argv
import copy
from datetime import datetime

class Strategy:
    
    def returnDic():
        return v_dict, l_dict
    def nextnode(self,opennodes):
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
    with open(argv[1]) as openfileobject:
        for line in openfileobject:
            print(line)
            if(line[0]=='V'):
                
                label,weight = line.split()
                v=Vertice(label,weight)
                v_dict[label]=v
            if(line[0]=='E'):
               
                lixo,v1,v2 =line.split()

                e_list.append((v1,v2))
                #v_dict[v1].add_neighbor(v_dict[v2])

            if(line[0]=="L"):
                
                lixo,date,pl,fc,vc = line.split()
                l=Launch(date,pl,fc,vc)
                l_dict[l.date]=l

    for x in e_list:
        v_dict[x[0]].add_neighbor(v_dict[x[1]])
    
    print([str(key) + ":" + str(v_dict[key]) for key in v_dict.keys()])
    print([str(key) + ":" + str(l_dict[key]) for key in l_dict.keys()])   

def successor(parent,operator):
    launch=operator[0]
    vertice=operator[1]
    print(vertice +' ' + launch)
    orbit=parent.state[0].copy()
    rpay=copy.deepcopy(parent.state[1])
    print("in orbit", orbit)
    if not orbit:
        if rpay[launch].payload-v_dict[vertice].weight>=0:
            rpay[launch].payload=rpay[launch].payload-v_dict[vertice].weight
            print("no vertex in orbit. Added vertex:" + vertice)
            orbit[vertice]=launch
            return orbit, rpay
        else:
            print("nothing in orbit but vertex exceeds payload")
            return False
    if datetime.strptime(parent.id[0],'%d%m%Y')>datetime.strptime(operator[0],'%d%m%Y'):
        print("launch sequence not respected")
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
            
            print("neighbor in orbit")
            return orbit, rpay
        else:
            print("payload for launch already exceeded")
            return False
    else:
        print("no neighbor in orbit")
        return False

def isGoal(state):
    s1=set(state[0].keys())
    s2=set(v_dict.keys())

    if s1.issuperset(s2):
        print("goal achieved")
        return True
    else:
        return False

def gfunction(rpay,cost,operator):
    launch=operator[0]
    vertice=operator[1]
    
    if not rpay[launch].first:
        cost=rpay[launch].fixedc+ cost+v_dict[vertice].weight * l_dict[launch].varc
        rpay[launch].first = True
    else:
        cost=cost+v_dict[vertice].weight * l_dict[launch].varc    
    return cost
