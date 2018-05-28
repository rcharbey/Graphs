# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:24:34 2018

@author: raphael
"""

from os import listdir
from igraph import Graph

from graph_utils import ClassicIndicators
from numpy import mean

DATA = '../Data/Graphs_likers'

dict_results = {
    'n' : [], 
    'm' : [], 
    'diametre' : [], 
    'densite' : [], 
    'transit' : [], 
    'centralisation' : [], 
    'nb_com' : [], 
    'modularite' : []
}

for graph_name in listdir(DATA):
    
    if graph_name != '030aefe7d1ee5be1bc17e69e4a452eb3.gml':
        continue
    g = Graph.Read_GML('%s/%s' % (DATA, graph_name))
    ci = ClassicIndicators(g)
    
    dict_results['n'].append(len(g.vs))
    dict_results['m'].append(len(g.es))
    dict_results['diam'].append(ci.diameter())
    dict_results['densite'].append(ci.density())
    dict_results['transit'].append(ci.clustering_coeff())
    dict_results['centralisation'].append(ci.freeman_betweenness())
    dict_results['nb_com'].append(ci.nb_louvain_com())
    dict_results['modularite'].append(ci.modularity()) 
    print graph_name
    
def moyenne(t):
    return round(mean(t), 2)
    
for indic in dict_results:
    print '%s : %s' % (indic, moyenne(dict_results[indic]))
    