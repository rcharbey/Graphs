# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 10:15:01 2019

@author: raphael
"""

from graph_utils import Admin

class Communities(object):
    def __init__(self, indicators, graph):
        self.graph = Admin.import_graph(graph)
        self.compute_communities()
        indicators.communities = self
            
    def compute_communities(self):
        max_modularity, max_communities = -1, None
        for i in range(20):
            communities = self.graph.community_multilevel()
            mod = communities.modularity
            if mod > max_modularity:
                max_modularity = mod
                max_communities = communities
        temp_com = [c for c in max_communities]
        temp_com.sort(key = lambda x: len(x), reverse = True)
        self.communities = temp_com
        self._modularity = max_modularity 
        
    def modularity(self):
        return self._modularity
        
    def densities(self):
        result = []
        for c in self.communities:
            temp_graph = self.graph.subgraph(c)
            result.append(Indicators(temp_graph).density())
        return result
        
    def proportions(self):
        result = []
        for c in self.communities:
            temp_graph = self.graph.subgraph(c)
            result.append(Indicators(temp_graph).n() / float(Indicators(self.graph).n()))
        return result
        
    def nb_communities(self, size_min = 2):
        i = 0
        for community in self.communities:
            if len(community) >= size_min:
                i += 1
            else: 
                break
        return i        
    
def Journey(object):
    def __init__(self, graph):
        self.graph = Admin.import_graph(graph)
        
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
        

class Indicators(object):
    def __init__(self, graph):
        self.graph = Admin.import_graph(graph)
        self.connected_components = None
        self.max_cc = None
        self.connected_components = self.graph.decompose()
        
    @staticmethod
    def __list_indicators__():
        return [indic for indic in dir(Indicators) if not indic[0] == '_']
        
    def size_max_cc(self):
        max_cc = None
        for cc in self.connected_components:
            if not max_cc or len(cc.vs) > len(max_cc.vs):
                max_cc = cc
        max_cc = max_cc
        
        if not self.max_cc:
            return 0
        return len(self.max_cc.vs) / float(self.n())
        
    def n(self):
        return len(self.graph.vs())
        
    def m(self):
        return len(self.graph.es())

    def diameter(self):
        return self.graph.diameter(directed = False)

    def clustering_coeff(self):
        return round(self.graph.transitivity_undirected(),5)

    def density(self):
        return round(self.graph.density(),5)

    def freeman_betweenness(self):
        n = self.n()
        if n in [0,1]:
            return 'undetermined'
        
        btw_list = self.graph.betweenness()
        max_possible_btw = (n**2 -3*n + 2) / 2.0
        relative_btw_list = [btw/max_possible_btw for btw in btw_list]
        max_rbtw = max(relative_btw_list)
        sum_rbtw = sum([(max_rbtw - rbtw) for rbtw in relative_btw_list])
        return sum_rbtw/(n-1)

    def nb_isolated_vertices(self):
        return len([v for v in self.graph.vs if v.degree() == 0])

    def prop_non_isolated_vertices(self):
        return round((len(self.graph.vs) - self.nb_isolated_vertices())/len(self.graph.vs), 5) if len(self.graph.vs) else 'undetermined'

    def nb_connected_components(self):
        return len(self.graph.decompose(minelements=2))
            
    def nb_communities(self, size_min = 2):
        try :
            return self.communities.nb_communities(size_min)
        except:
            return Communities(self, self.graph).nb_communities(size_min) 

    def modularity(self):
        try :
            return self.communities.modularity()
        except:
            return Communities(self, self.graph).modularity()
        
    def com_densities(self):
        try :
            return self.communities.densities()
        except:
            return Communities(self, self.graph).densities()
            
    def com_proportions(self):
        try :
            return self.communities.proportions()
        except:
            return Communities(self, self.graph).proportions()
        