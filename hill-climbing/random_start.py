#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Description: 用首选爬山并随机重新开始算法来解决8皇后问题。

import random

chess_status_count = 0 # 在一次求解中所搜索的棋盘总数
all_count = 0          # 大量测试所搜索的棋盘总数
success_time = 0       # 在多次求解中得到全局最优解的次数

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

def  hill_climbling_first_choice(status):
    '''随机选择相邻状态直到选择出一个比当前状态价值高的，立即返回。否则返回原状态。

    参数为棋盘摆放状态。
    '''
    global chess_status_count
    pos = [(x, y) for x in range(8) for y in range(8)]
    random.shuffle(pos)
    for col, row in pos:
        if status[col] == row:
            continue
        chess_status_count += 1
        status_copy = list(status)
        status_copy[col] = row
        if get_num_of_conglict(status_copy) < get_num_of_conglict(status):
            status[col] = row
            return status
    return status

def Queens():
    '''求解八皇后问题。

    初始棋盘是随机生成的。
    '''
    global chess_status_count, success_time, all_count
    chess_status_count = 0

    next_status = []
    for i in range(8):
        random_num = random.randint(0, 7)
        next_status.append(random_num)

    current_status = []
    # 若当前状态与下一状态不相等时，即未达到最优解时，继续循环求解。
    while current_status != next_status:
        current_status = list(next_status)
        next_status = hill_climbling_first_choice(next_status)
    if get_num_of_conglict(current_status) is 0:
        success_time += 1

    # 当冲突数不为零时，随机重新开始
    if get_num_of_conglict(current_status) != 0:
        all_count += chess_status_count
        Queens()

if __name__ == '__main__':
    all_count = 0
    success_time = 0
    test_num = 1000
    for i in range(test_num):
        Queens()
        all_count += chess_status_count
    print "[8queen_hill_climbing_first_choice_with_random_restart.py Test]"
    print "Tests number: 1000"
    print "Average search cost: %.2f chessboards" % (all_count / (test_num + 0.0))
    print "Percentage of solved problems: %.2f%%" % (success_time / (test_num + 0.0) * 100)
