# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:36:18 2019

@author: raphael
"""

from igraph import Graph
from graph_utils import Admin

folder = 'Caen'

def draw_graph(data, gallery, gname):
    graph = Admin.import_graph(data + '/' + gname)
    in_graph = [False]*len(graph.vs)
    filename = gname.split('.g')[0] + '.svg'
    layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
    graph.write_svg(gallery + '/' + filename, layout = layout)

def draw_folder(folder):
    folder = '../' + folder
    Data = folder + '/Data'
    Gallery = folder + '/Gallery'
    if not 'Gallery' in os.listdir(folder):
        os.mkdir(Gallery)
        
    print os.listdir(Data)
    
    for gname in os.listdir(Data):
        draw_graph(Data, Gallery, gname)
        
        
import os
        
draw_folder(folder)