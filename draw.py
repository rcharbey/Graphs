# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:36:18 2019

@author: raphael
"""

from graph_utils import Admin
import argparse
import os
        

folder = 'Caen'

class Drawer(object):
    def __init__(self, folder):
        self.folder = folder
        self.Data = os.path.join(folder, 'Data')
        self.Gallery = os.path.join(folder, 'Gallery')
        
        if not 'Gallery' in os.listdir(folder):
            os.mkdir(self.Gallery)
        
    def draw_graph(self, data, gallery, gname):
        graph = Admin.import_graph(os.path.join(data, gname))
        svgname = gname.split('.')[0] + '.svg'
        layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
        graph.write_svg(os.path.join(gallery, svgname), layout = layout)
            
    def draw_folder(self):
        for root, dirs, files in os.walk(self.Data, topdown=True):
            gallery = root.replace(self.Data, self.Gallery)
            if not os.path.exists(gallery):
                os.mkdir(gallery)
            for name in files:
                self.draw_graph(root, gallery, name)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='data folder')
    parser.add_argument('folder', type=str,
                        help='the folder containing the graphs')
    args = vars(parser.parse_args())
    Drawer(args['folder']).draw_folder()