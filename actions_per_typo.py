# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 19:36:41 2019

@author: raphael
"""

folder = 'Caen'
folder_typo = 'Graphlets/kmeans_repres'


def get_typo_per_graph():
    typo_per_graph = {}
    with open(full_folder + '/typo_par_graph.csv', 'r') as to_read:
        csvr = csv.reader(to_read, delimiter = ';')
        header = csvr.next()
        for line in csvr:
            typo_per_graph[line[0]] = int(line[1])
    return typo_per_graph
    
def indicators_per_typo():    
    indics_per_typo = {}
    
    for gname in list_graphs:
        graph = Admin.import_graph(Graphs + gname)
        list_all = ClassicIndicators(graph).list_all()
        
        if not gname in typo_per_graph:
            continue
        this_typo = typo_per_graph[gname]
        
        if not this_typo in indics_per_typo:
            indics_per_typo[this_typo] = {indic : [] for indic in list_all}
        
        for indic in list_all:
            indics_per_typo[this_typo][indic].append(list_all[indic])
            
    means, medians = {}, {}
    
    for typo in indics_per_typo:
        means[typo] = {}
        medians[typo] = {}
        for indic in list_all:
            this_list = indics_per_typo[typo][indic]
            means[typo][indic] = np.mean(this_list)
            medians[typo][indic] = np.median(this_list)
    
            
    with open('%s/indics_per_cluster_means.csv' % full_folder, 'w') as to_write:
        csvw = csv.writer(to_write, delimiter = ';')
        csvw.writerow(['cluster'] + [indic for indic in list_all])
        
        for typo in indics_per_typo:
            row = [typo]
            for indic in list_all:
                row.append(round(means[typo][indic], 2))
                
            csvw.writerow(row)

                        
    with open('%s/indics_per_cluster_medians.csv' % full_folder, 'w') as to_write:
        csvw = csv.writer(to_write, delimiter = ';')
        csvw.writerow(['cluster'] + [indic for indic in list_all])
        
        for typo in indics_per_typo:
            row = [typo]
            for indic in list_all:
                row.append(round(medians[typo][indic], 2))
                
            csvw.writerow(row)
            
def plot_per_typo():
    for gname in typo_per_graph:
        this_typo = typo_per_graph[gname]        
        if not 'Plots' in os.listdir(full_folder):
            os.mkdir(full_folder + '/Plots/')
        if not str(this_typo) in os.listdir(full_folder + '/Plots/'):
            os.mkdir(full_folder + '/Plots/' + str(this_typo))
        svgname = gname.split('.')[0] + '.svg'
        bashCommand = 'ln -s ~/Graphs/%s/Gallery/%s %s/Plots/%s/%s' % (folder, svgname, full_folder, this_typo, svgname)        
        os.system(bashCommand)
            

        
  

import csv
import os
from graph_utils import ClassicIndicators, Admin
import numpy as np

full_folder = '../%s/%s' % (folder, folder_typo)
typo_per_graph = get_typo_per_graph()
Graphs = '../%s/Data/' % folder
list_graphs = os.listdir(Graphs)
plot_per_typo() 