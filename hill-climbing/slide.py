#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: 陈炜健
# Description: 用最陡爬山算法加侧向移动优化来解决8皇后问题。

import random

chess_status_count = 0  # 在一次求解中所搜索的棋盘总数
success_time = 0        # 在多次求解中得到全局最优解的次数
MAX_SIDEWAYS_MOVE = 100 # 在一次求解中允许侧向移动的最大次数
sideways_move_count = 0 # 记录在一次求解中已走的侧向移动次数

def get_num_of_conglict(status):
    '''判断该棋盘摆放状态的冲突数。

    参数为棋盘摆放状态。
    '''
    num = 0
    for i in range(len(status)):
        for j in range(i + 1, len(status)):
            if status[i] == status[j]:
                num += 1
            offset = j - i
            if abs(status[i]-status[j]) == offset:
                num += 1
    return num

def  hill_climbing_steepest_ascent(status):
    '''返回所有相邻状态中皇后之间冲突数最少的状态。否则返回原状态。

    参数为棋盘摆放状态。
    '''
    global chess_status_count, sideways_move_count
    convert = {}
    length = len(status)
    for col in range(length):
        for row in range(length):
            if status[col] == row:
                continue
            status_copy = list(status)
            status_copy[col] = row
            convert[(col,row)] = get_num_of_conglict(status_copy)
            chess_status_count += 1

    answers = [] # 最佳后继集合
    conflict_now = get_num_of_conglict(status) # 当前皇后冲突对数
    conflict_better = conflict_now

    # 遍历存储所有可能后继的字典，找出最佳后继
    for key,value in convert.iteritems():
        if value < conflict_better:
            conflict_better = value
    if conflict_now != conflict_better:
        for key,value in convert.iteritems():
            if value == conflict_better:
                answers.append(key)

    if len(answers) == 0 and sideways_move_count < MAX_SIDEWAYS_MOVE:
        for key,value in convert.iteritems():
            if value == conflict_now:
                answers.append(key)
        if len(answers) == 0:
            return status
        else:
            sideways_move_count += 1

    # 随机选择后续集合中的一个
    if len(answers) > 0:
        x = random.randint(0, len(answers)-1)
        col = answers[x][0]
        row = answers[x][1]
        status[col] = row

    return status

def Queens():
    '''求解八皇后问题。

    解出的答案不一定为全局最优解，即冲突数不一定为零。
    初始棋盘摆放状态是随机生成的。
    '''
    global chess_status_count, success_time
    chess_status_count = 0

    next_status = []
    for i in range(8):
        random_num = random.randint(0, 7)
        next_status.append(random_num)

    current_status = []
    # 若当前状态与下一状态不相等时，即未达到最优解时，继续循环求解。
    while current_status != next_status:
        current_status = list(next_status)
        next_status = hill_climbing_steepest_ascent(next_status)
    if get_num_of_conglict(current_status) is 0:
        success_time += 1

if __name__ == '__main__':
    all_count = 0
    success_time = 0
    test_num = 1000
    for i in range(test_num):
        sideways_move_count = 0
        Queens()
        all_count += chess_status_count
    print "[8queen_hill_climbing_steepest_ascent.py Test]"
    print "Tests number: 1000"
    print "Average search cost: %.2f chessboards" % (all_count / (test_num + 0.0))
    print "Percentage of solved problems: %.2f%%" % (success_time / (test_num + 0.0) * 100)
