#!/usr/bin/env python
#-*- coding:utf-8 -*-

from numpy import *


def loadDataSet():
	dataMat = []; labelMat = []
	fr = open('testSet.txt')
	for line in fr.readlines():
		lineArr = line.strip().split()
		dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
		labelMat.append(int(lineArr[2]))
	return dataMat, labelMat

def sigmoid(inX):
	return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn, classLabels):
	dataMatrix = mat(dataMatIn)
	# trainspose 将矩阵转置
	labelMat = mat(classLabels).transpose()
	# spape 输出矩阵的行列
	m,n = shape(dataMatrix)
	print m,n
	# 移动步长
	alpha = 0.001
	# 迭代次数
	maxCycles = 500
	# 生成3咧都是1的矩阵
	weights = ones((n,1))
	print weights
	for k in range(maxCycles):
		# 矩阵相乘
		# 这里有个公式要去研究一下，计算真实值和预测值的差值，根据差值去调整回归系数
		h = sigmoid(dataMatrix * weights)
		error = (labelMat - h)
		weights = weights + alpha * dataMatrix.transpose() * error
	return weights



if __name__ == '__main__':
	# print loadDataSet()

	dataArr, labelMat = loadDataSet()
	print gradAscent(dataArr, labelMat)
