# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 19:25:57 2019

@author: raphael
"""

from graph_utils import Indicators
from os import listdir

import numpy as np
import matplotlib.pyplot as plt

#plt.plot(base[:-1], len(data)-cumulative, c='green')

plt.show()

percent_per_graph = []

data = '../Facebook/Data/'

for graph in listdir(data):
    gloc = data + graph
    ind = Indicators(gloc)
    if ind.n() <= 150 and ind.n() > 20:
        per = ind.nodes_in_max_cc()
        if per == 0:
            continue
        percent_per_graph.append(round(100*per))
        
print len(percent_per_graph)
print percent_per_graph
values, base = np.histogram(percent_per_graph, bins=40)
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative, c='blue')

plt.show()