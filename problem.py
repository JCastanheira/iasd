#!/usr/bin/env python3
from sys import argv
from datetime import datetime

class Node:
    
    def __init__(self, state=None,label=None,path_cost=0, depth=0, action='empty'):  
        '''state[0] - vertices already in orbit
           state[1] - remaining payloads for each launch
           state[2] and [3] are auxiliary variables to simplify the code
           state[2] - vertices not yet in orbit (which will be the operators)
           state[3] - list of sorted launches by date'''
        self.state=state
        self.label=label
        if state  is None:
            self.state=({},light_ldict,list(v_dict.keys()),sorted_l)
            self.label=sorted_l.pop() 
        self.path_cost=path_cost
        self.depth=depth
        self.action=action

    def __repr__(self):
        return str(self.label)
    def __lt__(self, other):
        return self.label < other.label

class Strategy:
    
    def __init__(self):
        if not (argv[1]=='-i' or argv[1]=='-u'):
            raise ValueError
    def nextnode(self,opennodes):
        return opennodes.get()

class Vertice:
    '''defines a component'''
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
    '''defines a launch'''
    def __init__(self,date,pl,fc,vc):
        self.date=date
        self.payload=float(pl)
        self.fixedc=float(fc)
        self.varc=float(vc)
    def __repr__(self):
        return self.date + ' ' + str(self.payload) + ' ' + str(self.fixedc) + ' ' + str(self.varc)

def readfile():
    '''opens file containing problem domain''' 
    global v_dict 
    global l_dict
    global light_ldict
    global sorted_l
    global all_launches

    light_ldict={}
    sorted_l=[]
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
                light_ldict[date]=float(pl)

    for x in e_list:
        v_dict[x[0]].add_neighbor(v_dict[x[1]])

    sorted_l= list(light_ldict.keys())
    sorted_l.sort(key= lambda x: datetime.strptime(x,'%d%m%Y'),reverse=True)
    all_launches=sorted_l.copy()

def successor(parent,operator):
    '''considering  current node and operator(component) 
        checks if it's possible to send component in current launch''' 
    launch=parent.label
    vertice=operator
    orbit=parent.state[0].copy()
    rpay=parent.state[1].copy()
    rver=parent.state[2].copy()
    l_launches=parent.state[3].copy()
    
    if operator is 'empty':
        if l_launches:
            return orbit, rpay,rver,l_launches
        else:
            return False
    #check if no component in orbit
    if not orbit:
        #check if current launch still has enough payload to accept current operator(component)
        if rpay[launch]-v_dict[vertice].weight>=0:
            rpay[launch]=rpay[launch]-v_dict[vertice].weight
            orbit[vertice]=launch
            rver.remove(vertice)
            return orbit, rpay, rver,l_launches
        else:
            #no node in orbit but exceeds vertex payload
            return False
      
    s1=set(v_dict[vertice].neighbors)
    s2=set(orbit.keys())

    # check if operation is possible, i.e if it has neighbor in orbit
    if not s1.isdisjoint(s2):
        #check if current launch still has enough payload to accept current operator(component)
        if rpay[launch]-v_dict[vertice].weight>=0:
            rpay[launch]=rpay[launch]-v_dict[vertice].weight
            orbit[vertice]=launch
            rver.remove(vertice)
            return orbit, rpay, rver,l_launches
        else:
            # has neighbor but payload for launch already exceeded
            return False
    else:
        # no neighbor in orbit
        return False

def isGoal(state):
    '''check if current state is goal state'''

    if len(state[0].keys()) == len(v_dict.keys()):
        return True
    else:
        return False

def gfunction(node,operator,parent_action):
    '''calculates path cost'''

    launch=node.label
    vertice=operator
    cost=node.path_cost

    if parent_action is 'empty':
        cost=l_dict[launch].fixedc+ cost+v_dict[vertice].weight * l_dict[launch].varc
    else:
        cost=cost+v_dict[vertice].weight * l_dict[launch].varc
    node.path_cost=cost
    return cost

def h1(node):
    """ Other tested heuristic not used in program. 
        cheapest variable cost"""
    if node.state[3]:
        min_vc=l_dict[node.label].varc
        cheap_launch=node.label
        for x in node.state[3]:
            if l_dict[x].varc < min_vc:
                min_vc= l_dict[x].varc
                cheap_launch=x    
    else:
        cheap_launch=node.label
        min_vc=l_dict[node.label].varc     
    cost=0
    if node.state[2]:
        for x in node.state[2]:
            cost=cost+v_dict[x].weight*min_vc
        return cost
    else:
        return 0

def h2(node):
    '''heuristic used for informed strategy.
        calculates estimated cost by checking which one of the remaining available launches
        produces the minimum cost when sending all the remaining components into orbit in a single package'''
    min_cost=10000000

    if node.state[3]:
        if node.state[2]:
            for x in node.state[3]:
                cost= l_dict[x].fixedc
                for y in node.state[2]: # remaining launches
                    cost=cost+ v_dict[y].weight*l_dict[x].varc
                if min_cost > cost:
                    min_cost=cost
            if node.action is 'empty': # current launch
                cost=l_dict[node.label].fixedc
            else:
                cost=0
            for y in node.state[2]:
                    cost=cost+ v_dict[y].weight*l_dict[node.label].varc     
            if min_cost > cost:
                    min_cost=cost  
            return min_cost
        else:
            return 0
    else:
        cost=0
        for y in node.state[2]:
             cost=cost+ v_dict[y].weight*l_dict[node.label].varc
        return cost


def hfunction(node):
    """calculates heuristic value based on state"""
    return h2(node)

def evaluation(node,operator, parent_action):
    """calculates evaluation cost for each method, uninformed and informed
        uninformed:f(n)=g(n)
        informed:f(n)=h(n)+g(n)"""
    if argv[1] == '-u':
        if operator is 'empty':
            return node.path_cost
        return gfunction(node,operator,parent_action)
    if argv[1] == '-i':
        if operator is 'empty':
            return node.path_cost + hfunction(node)
        return gfunction(node,operator,parent_action) + hfunction(node)
        
def print_Solution(node):
    '''prints the solution to the problem'''
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

def operators(node):
    '''returns operators. Operators are all the vertices still not in orbit 
        plus empty operator that allows to skip launch'''
    operators=node.state[2].copy()
    operators.append('empty')
    return operators