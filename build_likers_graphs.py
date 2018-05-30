#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 14:19:57 2018

@author: raphael
"""

from os.path import isfile, expanduser
from os import listdir
from igraph import Graph
import gzip
import json

def open_json(ego):
    path = expanduser('~/data/three/%s/statuses.jsons' %(ego))

    if isfile(path):
        f = open(path, 'rb')
    else:
        gz = path+".gz"
        f = gzip.open(gz, 'rb')
    return f

def get_list_of_friends(ego):
    path = expanduser('~/GALLERY/three/%s/Graphs/correspondence_table' % ego)
    result = []
    with open(path, 'r') as f:
        for line in f:
            result.append(line[0:len(line)-1].decode('utf-8'))
    return result

def check_likers(ego):
    f = open_json(ego)
    result = {}
    friends = get_list_of_friends(ego)
    for line in f:
        jr = json.loads(line)
        likes = jr.get('likes', [])
        for like in likes:
            liker = like['id']
            if not liker in friends:
                continue
            if not liker in result:
                result[liker] = set()
            for like_2 in likes:
                liker_2 = like_2['id']
                if liker_2 in friends and liker_2 != liker:
                    result[liker].add(liker_2)
    f.close()
    return {friend:list(result[friend]) for friend in result}

def create_likers_graph(ego):
    graph = Graph.Full(0)
    name_to_id = []

    colikers = check_likers(ego)

    for friend in colikers:
        name_to_id.append(friend)
        graph.add_vertex(name = friend)

    for liker in colikers:
        mutual_likers = colikers[liker]
        liker_id = name_to_id.index(liker)
        for mutual_liker in mutual_likers:
            mutual_id = name_to_id.index(mutual_liker)
            if mutual_id > liker_id:
                    continue
                
            print liker_id, mutual_id
            graph.add_edge(liker_id, mutual_id)


    graph.write(expanduser('../Graphs_likers/%s.gml' % ego), format = 'gml')
    
for ego in listdir(expanduser('~/data/three')):
    create_likers_graph(ego)
    break