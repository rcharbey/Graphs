# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:24:34 2018

@author: raphael
"""

from os import listdir
from igraph import Graph

from indicators import Indicators

import csv

DATA = '../Sqily/Data'

list_indics = [
    'n',
    'm', 
    'diametre', 
    'densite', 
    'transit', 
    'centralisation', 
    'nb_com', 
    'modularite'
]

dict_results = {}

for graph_name in listdir(DATA):
    ego_name = graph_name.split('.')[0]
    
    print(graph_name)
    g = Graph.Read_GML('%s/%s' % (DATA, graph_name))
    ci = Indicators(g)
    
    this_graph_results = {}
    
    this_graph_results['n'] = len(g.vs)
    this_graph_results['m'] = len(g.es)
    this_graph_results['diametre'] = ci.diameter()
    this_graph_results['densite'] = ci.density()
    this_graph_results['transit'] = ci.clustering_coeff()
    this_graph_results['centralisation'] = ci.freeman_betweenness()
    this_graph_results['nb_com'] = ci.nb_communities()
    this_graph_results['modularite'] = ci.modularity()
    
    dict_results[ego_name] = this_graph_results
    
list_ego = dict_results.keys()
with open('%s/../Results/indics_per_network.csv' % DATA, 'w') as to_write:
    csvw = csv.writer(to_write, delimiter = ';')
    csvw.writerow(['network'] + list_indics)
    for ego in dict_results:
        if dict_results[ego]['n'] == 0:
            continue
        csvw.writerow([ego] + [dict_results[ego][indic] for indic in list_indics])
    