#!/usr/bin/env python
#-*-coding:utf-8-*-
from math import log
import operator

"""
    香农公式的用途：
        假设数据集的最后一列是特征值：
        香农公式用来计算信息增益：
            获取信息增益最高的特征就是最好的选择
            信息的度量方式就成为香农熵

"""
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def createDataSet():
    dataSet = [
      [1,1,'yes'],
      [1,1,'yes'],
      [1,0,'no'],
      [0,1,'no'],
      [0,1,'no']
    ]
    labels = ['no surfacing', 'flippers','fish']

    return dataSet, labels

"""
    用来划分数据集
    dataSet: 需要划分的数据集
    axis: 划分数据集的特征 (也就是数据集中的位数)
    value: 指定的特征值
"""
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet


"""
    选择最好的数据集划分方式

"""
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) -1
    # 当前信息的香农熵
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            # 计算信熵值，并对素有唯一特征值得到的熵求和，信息增益是熵的减少或者是数据无序度的减少
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


"""
    选择分类中出现次数最多的特征
"""
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), \
        key = operator.itemgetter(1), resverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    
    # 类别完全相同则停止划分
    if classList.count(classList[0]) == len(classList):
        return classList[0]

    # 遍历完所有的特征时返回出现次数最多的 
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}

    # 得到列表包含的所有属性值
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLables = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLables)
    return myTree


if __name__ == '__main__':
    myDat, labels = createDataSet()
    print myDat
 
    # print calcShannonEnt(myDat)
    # myDat[0][-1] = 'maybe'
    # print myDat
    # 熵越高，混合的数据也就越多
    # print calcShannonEnt(myDat)
    print "---------------"

    # print splitDataSet(myDat,0, 0)
    print chooseBestFeatureToSplit(myDat)
    print "----------------"

    myTree = createTree(myDat, labels)
    print myTree

