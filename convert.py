#!/usr/bin/env python3

# Authors: 
# João Castanheira - 77206
# Francisco Azevedo - 78647

import sys
   
def readStdin():
    '''reads file content from stdin'''

    sentences=[]    
    for line in sys.stdin:
        result = eval(line)
        sentences.append(result)
    
    return sentences

def testSentence(sentence):
    '''tests operator from sentence'''

    if type(sentence) is tuple:
        sentence_type=sentence[0]
        return sentence_type
    else:
        return "atom"

def transform(types,sentence,i=0):
    ''' transforms sentence according to rules '''

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
    ''' search for equivalence'''

    new = sentence
    result=testSentence(sentence)
    if result == "atom" or result == "<=>":
        if result == "<=>":
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
    '''search implication '''

    new = sentence
    result=testSentence(sentence)

    if result == "atom" or result == "=>":
        if result == "=>":
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
    '''move not inwards in order to appear in literals only'''

    new = sentence
    result=testSentence(sentence)

    if result == "atom" or (result == "not" and  type(sentence[1]) is tuple):
        if result == "not":
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
    '''apply distributive rule in order to get a conjuction of disjuctions'''

    new = sentence
    result=testSentence(sentence)

    if result == "atom" or (result == "and" and  last== "or"):
        #there is a conjuction inside a disjuction -> needs transformation on parent level
        if result != "atom":
            return "transform"
    else:
        sen1=distribute(sentence[1], result)
        if sen1 != sentence[1] and sen1 != "transform":
            new=(result, sen1, new[2])
            if result == 'or' and testSentence(sen1)== 'and': 
                sen1= "transform"

        if sen1 == "transform":
            #found problem at lower level -> applies transformation rule 
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
                    #found problem at loew level -> applies transformation rule 
                    newsen= transform(result,new, 2)
                    sen0 = distribute(newsen,"")
                    return sen0
    return new

def getDisjuctions(sentence,CNF):
    '''after all transformations finds disjuctions'''

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
    '''conversion to CNF algorithm'''
    CNF=[]
    operator = testSentence(sentence)

    if operator == "atom" or (operator == "not" and (type(sentence[1]) is not tuple)):
        #sentence is already a literal or negation of literal
        CNF.append([sentence])
    else:
        aux = searchEqui(sentence)
        aux = searchImpl(aux)
        aux = searchNot(aux)
        aux = distribute(aux,"")

        if testSentence(aux) == 'and':
            output = getDisjuctions  (aux,[])
        else:
            #when top operator is not a conjunction
            output=[]
            output.append(aux)
        CNF = outputDisj(output)

    return CNF

def printOutput(CNF):
    ''' prints to stdout the results with correct format'''
    for i in CNF:
            if len(i) ==1:
                if type(i[0]) is not tuple:
                    str0= "'" + str(i[0]) + "'" 
                    print(str0)
                else:
                    print(i[0])
            else:
                print(i)

if __name__ == '__main__':   
    try:
        sentences = readStdin();
        CNF=[]
        for i in sentences:
            aux = convert2CNF(i)
            for x in aux:
                # for the new clauses checks if they don't exist already
                if x not in CNF:
                    CNF.append(x)
        
        printOutput(CNF)
        
    except (NameError,SyntaxError):
        print("Syntax problem with input sentences")