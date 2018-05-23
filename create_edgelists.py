#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 14:57:26 2018

@author: raphael
"""

from os import listdir
from graph_utils import Admin

for gname in listdir('../Data/Graphs'):
    egoname = gname.split('.')[0]
    Admin.write_edgelist(Admin.import_graph(egoname), egoname) 