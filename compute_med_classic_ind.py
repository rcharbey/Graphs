# -*- coding: utf-8 -*-
"""
Created on Mon May 28 16:24:34 2018

@author: raphael
"""

from os import listdir
from igraph import Graph

from graph_utils import ClassicIndicators
from numpy import mean, median

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

i = 0
for graph_name in listdir(DATA):
    
    print graph_name
    g = Graph.Read_GML('%s/%s' % (DATA, graph_name))
    ci = ClassicIndicators(g)
    
    dict_results['n'].append(len(g.vs))
    dict_results['m'].append(len(g.es))
    dict_results['diametre'].append(ci.diameter())
    dict_results['densite'].append(ci.density())
    dict_results['transit'].append(ci.clustering_coeff())
    dict_results['centralisation'].append(ci.freeman_betweenness())
    dict_results['nb_com'].append(ci.nb_louvain_com())
    dict_results['modularite'].append(ci.modularity())
    
    i += 1
    if i > 5:
        break
    
def moyenne(t):
    return round(mean(t), 2)
    
for indic in dict_results:
    new_indic = [x for x in dict_results[indic] if type(x) == float]
    print new_indic
    print '%s : %s' % (indic, round(median(new_indic), 2))
    