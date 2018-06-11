from collections import deque
import os

from igraph import Graph

class Admin(object):
    @staticmethod
    def import_graph(ego):
        return Graph.Read_GML(os.path.expanduser('../Data/Graphs_friends/%s.gml' % ego))

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
    def write_graph(graph, folder, ego, name):
        graph.write('GALLERY/%s/%s/Graphs/%s.gml' % (folder, ego, name), format = 'gml')
        
    @staticmethod
    def write_edgelist(graph, ego):
        with open('../Data/Edgelists/%s.edgelist' % ego, 'w') as to_write:
            for e in graph.es:
                to_write.write('%s %s\n' % (e.source, e.target))


class Enumerate_directed(object):
    DICT_PATTERNS = {
        '[1, 1, 6]' : (1, '021D'),
        '[2, 3, 3]' : (2, '021U'),
        '[1, 3, 4]' : (3, '021C'),
        '[3, 4, 5]' : (4, '111D'),
        '[1, 4, 7]' : (5, '111U'),
        '[2, 4, 6]' : (6, '030T'),
        '[4, 4, 4]' : (7, '030C'),
        '[4, 4, 8]' : (8, '201'),
        '[5, 5, 6]' : (9, '120D'),
        '[2, 7, 7]' : (10, '120U'),
        '[4, 5, 7]' : (11, '120C'),
        '[5, 7, 8]' : (12, '210'),
        '[8, 8, 8]' : (13, '300')
     }

    DICT_POSITIONS = [
        {1 : 1, 6 : 2}, #1
        {2 : 6, 3 : 7}, #2
        {1 : 3, 3 : 4, 4 : 5}, #3
        {3 : 12, 4 : 13, 5 : 14}, #4
        {1 : 15, 4 : 16, 7 : 17},#5
        {2 : 9, 4 : 10, 6 : 11}, #6
        {4 : 8}, #7
        {4 : 25, 8 : 26},#8
        {5 : 20, 6 : 21},#9
        {2 : 18, 7 : 19},#10
        {4 : 22, 5 : 23, 7 : 24},#11
        {5 : 27, 7 : 28, 8 : 29},#12
        {8 : 30},#13
    ]

    def __init__(self, graph, k):
        self.patterns_tab = []
        self.positions_tab = []
        self.special_patterns_dict = {}
        self._graph = graph
        self._k = k

    def create_list_neighbors(self):
        for v in self._graph.vs:
            v['list_neighbors'] = {'ALL' : set(), 'IN' : set(), 'OUT' : set()}
        for e in self._graph.es:
            if e.target == e.source:
                continue
            self._graph.vs[e.target]['list_neighbors']['ALL'].add(e.source)
            self._graph.vs[e.source]['list_neighbors']['ALL'].add(e.target)
            self._graph.vs[e.target]['list_neighbors']['IN'].add(e.source)
            self._graph.vs[e.source]['list_neighbors']['OUT'].add(e.target)
        for v in self._graph.vs:
            v['list_neighbors'] = \
                {
                    'ALL' : sorted(list(v['list_neighbors']['ALL']), reverse = True),
                    'IN' : sorted(list(v['list_neighbors']['IN']), reverse = True),
                    'OUT' : sorted(list(v['list_neighbors']['OUT']), reverse = True)
                }

    def graph_to_triad_index(self, graph_sub):
        tab = [0,0,0]
        for e in graph_sub.es:
            tab[e.target] += 1
            tab[e.source] += 3
        tab.sort()
        return tab

    def index_pattern(self, graph_sub):
        if len(graph_sub.vs) != self._k:
            return
        new_pattern, new_pattern_name = self.DICT_PATTERNS[str(self.graph_to_triad_index(graph_sub))]
        self.patterns_tab[new_pattern - 1] += 1
        new_positions = self.DICT_POSITIONS[new_pattern - 1]
        for v in graph_sub.vs:
            self.positions_tab[v['id_principal']][new_positions[v.indegree() + 3*v.outdegree()] - 1] += 1

    def in_neighborhood_vsub(self, list_neighbors, length_vsub):
        for n in list_neighbors['ALL']:
            if self._graph.vs[n]['id_sub'] != -1 and self._graph.vs[n]['id_sub'] != length_vsub-1:
                return True
        return False

    def add_vertex(self, graph_sub, vertex):
        vertex['id_sub'] = len(graph_sub.vs)
        graph_sub.add_vertex(name = vertex['name'], **{'id_principal' : vertex.index})

    def extend_subgraph(self, graph_sub, v, vext):
        if len(graph_sub.es) > 0 :
            self.index_pattern(graph_sub)
        if len(graph_sub.vs) == self._k:
            return
        while vext:
            new_vertex = vext.pop()
            vext2 = list(vext)
            self.add_vertex(graph_sub, new_vertex)
            for nei_of_new_vertex in new_vertex['list_neighbors']['ALL']:
                u = self._graph.vs[nei_of_new_vertex]
                if u.index >= v.index:
                    if u['id_sub'] == -1 :
                        if not self.in_neighborhood_vsub(u['list_neighbors'], len(graph_sub.vs)):
                            vext2.append(u)
                    else:
                        if u.index in new_vertex['list_neighbors']['IN']:
                            graph_sub.add_edge(u['id_sub'], len(graph_sub.vs) - 1)
                        if u.index in new_vertex['list_neighbors']['OUT']:
                            graph_sub.add_edge(len(graph_sub.vs) - 1, u['id_sub'])
                else:
                    break

            self.extend_subgraph(graph_sub, v, vext2)
            graph_sub.delete_vertices(new_vertex['id_sub'])
            new_vertex['id_sub'] = -1

    def characterize_directed_with_patterns(self):
        self.create_list_neighbors()
        self.patterns_tab = 13*[0]
        for v in self._graph.vs:
            self.positions_tab.append(30*[0])
            v['id_sub'] = -1
        for v in self._graph.vs:
            graph_sub = Graph(directed = True)
            v['id_sub'] = 0
            if not 'name' in v.attributes():
                v['name'] = str(v.index)
            graph_sub.add_vertex(name = v['name'], **{'id_principal' : v.index, 'evol_class' : 1, 'pattern_sub' : 0})

            vext = []
            for nei in v['list_neighbors']['ALL']:
                if nei > v.index:
                    vext.append(self._graph.vs[nei])

            if len(vext) > 0:
                self.extend_subgraph(graph_sub, v, vext)
            v['id_sub'] = -1
        print self.patterns_tab
        for pos in self.positions_tab:
            print pos
        return (self.patterns_tab, self.positions_tab)


