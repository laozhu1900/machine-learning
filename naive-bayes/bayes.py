#!/usr/bin/env python
#-*- coding:utf-8 -*-

from numpy import *

def loadDataSet():
    postingList = [
	  ['my','dog','has','flea','problems','help','please'],
	  ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
      ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
      ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
      ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
      ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
	]
    classVec = [0,1,0,1,0,1]
    return postingList, classVec


def createVocabList(dataSet):
    #创建一个空集合
    vocabSet = set([])
    for  document in dataSet:
    	vocabSet = vocabSet | set(document)
    return list(vocabSet)

# 将单词变成一个向量
def setOfWord2Vec(vocabList, inputSet):
	# 创建一个所含元素都是0的向量
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word: %s is not in my Vocabulary !" %word
	return returnVec

def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	# 侮辱性词汇的数量
	numWords = len(trainMatrix[0])
	# 侮辱性句子在总句子中的比例
	pAubsive = sum(trainCategory) / float(numTrainDocs)
	p0Num = zeros(numWords);p1Num = zeros(numWords)
	p0Denom = 0.0; p1Denom = 0.0
	for i in range(numTrainDocs):
		# 侮辱性的词汇和正常单词统计
		# 向量相加
		# 单词个数相加
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	print "1:", p1Num, p1Denom
	print "0:", p0Num, p0Denom
	# 侮辱性词汇中每个单词在侮辱性词汇中的概率
	p1Vect = p1Num / p0Denom
	# 正常词汇中每个单词在正常词汇中的概率
	p0Vect = p0Num / p0Denom
	return p1Vect, p0Vect,pAubsive

if __name__ == '__main__':
	listOPosts, listClasses = loadDataSet()
	print listOPosts
	print listClasses

	myVocabList = createVocabList(listOPosts)
	print myVocabList
	print setOfWord2Vec(myVocabList, listOPosts[0])
	print setOfWord2Vec(myVocabList, listOPosts[3])
	print '------------------'
	trainMat = []
	for postinDoc in listOPosts:
		vect = setOfWord2Vec(myVocabList,postinDoc)
		trainMat.append(vect)
	print trainMat
	# trainMat 是个32*5的向量
	print listClasses
	print '----------------'
	p0V, p1V, pAb = trainNB0(trainMat, listClasses)

	print p0V
	print p1V
	print pAb

