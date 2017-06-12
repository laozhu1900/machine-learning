#!/usr/bin/env python
#-*- coding:utf-8 -*-

from numpy import *
import re

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
def setOfWords2Vec(vocabList, inputSet):
	# 创建一个所含元素都是0的向量
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else:
			print "the word: %s is not in my Vocabulary !" %word
	return returnVec

def bagOfWords2VecMN(vocabList, inputSet):
	returnVec = [0] * len(vocabList)
	for word in inputSet:
		if word in vocabList:
			returnVec[vocabList.index(word)] += 1
	return returnVec

def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	# 侮辱性词汇的数量
	numWords = len(trainMatrix[0])
	# 侮辱性句子在总句子中的比例
	pAubsive = sum(trainCategory) / float(numTrainDocs)

	# p0Num = zeros(numWords);p1Num = zeros(numWords)
	# p0Denom = 0.0; p1Denom = 0.0
	# ones 方法是生成一维矩阵
	p0Num = ones(numWords); p1Num = ones(numWords)
	p0Denom = 2.0; p1Denom = 2.0
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

	# 侮辱性词汇中每个单词在侮辱性词汇中的概率
	# p1Vect = p1Num / p0Denom
	# 正常词汇中每个单词在正常词汇中的概率
	# p0Vect = p0Num / p0Denom
	p1Vect = log(p1Num / p1Denom)
	p0Vect = log(p0Num / p0Denom)
	return p0Vect, p1Vect,pAubsive

def classifyNB(vec2Classify, p0Vect, p1Vect, pClass1):
	# 元素相乘
	print 111, vec2Classify
	print 222, p1Vect
	print 3333, vec2Classify * p1Vect
	p1 = sum(vec2Classify * p1Vect) + log(pClass1)
	p0 = sum(vec2Classify * p0Vect) + log(1.0 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts, listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
	p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
	testEntry = ['love', 'my', 'dalmation']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
	testEntry = ['stupid','garbage']
	thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
	print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)

#  文件解析和完整的测试函数
def textParse(bigString):
	listOfTokens = re.split(r'\W*', bigString)
	# 只返回长度大于2的单词
	return [tok.lower() for tok in listOfTokens if len(tok) > 2]
def spamTest():
	# 文档的样本，分类样本，全部样本
	docList = []; classList = []; fullText = []
	for i in range(1,26):
		wordList = textParse(open('email/spam/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(1)
		wordList = textParse(open('email/ham/%d.txt' % i).read())
		docList.append(wordList)
		fullText.extend(wordList)
		classList.append(0)

    # 对这些单词创建向量
	vocabList = createVocabList(docList)

   # 这里取50的是因为：len(docList)=50, len(classList)=50
	trainingSet = range(50); testSet = []

	# 随机构建训练集
	for i in range(10):
		randIndex = int(random.uniform(0, len(trainingSet)))
		print randIndex
		testSet.append(trainingSet[randIndex])
		del(trainingSet[randIndex])
	print testSet
	print trainingSet
	trainMat = []; trainClass = []
	for docIndex in trainingSet:
		trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
		print len(setOfWords2Vec(vocabList, docList[docIndex]))
		trainClass.append(classList[docIndex])
	p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClass))
	print array(trainMat)
	print array(trainClass)
	print p0V
	print p1V
	print pSpam
	errorCount = 0

	# 对测试集分类
	for docIndex in testSet:
		wordVector = setOfWords2Vec(vocabList, docList[docIndex])
		if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
			errorCount += 1
	print 'the error rate is: ', float(errorCount) / len(testSet)


if __name__ == '__main__':
	listOPosts, listClasses = loadDataSet()
	print listOPosts
	print listClasses

	myVocabList = createVocabList(listOPosts)
	print myVocabList
	print setOfWords2Vec(myVocabList, listOPosts[0])
	print setOfWords2Vec(myVocabList, listOPosts[3])
	print '------------------'
	trainMat = []
	for postinDoc in listOPosts:
		vect = setOfWords2Vec(myVocabList,postinDoc)
		trainMat.append(vect)
	print trainMat
	# trainMat 是个32*5的向量
	print listClasses
	print '----------------'
	p0V, p1V, pAb = trainNB0(trainMat, listClasses)

	print p0V
	print p1V
	print pAb
	print '--------------------------------'
	testingNB()
	print '-----------test--4.6.1------'

	mySent = 'This book is the best bool on Python or M.L. I have ever laid eyes upon.'
	print mySent.split()
	regEx = re.compile('\\W*')
	# 除掉单词，数字外的任意字符串
	listOfTokens = regEx.split(mySent)
	print listOfTokens
    # 去掉空字符串
	print [tok.lower() for tok in listOfTokens if len(tok) > 0]

	print '-----------demo-------'
	emailText = open('email/ham/6.txt').read()
	print emailText
	listOfTokens = regEx.split(emailText)
	print listOfTokens
	print '----------test demo start---------------'

	spamTest()