class Enumerate(object):
    DICT_PATTERNS = {
        '[1, 1]' : 1,
        '[1, 1, 2]' : 2,
        '[2, 2, 2]' : 3,
        '[1, 1, 2, 2]' : 4,
        '[1, 1, 1, 3]' : 5,
        '[1, 2, 2, 3]' : 6,
        '[2, 2, 2, 2]' : 7,
        '[2, 2, 3, 3]' : 8,
        '[3, 3, 3, 3]' : 9,
        '[1, 1, 2, 2, 2]' : 10,
        '[1, 1, 1, 1, 4]' : 11,
        '[1, 1, 1, 2, 3]' : 12,
        '[1, 2, 2, 2, 3]' : (1,2,(13,17)),
        '[1, 1, 2, 3, 3]' : 14,
        '[1, 1, 2, 2, 4]' : 15,
        '[2, 2, 2, 2, 2]' : 16,
        '[1, 2, 3, 3, 3]' : 18,
        '[1, 2, 2, 3, 4]' : 19,
        '[2, 2, 2, 2, 4]' : 20,
        '[2, 2, 2, 3, 3]' : (3,3,(21,22)),
        '[1, 3, 3, 3, 4]' : 23,
        '[2, 2, 3, 3, 4]' : 24,
        '[2, 2, 2, 4, 4]' : 25,
        '[2, 3, 3, 3, 3]' : 26,
        '[3, 3, 3, 3, 4]' : 27,
        '[2, 3, 3, 4, 4]' : 28,
        '[3, 3, 4, 4, 4]' : 29,
        '[4, 4, 4, 4, 4]' : 30
    }

    DICT_POSITIONS = [
        {1 : 1}, #1
        {1 : 2, 2 : 3}, #2
        {2 : 4}, #3
        {1 : 5, 2: 6}, #4
        {1 : 7, 3 : 8}, #5
        {1 : 9, 2 : 10, 3 : 11}, #6
        {2 : 12},#7
        {2 : 13, 3 : 14},#8
        {3 : 15},#9
        {1 : 16, 2 : (1,(17,18))},#10
        {1 : 19, 4 : 20},#11
        {1 : (2,(21,22)), 2 : 23, 3 : 24},#12
        {1 : 25, 2 : (1,(26,27)), 3 : 28},#13
        {1 : 29, 2 : 30, 3 : 31},#14
        {1 : 32, 2 : 33, 4 : 34},#15
        {2 : 35},#16
        {1 : 36, 2 : (3,(38,37)), 3 : 39},#17
        {1 : 40, 2 : 41, 3 : (1,(42,43))},#18
        {1 : 44, 2 : 45, 3 : 46, 4 : 47},#19
        {2 : 48, 4 : 49},#20
        {2 : (2,(50, 51)), 3 : 52},#21
        {2 : 53, 3 : 54},#22
        {1 : 55, 3 : 56, 4 : 57},#23
        {2 : 58, 3 : 59, 4 : 60},#24
        {2 : 61, 4 : 62},#25
        {2 : 63, 3 : (2,(64,65))},#26
        {3 : 66, 4 : 67},#27
        {2 : 68, 3 : 69, 4 : 70},#28
        {3 : 71, 4 : 72},#29
        {4 : 73}#30
    ]

    def __init__(self, graph, k):
        self.patterns_tab = []
        self.positions_tab = []
        self._graph = graph
        self._k = k

    def create_list_neighbors(self):
        for v in self._graph.vs:
            v['list_neighbors'] = []
        for e in self._graph.es:
            if not e.source in self._graph.vs[e.target]['list_neighbors']:
                self._graph.vs[e.target]['list_neighbors'].append(e.source)
            if not e.target in self._graph.vs[e.source]['list_neighbors']:
                self._graph.vs[e.source]['list_neighbors'].append(e.target)
        for v in self._graph.vs:
            v['list_neighbors'].sort(reverse = True)

    def degree_distribution(self, graph_sub):
        result = []
        for v in graph_sub.vs:
            result.append(v.degree())
            v['d'] = result[v.index]
        result.sort()
        return result

    def disambiguate_pattern(self, graph_sub, new_pattern):
        for v in graph_sub.vs:
            if v['d'] == new_pattern[0]:
                for n in v.neighbors():
                    if n['d'] == new_pattern[1]:
                        return new_pattern[2][0]
        return new_pattern[2][1]

    def disambiguate_position(self, graph_sub, v, new_position):
        for n in v.neighbors():
            if n['d'] == new_position[0]:
                return new_position[1][0]
        return new_position[1][1]

    def index_pattern(self, graph_sub):
        new_pattern = self.DICT_PATTERNS[str(self.degree_distribution(graph_sub))]
        if type(new_pattern) != int :
            new_pattern = self.disambiguate_pattern(graph_sub, new_pattern)
        self.patterns_tab[new_pattern - 1] += 1
        new_positions = self.DICT_POSITIONS[new_pattern - 1]
        if new_pattern in [10, 12, 13, 17, 18, 21, 26] :
            for v in graph_sub.vs:
                new_position = new_positions[v['d']]
                if type(new_position) != int:
                    new_position = self.disambiguate_position(graph_sub, v, new_positions[v['d']])
                self.positions_tab[v['id_principal']][new_position - 1] += 1
        else:
            for v in graph_sub.vs:
                self.positions_tab[v['id_principal']][new_positions[v['d']] - 1] += 1

    def in_neighborhood_vsub(self, list_neighbors, length_vsub):
        for n in list_neighbors:
            if self._graph.vs[n]['id_sub'] != -1 and self._graph.vs[n]['id_sub'] != length_vsub-1:
                return True
        return False

    def add_vertex(self, graph_sub, vertex):
        vertex['id_sub'] = len(graph_sub.vs)
        graph_sub.add_vertex(name = vertex['name'], **{'id_principal' : vertex.index})

    def extend_subgraph(self, graph_sub, v, vext):
        if len(graph_sub.es) > 0 :
            self.index_pattern(graph_sub)
        if len(graph_sub.vs) == self._k:
            return
        while vext:
            w = vext.pop()
            vext2 = list(vext)
            self.add_vertex(graph_sub, w)
            for nei in w['list_neighbors']:
                u = self._graph.vs[nei]
                if u.index >= v.index:
                    if u['id_sub'] == -1 :
                        if not self.in_neighborhood_vsub(u['list_neighbors'], len(graph_sub.vs)):
                            vext2.append(u)
                    else:
                        graph_sub.add_edge(len(graph_sub.vs) - 1, u['id_sub'])
                else:
                    break

            self.extend_subgraph(graph_sub, v, vext2)
            graph_sub.delete_vertices(w['id_sub'])
            w['id_sub'] = -1

    def characterize_with_patterns(self):
        self.create_list_neighbors()
        self.patterns_tab = 30*[0]
        for v in self._graph.vs:
            self.positions_tab.append(73*[0])
            v['id_sub'] = -1
        for v in self._graph.vs:

            graph_sub = Graph.Formula()
            v['id_sub'] = 0
            if not 'name' in v.attributes():
                v['name'] = str(v.index)
            graph_sub.add_vertex(name = v['name'], **{'id_principal' : v.index, 'evol_class' : 1, 'pattern_sub' : 0})

            vext = []
            for nei in v['list_neighbors']:
                if nei > v.index:
                    vext.append(self._graph.vs[nei])

            if len(vext) > 0:
                self.extend_subgraph(graph_sub, v, vext)
            v['id_sub'] = -1
        return (self.patterns_tab, self.positions_tab)

