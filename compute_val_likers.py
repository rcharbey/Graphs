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

tab_n = []
tab_m = []
tab_diam = []
tab_densite = []
tab_transit = []
tab_centralisation = []
tab_nb_com = []
tab_mod = []

for graph_name in listdir(DATA):
    g = Graph.Read_GML('%s/%s' % (DATA, graph_name))
    ci = ClassicIndicators(g)
    
    tab_n.append(len(g.vs))
    tab_m.append(len(g.es))
    tab_diam.append(ci.diameter())
    tab_densite.append(ci.density())
    tab_transit.append(ci.clustering_coeff())
    tab_centralisation.append(ci.freeman_betweenness())
    tab_nb_com.append(ci.nb_louvain_com())
    tab_mod.append(ci.modularity()) 
    print graph_name
    
def moyenne(t):
    round(mean(t), 2)
    
print '%s : %s' % ('n', moyenne(tab_n))
print '%s : %s' % ('m', moyenne(tab_m))
print '%s : %s' % ('diametre', moyenne(tab_diam))
print '%s : %s' % ('densite', moyenne(tab_densite))
print '%s : %s' % ('transitivité', moyenne(tab_transit))
print '%s : %s' % ('centralisation Freeman', moyenne(tab_centralisation))
print '%s : %s' % ('nb communautés', moyenne(tab_nb_com))
print '%s : %s' % ('modularité', moyenne(tab_mod))
    
    