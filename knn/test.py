#!/usr/bin/env python
#-*- codiing:utf-8 -*-

import knn
from knn import *
import matplotlib
import matplotlib.pyplot as plt


def test_classify0():
    group, labels = createDataSet()
    k = classify0([0,0], group, labels, 3)
    print k

def show_file2matrix(file_name):
    reload(knn)
    datingDataMat, datingLabels = knn.file2matrix(file_name)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,1], datingDataMat[:,2], 15.0*array(datingLabels), 15.0*array(datingLabels))
    plt.show()

if __name__ == "__main__":
    show_file2matrix('../data/datingTestSet2.txt')