class ClassicIndicators(object):
    def __init__(self, graph):
        self.clusters_list = graph.community_multilevel()
        _cc_list = graph.decompose()
        self.max_cc = None
        for cc in _cc_list:
            if not self.max_cc or len(cc.vs) > len(self.max_cc.vs):
                self.max_cc = cc
        if self.max_cc:
            self.clusters_list_max_cc = self.max_cc.community_multilevel()
        self.graph = graph

    def bfs(self, start, stop_list = None):
        start['color'] = 'gray'
        start['distance'] = 0
        vertQueue = deque()
        vertQueue.append(start)
        while len(vertQueue) > 0:
            v = vertQueue.popleft()
            for nbr in v.neighbors():
                if not nbr['color']:
                    if stop_list and nbr.index in [u.index for u in stop_list]:
                        temp = v['distance'] + 1
                        del self.graph.vs['distance']
                        del self.graph.vs['color']
                        return temp
                    nbr['color'] = 'gray'
                    nbr['distance'] = v['distance'] + 1
                    vertQueue.append(nbr)
        del self.graph.vs['distance']
        del self.graph.vs['color']


    def diameter(self):
        print 'graph_utils.diameter'
        print self.graph.diameter(directed = False)
        return self.graph.diameter(directed = False)

    def nb_louvain_com(self, size_min = 1):
        return len([cluster for cluster in self.clusters_list if len(cluster) >= size_min])

    def modularity(self):
        return round(self.graph.modularity(self.clusters_list),5)

    def size_max_cc(self):
        if not self.max_cc:
            return 0
        return len(self.max_cc.vs)
    
    def nb_cluster_sup_2(self):
        nb = 0
        for cluster in self.clusters_list:
            if len(cluster) >= 2:
                nb += 1
        return nb

    def clustering_coeff(self):
        return round(self.graph.transitivity_undirected(),5)

    def density(self):
        return round(self.graph.density(),5)

    def freeman_betweenness(self):
        if len(self.graph.vs) == 0:
            return 'undetermined'
        btw_list = self.graph.betweenness()
        n = len(self.graph.vs)
        rbtw_list = [btw/(n**2-2*n+3) for btw in btw_list]
        max_rbtw = max(rbtw_list)
        sum_rbtw = sum([(max_rbtw - rbtw) for rbtw in rbtw_list])
        return 2*round(sum_rbtw/(n-1),5) if (n-1) != 0 else 'undetermined'

    def nb_isolated_vertices(self):
        return len([v for v in self.graph.vs if v.degree() == 0])

    def prop_non_isolated_vertices(self):
        return round((len(self.graph.vs) - self.nb_isolated_vertices())/len(self.graph.vs), 5) if len(self.graph.vs) else 'undetermined'

    def nb_connected_components(self):
        return len(self.graph.decompose(minelements=2))