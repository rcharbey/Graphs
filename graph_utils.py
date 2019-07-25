from collections import deque
import os
from os import path

from igraph import Graph

class Admin(object):
    @staticmethod
    def import_graph(graph_loc):
        if isinstance(graph_loc, Graph):
            return graph_loc
        extension = graph_loc.split('.')[-1]
        if extension == 'edgelist':
            return Graph.Read_Edgelist(graph_loc)
        elif extension == 'gml':
            return Graph.Read_GML(graph_loc)

    @staticmethod
    def draw_graph(folder, ego, name, svg = False):
        graph = Admin.create_graph(folder, ego, name)
        in_graph = [False]*len(graph.vs)

        if svg == True:
            place = os.path.expanduser('~/GALLERY/%s/%s/Graphs/%s.svg' % (folder, ego, name))
            layout = graph.layout_fruchterman_reingold(repulserad = len(graph.vs)**3)
            graph.write_svg(place, layout = layout)
            return

        place = os.path.expanduser('~/GALLERY/%s/%s/Graphs/%s.json' % (folder, ego, name))

        file_graph = open(place, 'w')
        file_graph.write('{\n "nodes": [\n')
        for v in graph.vs:
            in_graph[v.index] == True
            file_graph.write('  {')
            file_graph.write('\n   "id": "%s"' % v.index)
            file_graph.write(',\n   "label": "%s"' % v['name'])
            if 'nbcomments' in v.attributes():
                file_graph.write(',\n   "comments": "%s"' % int(v['nbcomments']))
#            if 'nblikes' in v.attributes():
#               file_graph.write(',\n   "likes": "%s"' % int(v['nblikes']))
            else:
               file_graph.write('\n')
            if len(graph.vs) == v.index + 1:
                file_graph.write('\n }\n')
            else:
                file_graph.write('\n  },\n')
        file_graph.write(' ],\n')
        file_graph.write(' "edges": [\n')
        for e in graph.es:
            file_graph.write('  {\n')
            file_graph.write('   "id": "%s",\n' % e.index)
            file_graph.write('   "source": "%s",\n' % e.source)
            file_graph.write('   "target": "%s"' % e.target)
            if 'color' in e.attributes():
                file_graph.write(',\n   "color": "%s"\n' % e['color'])
            else:
                file_graph.write('\n')
            if len(graph.es) == e.index + 1:
                file_graph.write(' }\n')
            else:
                file_graph.write('  },\n')
        file_graph.write(' ]\n}')
        file_graph.close()

    @staticmethod
    def write_graph(graph, gname, format = 'gml'):
        graph.write(gname, format = format)
        
    @staticmethod
    def write_edgelist(graph, ego):
        with open('../Data/Edgelists/%s.edgelist' % ego, 'w') as to_write:
            for e in graph.es:
                to_write.write('%s %s\n' % (e.source, e.target))    
                
class Leda(object):
    def __init__(self, folder):
        self.folder = folder
        
    def write(self, gname):
        nodes = []
        edges = []
        nb_nodes = 0
        nb_edges = 0
        with open(input_folder+patch_folder +fname+'.gml','r') as to_read:
            source = -1
            for line in to_read:
                splited_line = line.split(' ')
                if 'id' in splited_line:
                    nodes.append(int(splited_line[5]))
                    nb_nodes +=1
                if 'source' in splited_line:
                    source = int(splited_line[5])
                if 'target' in splited_line:
                    edges.append((int(splited_line[5]),source))
                    nb_edges +=1
        leda_fname = '{}.gw'.format(fname)
        leda_file = open(output_folder+leda_fname,'w')
        leda_file.write('#header section\n')
        leda_file.write('LEDA.GRAPH\n')
        leda_file.write('int\n')
        leda_file.write('int\n')
        leda_file.write('-2\n')
        leda_file.write('#nodes section\n')
        leda_file.write(str(nb_nodes)+'\n')
        for i in range(nb_nodes):
            leda_file.write('|{{{}}}|\n'.format(i))
        leda_file.write('#edges section\n')
        leda_file.write(str(nb_edges)+'\n')
        for i in range(1,nb_edges+1):
            leda_file.write('{} {} {}\n'.format(edges[i-1][0],edges[i-1][1],0))
        