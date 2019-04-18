# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:28:28 2019

@author: raphael
"""

corpus = 'P1'
indic = 'com_link_from_first_com'


class Corpus(object):
    def __init__(self, corpus_name):
        self.name = corpus_name
        self.folder = '../%s' % corpus_name
        self.Graphs_fold = self.folder + '/Data'
        self.Indics_fold = self.folder + '/Indics_per_graph' 
        
        self.list_gnames = os.listdir(self.Graphs_fold)  

    def compute_indic(self, indic_name):    
        indic_per_graph = {}
        for gname in self.list_gnames:
            print gname
            indic_per_graph[gname] = getattr(Indicators(self.Graphs_fold + '/' + gname), indic_name)()
            
        out = self.Indics_fold + '/%s_per_graph.csv' % indic_name
            
        with open(out, 'w') as to_write:
            csvw = csv.writer(to_write, delimiter = ';')
            csvw.writerow(['graph', indic_name])
            for gname in indic_per_graph:
                if type(indic_per_graph[gname]) == float:
                    csvw.writerow([gname, indic_per_graph[gname]])
                else:
                    csvw.writerow([gname] + indic_per_graph[gname])
        
        
import os
from graph_utils import Indicators
import csv  

if __name__ == '__main__':
    Corpus(corpus).compute_indic(indic)
    