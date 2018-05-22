#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 11:06:24 2018

@author: zhenfang
"""
numtopics = 20
def writeToTxt(list_name,file_path):
    try:
        fp = open(file_path,"w+")
        for item in list_name:
            fp.write(str(item)+"\n")
        fp.close()
    except IOError:
        print("fail to open file")
        
def readFile(file):
    docTopic = []
    with open(file) as f:
        line = f.readline()
        while line:
            line = line.split(' ')
            print(line)
            topicId = line.index(max(line))
            docTopic.append(topicId)
            line = f.readline()
    return docTopic
docTopic = readFile('model-final.txt')

writeToTxt(docTopic,'./docTopic.txt')