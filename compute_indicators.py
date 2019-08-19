# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:24:34 2018

@author: raphael
"""

from os import listdir
from igraph import Graph

from indicators import Indicators

import csv

DATA = '../Sqily/Data/Communities'

dict_results = {}
list_indicators = Indicators.__list_indicators__()

for graph_name in listdir(DATA):
    ego_name = graph_name.split('.')[0]
    
    print(graph_name)
    g = Graph.Read_GML('%s/%s' % (DATA, graph_name))
    ci = Indicators(g)
    
    this_graph_results = {}
    
    for indicator in list_indicators:
        this_graph_results[indicator] = ci.__getattribute__(indicator)()
    
    dict_results[ego_name] = this_graph_results
    
list_ego = dict_results.keys()
with open('%s/../Results/indics_per_network.csv' % DATA, 'w') as to_write:
    csvw = csv.writer(to_write, delimiter = ';')
    csvw.writerow(['network'] + list_indicators)
    for ego in dict_results:
        if dict_results[ego]['n'] == 0:
            continue
        csvw.writerow([ego] + [dict_results[ego][indic] for indic in list_indicators])
    