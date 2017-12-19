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

def searchEqui(sentence,aux,first):
    print(sentence)
    result=testSentence(sentence)
    print(result)
    if result == "atom" or result == "<=>":
        if result == "<=>":
            print("found <=>")
            aux = transform(result,sentence)
            newsen= eval(aux)
           # if not first:
           #     aux+= ","
            aux= aux  + searchEqui(newsen,"", False)
    else:
        sen1=searchEqui(sentence[1], "",False)
       # print("previous: ", sentence[1]," after: ", sen1)
        aux += sen1
        if len(sentence)==3:
       #     print("previous: ", sentence[1]," after: ", sen1)
            sen2=searchEqui(sentence[2],"", False)
            aux += sen2
    
    if first and result != "<=>" and aux!="":
        aux="( '" + str(result) + "'" + aux + ")"
    return aux

def searchImpl(sentence, aux,first):
    print(sentence)
    result=testSentence(sentence)
    print(result)
    if result == "atom" or result == "=>":
        if result == "=>":
            print("found =>")
            aux = transform(result,sentence)
            newsen= eval(aux)
           # if not first:
            #    aux+= ","
            aux= "," + aux  + searchImpl(newsen,"", False)
            
    else:
        sen1=searchImpl(sentence[1], "",False)
       # print("previous: ", sentence[1]," after: ", sen1)
        aux += sen1
        if len(sentence)==3:
       #     print("previous: ", sentence[1]," after: ", sen1)
            sen2=searchImpl(sentence[2],"", False)
            aux += sen2
    
    if first and result != "=>" and aux!="":
        aux="( '" + str(result) + "'" + aux + ")"

        
    return aux

def searchNot(sentence,aux,first):
    print(sentence)
    result=testSentence(sentence)
    print(result)
    if result == "atom" or (result == "not" and  type(sentence[1]) is tuple):
        if result == "not":
            print("found not")
            aux = transform(result,sentence)
            newsen= eval(aux)
            
            aux= "," + aux  + searchNot(newsen,"", False)
            
    else:
        sen1=searchNot(sentence[1], "",False)
       # print("previous: ", sentence[1]," after: ", sen1)
        aux += sen1
        if len(sentence)==3:
           # print("previous: ", sentence[1]," after: ", sen1)
            sen2=searchNot(sentence[2],"", False)
            aux += sen2
    
    if first and result != "not" and aux!="":
        aux="( '" + str(result) + "'" + aux + ")"
    return aux 

def distribute(sentence,last,first):
    print(sentence)
    result=testSentence(sentence)
    print(result)
    if result == "atom" or (result == "and" and  last== "or"):
        if result != "atom":
            print("found conjuntion inside disjuction")
            return "transform"
    else:
        sen1=distribute(sentence[1], result,False)
        aux= transform(result,sentence)
        if sen1 == "transform":
            aux= transform(result,sentence, 1)
            newsen= eval(aux)
            aux= "," + aux  + distribute(newsen,result, False)
        else:
            if len(sentence)==3:
                sen2=distribute(sentence[2],result, False)
                if sen2 == "transform":
                    aux= transform(result,sentence, 2)
                    newsen= eval(aux)
                    aux= "," + aux  + distribute(newsen,result, False)

    if first and aux!="":
        aux="( '" + str(result) + "'" + aux + ")"
    return aux 
def convert2CNF(sentence):
    
    aux = searchEqui(sentence,"", True)
    print("final equi:", aux)
    if  aux: 
        sentence=eval(aux)
    print("#######################################")
    aux= searchImpl(sentence,"",True)
    print("final impl: ", aux)
    if aux:
        sentence=eval(aux)
    print(sentence)
    print("#######################################")
    aux=searchNot(sentence,"",True)
    print("final not: ", aux)
    if aux:
        sentence=eval(aux)
    aux=distribute(sentence,"",True)
    print("final final:", aux)
    
if __name__ == '__main__':
    
    try:
       readfile();
       for i in sentences:
            print(i)
            #result=transform(testSentence(i),i)
            #print(result)
            convert2CNF(i)
       
    except IOError:
        print("Can't open file")
    except ValueError:
        print("Choose '-i'  or '-u' for informed or uninformed search")
   

