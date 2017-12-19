#!/usr/bin/env python3

# Authors: 
# João Castanheira - 77206
# Francisco Azevedo - 78647

from timeit import default_timer as timer
#import numpy as np
from sys import argv

def readfile():
    '''opens file containing problem domain''' 

    global sentences

    result=()
    sentences=[]
    with open(argv[1],'r') as openfileobject:
        for line in openfileobject:
            result = eval(line)
            sentences.append(result)
    

def testSentence(sentence):
    
    if type(sentence) is tuple:
        sentence_type=sentence[0]
        return sentence_type
    else:
        return "atom"

def transform(types,sentence,i=0):
    
    if types == "<=>":
        return str(('and',('=>',sentence[1],sentence[2]),('=>',sentence[2],sentence[1])))
    if types == "=>":
        return str(('or',('not', sentence[1]),sentence[2]))

    if types is "not" and type(sentence[1]) is tuple:
        if testSentence(sentence[1]) == "or":
            return str(('and',('not', sentence[1][1]), ('not', sentence[1][2])))
        if testSentence(sentence[1]) == "and":
            return str(('or',('not', sentence[1][1]), ('not', sentence[1][2])))
        if testSentence(sentence[1]) == "not":
            return "'" + str(sentence[1][1]) + "'"
    
    if types == "or":
        if i==1:
            return str(('and', ('or', sentence[1][1], sentence[2]) , ('or', sentence[1][2], sentence[2])))
        if i==2:  
            return str(('and', ('or', sentence[2][1], sentence[1]) , ('or', sentence[2][2], sentence[1])))

def searchEqui(sentence):
    new = sentence
    #print(sentence)
    result=testSentence(sentence)
    #print(result)
    if result == "atom" or result == "<=>":
        if result == "<=>":
            #print("found <=>")
            aux = transform(result,sentence)
            newsen= eval(aux)
            sen0 = searchEqui(newsen)
            return sen0
    else:
        sen1=searchEqui(sentence[1])
        if len(sentence)==3:
            sen2=searchEqui(sentence[2])
            new = (result,sen1,sen2)
        else:
            new = (result,sen1)
    return new

def searchImpl(sentence):
    new = sentence
    #print(sentence)
    result=testSentence(sentence)
    #print(result)
    if result == "atom" or result == "=>":
        if result == "=>":
            #print("found =>")
            aux = transform(result,sentence)
            newsen= eval(aux)
            sen0 = searchImpl(newsen)
            return sen0
    else:
        sen1=searchImpl(sentence[1])
        if len(sentence)==3:
            sen2=searchImpl(sentence[2])
            new = (result,sen1,sen2)
        else:
            new = (result,sen1)
    return new

def searchNot(sentence):
    new = sentence
    #print(sentence)
    result=testSentence(sentence)
    #print(result)
    if result == "atom" or (result == "not" and  type(sentence[1]) is tuple):
        if result == "not":
            #print("found not")
            aux = transform(result,sentence)
            newsen= eval(aux)
            sen0 = searchNot(newsen)
            return sen0
           
    else:
        sen1=searchNot(sentence[1])
        if len(sentence)==3:
            sen2=searchNot(sentence[2])
            new = (result,sen1,sen2)
        else:
             new = (result,sen1)   
    return new

def distribute(sentence,last):
    new = sentence
#   print(sentence)
    result=testSentence(sentence)
#   print(result)
    if result == "atom" or (result == "and" and  last== "or"):
        if result != "atom":
            #print("found conjuntion inside disjuction")
            return "transform"
    else:
        sen1=distribute(sentence[1], result)
        if sen1 != sentence[1] and sen1 != "transform":
            new=(result, sen1, new[2])
            if result == 'or' and testSentence(sen1)== 'and': 
                sen1= "transform"

        if sen1 == "transform":
            aux= transform(result,new, 1)
            newsen= eval(aux)
            sen0 = distribute(newsen,"")
            return sen0
        else:
            if len(sentence)==3:
                sen2=distribute(sentence[2],result)
                if sen2 != sentence[2] and sen2 != "transform":
                    new=(result,new[1],sen2)   
                    if result == 'or' and testSentence(sen2)== 'and': 
                        sen2= "transform"
                if sen2 == "transform":
                    aux= transform(result,new, 2)
                    newsen= eval(aux)
                    sen0 = distribute(newsen,"")
                    return sen0
    return new

def convert2CNF(sentence):
    
    aux = searchEqui(sentence)
    print("final equi:", aux)
    print("#######################################")
    aux= searchImpl(aux)
    print("final impl: ", aux)
    print("#######################################")
    aux=searchNot(aux)
    print("final not: ", aux)
    aux=distribute(aux,"")
    print("final:", aux)
    #orConditions(aux)

if __name__ == '__main__':
    
    try:
       readfile();
       for i in sentences:
            print("new sentence: ", i)
            convert2CNF(i)
       
    except IOError:
        print("Can't open file")
    except ValueError:
        print("Choose '-i'  or '-u' for informed or uninformed search")
