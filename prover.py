#!/usr/bin/env python3

# Authors: 
# João Castanheira - 77206
# Francisco Azevedo - 78647

import sys
from itertools import combinations
from random import randrange

def readStdin():
    '''Read input from stdin.'''
    
    sentences=[]
    for line in sys.stdin:
        result = eval(line)
        sentences.append(result)
    return sentences

class Clause:
    '''Class containing the relevant information for each sentence.'''
    
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
        return self.sentence == other
    
    def __iter__(self):
        return self
    
    def __hash__(self):
        return hash(str(self.sentence))
    
    def __lt__(self, other):
        return len(self.pos_literals) < len(other.pos_literals)
        
def buildOrdKB(sentences):
    '''Create a knowledge base ordered by the number of literals to enforce the UNIT PREFERENCE method.'''
    
    knowledge_base = []
    for sent in sentences:
        clause = Clause(sent)
        knowledge_base.append(clause)
    knowledge_base = sort(knowledge_base)
    return knowledge_base

def partition(lst, start, end, pivot):
    '''Partitions the list to be sorted.'''
    
    lst[pivot], lst[end] = lst[end], lst[pivot]
    store_index = start
    for i in range(start, end):
        if lst[i].num_literals < lst[end].num_literals:
            lst[i], lst[store_index] = lst[store_index], lst[i]
            store_index += 1
    lst[store_index], lst[end] = lst[end], lst[store_index]
    return store_index


def quick_sort(lst, start, end):
    '''Quick sort algorithm to be used with the sort() function.'''
    
    if start >= end:
        return lst
    pivot = randrange(start, end + 1)
    new_pivot = partition(lst, start, end, pivot)
    quick_sort(lst, start, new_pivot - 1)
    quick_sort(lst, new_pivot + 1, end)


def sort(lst):
    '''Sort the elements on a list.'''
    
    quick_sort(lst, 0, len(lst) - 1)
    return lst


def searchResolution(KB):
    '''Propositional logic resolution algorithm.''' 
    while True: 
        global new_set
        new_set =[]
        idx=0
        for Ci,Cj in combinations(KB,2):                
            resolvents = resolve(Ci,Cj)
            idx+=1
            if resolvents=="empty":
                # If resolvents return an empty set, then return true. 
                print('True')
                return True
            if resolvents != 'no_op':           
                if resolvents not in new_set:  
                    new_set.append(resolvents)
        if set(new_set).issubset(KB):
            # If all the new clauses are a subset of the existing KB, then return false.
            print('False')
            return False
        for new_clause in new_set:
            if new_clause not in KB: 
                # If new clause is not in the KB, then add it to the KB.
                KB.append(new_clause)
        KB = sort(simplify(KB))
        
def resolve(clause1,clause2):
    '''Resolve operator for a combination of two sentences.'''
    
    neg1 = clause1.neg_literals.copy()
    neg2 = clause2.neg_literals.copy()
    pos1 = clause1.pos_literals.copy()
    pos2 = clause2.pos_literals.copy()
    del1 = list(set(neg1).intersection(pos2))
    del2 = list(set(neg2).intersection(pos1))
    if len(del1)==1 and len(del2)==0:
        # if there is a negative literal in clause 1 that can be resolved by a positive literal in clause 2
        neg1.remove(del1[0])
        pos2.remove(del1[0])
    elif len(del2)==1 and len(del1)==0:
        # if there is a negative literal in clause 2 that can be resolved by a positive literal in clause 1
        neg2.remove(del2[0])
        pos1.remove(del2[0])
    else:
        # Do nothing
        return "no_op"
    new_neg = neg1+neg2
    new_pos = pos1+pos2
    if not new_neg and not new_pos:
        # If the there are no positive and negative literals in this clause, return empty
        return "empty"
    new_sentence = makeSent(new_neg,new_pos)
    return new_sentence
    
def makeSent(neg,pos):
    '''Rebuild a sentence string from the information about the positive and negative literals.'''
    
    global sentence
    sentence =[]
    for lit in neg:
        sentence.append(('not',lit))
    for lit in pos:
        sentence.append(lit)
    if len(sentence)==1:
        sentence=sentence[0]
    new_Clause = Clause(sentence)
    return new_Clause
    
def simplify(output):
    '''Simplifies clauses and eliminates redundancies.'''
    
    aux=output.copy()
    for clause in aux:
        # performs factoring
        if len(set(clause.sentence)) < len(clause.sentence):
            output.remove(clause)
            output.append(Clause(list(set(clause.sentence))))
    
    for x in aux:
        if type(x.sentence) is not list:
            a=[x.sentence]
        else:
            a=x.sentence
        for y in aux:
            if type(y.sentence) is not list:
                b=[y.sentence]
            else:
                b=y.sentence
            #removes clauses implied by others
            if set(a).issubset(b) and (y in output) and (a != b):
                output.remove(y)
            #removes duplicate clauses
            if set(a).issubset(b) and (y in output) and (x is not y):
                output.remove(y)
    return output           

if __name__ == '__main__':
    try:
       sentences = readStdin()
       KB = buildOrdKB(sentences)
       searchResolution(KB)
    except IOError:
       print("\nCan't open file")