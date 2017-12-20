#!/usr/bin/env python3

# Authors: 
# João Castanheira - 77206
# Francisco Azevedo - 78647

from timeit import default_timer as timer
from queue import PriorityQueue
import numpy as np
from sys import argv
from itertools import combinations
import copy

from random import randrange

def partition(lst, start, end, pivot):
    lst[pivot], lst[end] = lst[end], lst[pivot]
    store_index = start
    for i in range(start, end):
        if lst[i].num_literals < lst[end].num_literals:
            lst[i], lst[store_index] = lst[store_index], lst[i]
            store_index += 1
    lst[store_index], lst[end] = lst[end], lst[store_index]
    return store_index


def quick_sort(lst, start, end):
    if start >= end:
        return lst
    pivot = randrange(start, end + 1)
    new_pivot = partition(lst, start, end, pivot)
    quick_sort(lst, start, new_pivot - 1)
    quick_sort(lst, new_pivot + 1, end)


def sort(lst):
    quick_sort(lst, 0, len(lst) - 1)
    return lst

def readFile(): 
    global sentences
    sentences=[]
    with open(argv[1]) as file:
        for line in file: 
            sentences.append(eval(line))
    #print(sentences)

class Node:
    #Should contain the number of literals, positive literals and negative literals
    def __init__(self,sentence):
        self.sentence = sentence
        self.num_literals = len(sentence)
        self.pos_literals = []
        self.neg_literals = []
        if type(sentence) is tuple:
            self.neg_literals.append(sentence[1])
            self.num_literals = 1
        else:
            for unit in sentence:
                if type(unit) is tuple: 
                    # unit is a "not" tuple
                    self.neg_literals.append(unit[1])
                else:
                    self.pos_literals.append(unit)
                
    def __repr__(self):
        return str(self.sentence)
    
    def __eq__(self, other):
#        return self.sentence == other #para usar a priority queue arranjar outra solução
        return self.sentence == other
    
    def __iter__(self):
        return self
    
    def __hash__(self):
        return hash(str(self.sentence))
    
    def __lt__(self, other):
        return len(self.pos_literals) < len(other.pos_literals)
        
def buildOrdKB(sentences):
    #Create a queue ordered by the number of literals 
    knowledge_base = []
    for sent in sentences:
        print(sent)
        clause = Node(sent)
        knowledge_base.append(clause)
    print('--------------------')
    knowledge_base = sort(knowledge_base)
    return knowledge_base

def buildKB(sentences):
    knowledge_base = []
    for sent in sentences:
        print(sent)
        clause = Node(sent)
        knowledge_base.append(clause)
    print('--------------------')
    return knowledge_base
    
def searchResolution(KB):
    while True: 
        global new_set
        new_set =[]
        idx=0
        for Ci,Cj in combinations(KB,2):
            print(Ci,'+',Cj)                
            resolvents = resolve(Ci,Cj)
            print('Resolvents: ',resolvents)
            idx+=1
            if resolvents=="empty":
                # If resolvents return an empty set, then return true. 
                print('\nTrue')
                return True
            if resolvents != 'no_op':           
                if resolvents not in new_set:  
                    new_set.append(resolvents)
        print('Nr. of Combinations tested: ',idx)
        if set(new_set).issubset(KB):
            # If all the new clauses are a subset of the existing KB, then return false.
            print('\nFalse')
            return False
        for new_clause in new_set:
            if new_clause not in KB: # É preciso verificar também as frases que têm ordens diferentes
                print('----->',new_clause,' added to database')
                KB.append(new_clause)
        KB = sort(KB)
        
def resolve(clause1,clause2):
    neg1 = clause1.neg_literals.copy()
    neg2 = clause2.neg_literals.copy()
    pos1 = clause1.pos_literals.copy()
    pos2 = clause2.pos_literals.copy()
    del1 = list(set(neg1).intersection(pos2))
    del2 = list(set(neg2).intersection(pos1))
    if len(del1)==1 and len(del2)==0:
        print('intersection: ','not',del1,'and',del1)
        neg1.remove(del1[0])
        pos2.remove(del1[0])
    elif len(del2)==1 and len(del1)==0:
        print('intersection: ',del2,'and','not',del2,)
        neg2.remove(del2[0])
        pos1.remove(del2[0])
    else:
        return "no_op"
    new_neg = neg1+neg2
    new_pos = pos1+pos2
    if not new_neg and not new_pos:
        return "empty"
    new_sentence = makeSent(new_neg,new_pos)
    return new_sentence
    
def makeSent(neg,pos):
    global sentence
    sentence =[]
    for lit in neg:
        sentence.append(('not',lit))
    for lit in pos:
        sentence.append(lit)
    if len(sentence)==1:
        sentence=sentence[0]
    new_node = Node(sentence)
    return new_node
    
    
if __name__ == '__main__':
    try:
       readFile()
       #KB = buildKB(sentences)
       KB = buildOrdKB(sentences)
       searchResolution(KB)
       
    except IOError:
        print("\nCan't open file")






