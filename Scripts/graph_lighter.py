#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 15:39:08 2018

@author: raphael
"""
import os

for graph in os.listdir('Graphs'):
     
    ego = graph.split('.')[0]
    with open('Graphs/%s' % graph, 'r') as to_read:
        with open('Graphs_light/%s' % graph, 'w') as to_write:
            to_write.write('graph \n')
            to_write.write('[\n')
            to_write.write('  directed 0\n')
            to_write.write('  ego \"%s\"\n' % ego)
            
            to_read.next()
            to_read.next()
            to_read.next()
            to_read.next()
            to_read.next()
            to_read.next()
            to_read.next()
            
            for line in to_read:
                if 'nbcomments' in line:
                    continue
                if 'sumcommentslikes' in line:
                    continue
                if 'cluster' in line:
                    continue
                if 'nblikes' in line:
                    continue
                to_write.write(line)