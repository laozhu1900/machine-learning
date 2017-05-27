#!/usr/bin/env python

"""
   理解点：
       信息增益：划分数据集之前之后信息发生的变化称为信息增益，也就是计算特征值
       香农公式
       熵定义为信息的期望值
       什么是信息：
      
      需要学习的知识：数学期望，标准差，方差

"""
from math import log

# 计算给定数据集的香农熵
def calcShannonEnt(dateSet):
    numEntries = len(dateSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2
    return shannonEnt


