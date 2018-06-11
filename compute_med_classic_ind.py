# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:24:34 2018

@author: raphael
"""

from os import listdir
from igraph import Graph

from graph_utils import ClassicIndicators
from numpy import mean, median

graphs_type = 'likers'
DATA = '../Data/Graphs_%s' % graphs_type

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
i = 0
for graph_name in listdir(DATA):
    ego_name = graph_name.split('.')[0]
    
    print graph_name
    g = Graph.Read_GML('%s/%s' % (DATA, graph_name))
    ci = ClassicIndicators(g)
    
    this_graph_results = {}
    
    this_graph_results['n'] = len(g.vs)
    this_graph_results['m'] = len(g.es)
    this_graph_results['diametre'] = ci.diameter()
    this_graph_results['densite'] = ci.density()
    this_graph_results['transit'] = ci.clustering_coeff()
    this_graph_results['centralisation'] = ci.freeman_betweenness()
    this_graph_results['nb_com'] = ci.nb_louvain_com()
    this_graph_results['modularite'] = ci.modularity()
    
    dict_results[ego_name] = this_graph_results
    
    i += 1
    if i > 5:
        break
    
list_ego = dict_results.keys()
with open('../Results/indics_classics_par_reseau_%s.csv' % graphs_type) as to_write:
    csvw = csv.writer(to_write, delimiter = ';')
    csvw.writerow(['ego'] + list_indics)
    for ego in dict_results:
        for indic in list_indics:
            csvw.writerow(dict_results[ego][indic])
    