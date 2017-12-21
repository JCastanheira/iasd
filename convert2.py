#!/usr/bin/env python3

# Authors: 
# João Castanheira - 77206
# Francisco Azevedo - 78647

import sys
def readfile():
    '''opens file containing problem domain''' 

    global sentences

    result=()
    sentences=[]
    with open(argv[1],'r') as openfileobject:
        for line in openfileobject:
            result = eval(line)
            sentences.append(result)
    
def readSdin():
    global sentences

    result=()
    sentences=[]
    
    for line in sys.stdin:
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
        return ('and',('=>',sentence[1],sentence[2]),('=>',sentence[2],sentence[1]))
    if types == "=>":
        return ('or',('not', sentence[1]),sentence[2])

    if types is "not" and type(sentence[1]) is tuple:
        if testSentence(sentence[1]) == "or":
            return ('and',('not', sentence[1][1]), ('not', sentence[1][2]))
        if testSentence(sentence[1]) == "and":
            return ('or',('not', sentence[1][1]), ('not', sentence[1][2]))
        if testSentence(sentence[1]) == "not":
            return sentence[1][1]
    
    if types == "or":
        if i==1:
            return ('and', ('or', sentence[1][1], sentence[2]) , ('or', sentence[1][2], sentence[2]))
        if i==2:  
            return ('and', ('or', sentence[2][1], sentence[1]) , ('or', sentence[2][2], sentence[1]))

def searchEqui(sentence):
    new = sentence
    #print(sentence)
    result=testSentence(sentence)
    #print(result)
    if result == "atom" or result == "<=>":
        if result == "<=>":
            #print("found <=>")
            newsen = transform(result,sentence)
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
            newsen = transform(result,sentence)
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
            newsen = transform(result,sentence)
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
            newsen= transform(result,new, 1)
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
                    newsen= transform(result,new, 2)
                    sen0 = distribute(newsen,"")
                    return sen0
    return new

def getDisjuctions(sentence,CNF):

    result=testSentence(sentence)

    if (result == "and"):
        if sentence[1][0] != "and":
            CNF.append(sentence[1])
        else:
            getDisjuctions(sentence[1],CNF)
        if sentence[2][0] != "and":
            CNF.append(sentence[2])
        else:
            getDisjuctions(sentence[2],CNF)
    
    return CNF

def findLiterals(allClauses,clause,i):
    '''find literals inside disjuction and create clause''' 
    result=testSentence(clause)

    if result== "atom" or result== "not":
            allClauses[i].append(clause)
    else:
        findLiterals(allClauses,clause[1],i)
        findLiterals(allClauses,clause[2],i)

        
def outputDisj(CNFlist):
    '''get list of clauses'''
    allClauses=[]
    i=0
    for clause in CNFlist:
        allClauses.append([])
        findLiterals(allClauses,clause,i)
        i=i+1
    #for x in allClauses:
    #    print(x)
    return simplify(allClauses)

def simplify(output):
    ''' simplifies list of clauses'''

    aux=output.copy()
    for clause in aux:
        for literal in clause:
            # removes tautologies 
            if type(literal) is tuple:
                if literal[1] in clause:
                    output.remove(clause)
                    break
        # performs factoring
        if len(set(clause)) < len(clause) and (clause in output) :
            output.remove(clause)
            output.append(list(set(clause)))
    
    for x in output:
        for y in output:
            #removes clauses implied by others
            if set(x).issubset(y) and (y in output) and (x !=y):
                output.remove(y)
            #removes duplicate clauses
            if set(x).issubset(y) and (y in output) and (x is not y):
                output.remove(y)

    return output        
def convert2CNF(sentence):
    
    CNF=[]
    operator = testSentence(sentence)

    if operator == "atom" or (operator == "not" and (type(sentence[1]) is not tuple)):
        #if sentence is a literal or negation of literal
        CNF.append([sentence])
    else:
        aux = searchEqui(sentence)
        aux = searchImpl(aux)
        aux = searchNot(aux)
        aux = distribute(aux,"")

        if testSentence(aux) != 'or':
            output = getDisjuctions  (aux,[])
        else:
            #when top operator is already a disjuction
            output=[]
            output.append(aux)
        CNF = outputDisj(output)


    #print("There are ", len(CNF), " clauses")
    #for i in CNF:
    #    print(i)
    
    return CNF

if __name__ == '__main__':   
    try:
        #readfile();
        readSdin();
        CNF=[]
        for i in sentences:
            #print("new sentence: ", i)
            aux = convert2CNF(i)
            for x in aux:
                # for the new clauses checks if they don't exist already
                if x not in CNF:
                    CNF.append(x)
        #print("KB in CNF for this file is: ")
        for i in CNF:
            if len(i) ==1:
                if type(i[0]) is not tuple:
                    str0= "'" + str(i[0]) + "'" 
                    print(str0)
                else:
                    print(i[0])
            else:
                print(i)

    except IOError:
        print("Can't open file")