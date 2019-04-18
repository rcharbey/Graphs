# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 11:25:59 2019

@author: raphael
"""

from graph_utils import Enumerate
import os
from igraph import Graph
import csv

folder = '50_150_R'
Data = '../%s/Data/' % folder
Graphlets = '../%s/Graphlets/' % folder
Positions = Graphlets + 'Positions/'

with open(Graphlets+'graphlets_per_ego.csv', 'w') as to_write:
    csvw = csv.writer(to_write)
    csvw.writerow(['graph', 'class', 'size'] + ['graphlet_%s' % i for i in range(10,31)])
    

for classe in os.listdir(Data):
    classe_loc = Data + classe
    for gname in os.listdir(classe_loc):
        if not gname.split('.')[-2].split('_')[-2] == 'r':
            continue
        print gname
        graph_loc = classe_loc + '/' + gname
        graph = Graph.Read_Edgelist(graph_loc)
        enum = Enumerate(graph, 5)
        graphlet_count, position_count = enum.characterize_with_patterns()
        with open(Data+gname+'.csv', 'w') as to_write:
            csvw = csv.writer(to_write)
            csvw.writerow(graphlet_count)
            
            
        gname_2 = '' 
        for i in gname.split('_')[3:]:
            gname_2 += str(i)
    
        with open(Graphlets+'graphlets_per_ego.csv', 'a') as to_write:
            csvw = csv.writer(to_write)
            row = [gname_2, classe, 'R%s' % len(graph.vs)] + graphlet_count[10:31]
            csvw.writerow(row)
            
        with open(Positions+gname+'.csv', 'w') as to_write:
            csvw = csv.writer(to_write)
            for alter in positions:
                csvw.writerow(alter)
                
        print '... OK!'