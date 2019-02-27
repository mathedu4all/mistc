#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    curve subdivision tools.

"""

import matplotlib.pyplot as plt
import numpy as np
import time


class Spline(object):
    """
        Closed curve points coordinates series.
    """

    def __init__(self, points,weights=[],degree=2):
        self.pts = points
        self.weights = weights
        if len(self.weights) < 2:
            self.weights = np.array(self.pascal_triangle(degree))/2**(degree-1)
            self.degree = degree
        else:
            self.weights = np.array(self.weights)/sum(self.weights)
            self.degree = len(weights)

    def pascal_triangle(self,level):
        if level == 1:
            return [1]
        if level == 2:
            return [1,1]
        else:
            upper = self.pascal_triangle(level-1)
            row = [1]
            for index in range(len(upper)-1):
                row.append(upper[index]+upper[index+1])
            row.append(1)
            return row

    def split(self):
        n = len(self.pts)
        A = np.zeros((2 * n, n))
        for i in range(2 * n):
            if i % 2 == 0:
                A[i, i//2] = 1
            else:
                A[i, (i-1)//2%(n)] = 0.5
                A[i, ((i-1)//2+1)%(n)]=0.5
        self.pts = np.dot(A,self.pts)

    def average(self):
        n = len(self.pts)
        A = np.zeros((n,n))
        for i in range(n):
            for j in range(self.degree):
                A[i, (i+j) % n] = self.weights[j]
        self.pts = np.dot(A, self.pts)

    def closed_pts(self):
        return np.vstack([self.pts, self.pts[0, :]])


def tellme(s):
    print(s)
    plt.title(s, fontsize=16)
    plt.draw()


if __name__ == '__main__':

    ##################################################
    # plt setup.

    plt.clf()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.axis([-1., 1., -1., 1.])
    plt.setp(plt.gca(), autoscale_on=False)

    tellme(u'你即将开启探索曲线细分之旅，点击鼠标开始')

    plt.waitforbuttonpress()

    ##################################################
    # Input points of curve.

    while True:
        tellme(u'点击左键添加曲线上的点，点击中键结束.')
        pts = np.asarray(plt.ginput(50, timeout=-1))
        if len(pts) < 2:
            tellme(u'至少需要两个点哦~')
            time.sleep(5)  # Wait a second
            continue
        else:
            closed_pts = np.vstack([pts, pts[0, :]])
            line1 = plt.plot(closed_pts[:, 0], closed_pts[:, 1], 'r-')
            line2 = plt.plot(closed_pts[:, 0], closed_pts[:, 1], 'ro')

        tellme(u'满意吗？敲下键盘继续，点击鼠标重来.')

        if plt.waitforbuttonpress():
            break

        for l in line1:
            l.remove()
        for l in line2:
            l.remove()

    ##################################################
    # create Spline object and do the subdivision.

    spline = Spline(points=pts)
    # #Uncomment these lines to set the initial curve as square and ignore the input points.
    # spline = Spline(points=np.array([[-0.9,0.9],[0.9,0.9],[0.9,-0.9],[-0.9,-0.9]]),weights=[1,-2,3])
    # closed_pts = spline.closed_pts()
    # line1 = plt.plot(closed_pts[:, 0], closed_pts[:, 1], 'r-')
    # line2 = plt.plot(closed_pts[:, 0], closed_pts[:, 1], 'ro')

    line3 = plt.plot(closed_pts[:, 0], closed_pts[:, 1], 'b-')
    line4 = plt.plot(closed_pts[:, 0], closed_pts[:, 1], 'bo')

    while True:
        tellme(u'点击鼠标执行细分，敲击键盘结束.')
        if plt.waitforbuttonpress():
            break
        spline.split()
        closed_pts = spline.closed_pts()
        line4[0].set_data((closed_pts[:, 0], closed_pts[:, 1]))
        tellme(u'分割(取中点).')
        plt.waitforbuttonpress()
        spline.average()
        closed_pts = spline.closed_pts()
        line4[0].set_data((closed_pts[:, 0], closed_pts[:, 1]))
        line3[0].set_data((closed_pts[:, 0], closed_pts[:, 1]))
        tellme(u'取平均(移动点).')
        plt.waitforbuttonpress()




