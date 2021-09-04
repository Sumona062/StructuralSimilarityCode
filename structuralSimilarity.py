# -*- coding: utf-8 -*-
"""
Created on Sat Sep  4 17:45:11 2021

@author: Hp
"""


import sys
import re
import PyPDF2 
import numpy as np
import math
from sklearn.feature_extraction.text import TfidfVectorizer
print("Program name: ",sys.argv[0].replace('py',''))
print("Program name(with type): ",sys.argv[0])
print("Element number of program: ",len(sys.argv))
print("Argument list:", sys.argv)
print()



def cosineSimCalc(data1,data2):
    
    multiply=[data1[i]*data2[i] for i in range(len(data1))]
    dot=sum(multiply)
    
    data1Sq=[data1[i]**2 for i in range(len(data1))]
    data1Norm=(sum(data1Sq)**0.5)
    data2Sq=[data2[i]**2 for i in range(len(data2))]
    data2Norm=(sum(data2Sq)**0.5)
    
    
   
   
    
    return round(dot/(data1Norm*data2Norm)*100,4)
    
def preprocess(dataset,i,j,vectorizer):
    corpus=[]
    
    corpus.append(processDataset(dataset[i]))
    corpus.append(processDataset(dataset[j]))
    
                
    return setCorpus(corpus,vectorizer)
    
        
        
                
        
def processDataset(dataset):
    
    
    text = re.sub('[^a-zA-Z]', ' ', dataset)
    text = text.lower()
    text = text.split()
    for t in text:
        if len(t)<3:
            text.remove(t)
    text = ' '.join(text)
        
    return text

def setCorpus(corpus,vectorizer):
    #print(corpus)
    str2 = []
    for k in range(2):
        text = corpus[k]
        str = text.split()
        
        for i in str:
            if len(i)<4:
                str.remove(i)
            if i not in str2:
                str2.append(i)
            
    
    stopWord=['we','was','that', 'the', 'they', 'this', 'those', 'thus','their', 'them', 'then', 'there', 'therefore', 'these', 'well', 'what', 'whether', 'two', 'u','would', 'you', 'your','which', 'while', 'who', 'whole', 'whose', 'will', 'with', 'within',"a"," about", "above", "after", "again", "against", "all", "am", "an", "and", 'able', 'about', 'additionally', 'almost','also','apply', "to","any", "are", "aren't", "as", 'always',"at",'around', "be", "because" ,"been",'become', "before" ,"being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during" ,"each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't" ,"have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers ","herself", "him", "himself", "his" ,"how", "how's", "i'd", "i'll", "i'm", "i've" ,"if" ,"in", "into" ,"is" ,"isn't", "it", "it's" ,"its" ,"itself", "let's" ,"me", "more" ,"most", "mustn't" ,"my", "myself" ,"no", "nor", "not" ,"of" ,"off" ,"on", "once", "only", "or" ,"other" ,"ought" ,'one',"our", "ours"]
    
    for i in range(len(stopWord)):
        
        if stopWord[i] in str2:
            str2.remove(stopWord[i])
    
    str2.sort()
    #print(str2)
    
    if vectorizer == "count":
        return Count_Vectorizer(corpus,str2)
        
    elif vectorizer =="tf-idf":
        return TF_IDF_Vectorizer(corpus, str2)
    
    

def Count_Vectorizer(corpus,str2):
    
    data=[]
    for k in range(2):
        file=[]
        text = corpus[k]
    
        for i in range(len(str2)):
            file.append(text.count(str2[i]))
            #print('Frequency of', str2[i],' in dataset',k ,'is :', text.count(str2[i]))
        data.append(file)

    #print(data)
    
    return data

def TF_IDF_Vectorizer(corpus,str2):
    
    data=[]
    for k in range(2):
        file=[]
        text = corpus[k]
        df=0
    
        for i in range(len(str2)):
            tf=text.count(str2[i])
            if(corpus[0].count(str2[i])!=0):
                df=df+1
            if(corpus[1].count(str2[i])!=0):
                df=df+1
            idf=math.log(3/(df+1))+1
            tf_idf=tf*idf
            file.append(tf_idf)
        data.append(file)

    #print(data)
    
    return data
def similiarity(data,doc1,doc2):
    
    cos_sim=cosineSimCalc(data[0], data[1])
    print (f"Cosine Similarity between {sys.argv[doc1+1]} and {sys.argv[doc2+1]} :{cos_sim}")
    print()




def findSimiliarity(dataset,vectorizer):
    for i in range(len(dataset)):
        for j in range(len(dataset)):
            if(i<j):
                data=preprocess(dataset,i,j,vectorizer)
                similiarity(data, i, j)
                
            
            
            
def setFile(argument,dataset):
    
    pdfFileObj = open(argument+'.pdf', 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    pageObj = pdfReader.getPage(0) 
    dataset.append(pageObj.extractText())
    pdfFileObj.close()
    return dataset

    
        
        
if __name__=="__main__":
    
        
    NumofParam= len(sys.argv)
    print("Num of Params= ",NumofParam)
    list=sys.argv
    dataset=[]
    vectorizer="tf-idf"
    
    
            
    i=1
    while(i<NumofParam):
        argument=list[i].replace(' ','')
        if argument == "-vectorizer":
            if (sys.argv[i+1]).lower() == 'tf-idf' or (sys.argv[i+1]).lower() == 'count':
                vectorizer=(sys.argv[i+1]).lower()
                i=i+2
            else:
                print("Invalid argument! vectorizer options are- 'count' and 'tf-idf'")
                exit(1)
        else:
            dataset=setFile(argument,dataset)
            i=i+1
        
        
    
    findSimiliarity(dataset,vectorizer)
        
   