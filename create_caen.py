# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 15:50:11 2019

@author: raphael
"""

import csv
from igraph import Graph

lines = []
with open('../alters_caen.csv', 'r') as to_read:
    csvr = csv.reader(to_read, delimiter = ';')
    header = csvr.next()
    for line in csvr:
        lines.append(line)

gname = 'A01' 
graph = Graph()    
neighbors_per_vertex = {}
id_per_name, current_id = {}, 0  
        
for line in lines:
    if gname != line[0]:
        print gname
        for vertex in neighbors_per_vertex:
            for nei in neighbors_per_vertex[vertex]:
                graph.add_edge(id_per_name[vertex], id_per_name[nei])
        print '../Caen/Data/%s.gml' % gname
        graph.write_gml('../Caen/Data/%s.gml' % gname)
        graph = Graph()
        neighbors_per_vertex = {}
        gname = line[0]
        current_id = 0
    
    vertex = line[5]
    id_per_name[vertex] = current_id
    current_id += 1
    neighbors_per_vertex[vertex] = []
    for nei in line[6:]:
        if nei == '' or nei == '  ':
            break
        neighbors_per_vertex[vertex].append(nei)
    graph.add_vertex(name = vertex)
    
    