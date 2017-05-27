#!/usr/bin/env python
#-*-coding:utf-8-*-

from numpy import *
import operator

"""
    KNN算法：
         存在一个样本数据集合，也称训练样本集，
         并且样本集中的每一个数据都存在标签，即我们知道每一个数据所属的分类
         输入没有标签的新数据
         将新数据的每个特征与样本集中数据对应的特征进行比较
         然后算法提取样本集中特征最相似数据（最近邻）的分类标签
         一般选前k个最相似的数据，通常k是不大于20的整数
         最后选择k个最相似数据中出现次数最多的分类，作为新数据的分类
"""

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels  = ['A','A','B','B']
    return group, labels

# labels是标签信息，dataSet是数据集信息，inX是输入的向量信息
def classify0(inX, dataSet, labels, k):
    
    # 计算距离
    dataSetSize = dataSet.shape[0]
    diffMat =  tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    # 选择距离最小的k个点
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    # 排序
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]



def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    # 创建一个numberOfLines行，3列的矩阵，并且每一列的元素为0
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        # 给矩阵赋值，index 表示行，后面表示矩阵每一列的元素的下标
        returnMat[index,:] = listFromLine[0:3]
        #print listFromLine
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dateSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))

