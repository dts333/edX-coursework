#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 11:07:16 2020

@author: DannySwift
"""

import resource
import sys
import time

from heapq import heappush, heappop


class Node:
    def __init__(self, board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0
        self.f = self.depth
        for x in self.board:
            if x == 0:
                continue
            i = self.board.index(x)
            i -= x
            i = abs(i)
            self.f += i // 3
            self.f += i % 3

def get_children(node):
    board = node.board
    children = []
    zero = board.index(0)
    if zero > 2:
        child = board.copy()
        child[zero], child[zero - 3] = child[zero - 3], 0
        children.append(Node(child, node, 'Up'))
    if zero < 6:
        child = board.copy()
        child[zero], child[zero + 3] = child[zero + 3], 0
        children.append(Node(child, node, 'Down'))
    if zero in [1, 2, 4, 5, 7, 8]:
        child = board.copy()
        child[zero], child[zero - 1] = child[zero - 1], 0
        children.append(Node(child, node, 'Left'))
    if zero in [0, 1, 3, 4, 6, 7]:
        child = board.copy()
        child[zero], child[zero + 1] = child[zero + 1], 0
        children.append(Node(child, node, 'Right'))
    
    return children
        

def solve(method, board):
    goal = [0,1,2,3,4,5,6,7,8]
    root = Node(board)
    if method == 'ast':
        frontier = [(root.f, 0, root)]
    else:
        frontier = [root]
    explored = []
    path = []
    current = root
    nodes_expanded = 0
    max_depth = 0
    max_mem = 0
    start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    while current.board != goal:
        try:
            if method == 'bfs':
                current = frontier.pop(0)
            elif method == 'dfs':
                current = frontier.pop()
            elif method == 'ast':
                current = heappop(frontier)[2]
        except IndexError:
            return 'FAILIURE'
        explored.append(current.board)
        nodes_expanded += 1
        if current.depth > max_depth:
            max_depth += 1
        i=0
        for child in get_children(current):
            i += 1
            if child.board not in explored:
                if method in ['bfs', 'dfs']:
                    frontier.append(child)
                elif method == 'ast':
                    heappush(frontier, (child.f, 4 * nodes_expanded + i, child))
        mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
        if mem > max_mem:
            max_mem = mem
        
    path.append(current.move)
    while current.parent:
        path.append(current.parent.move)
        current = current.parent
    depth = len(path)-1
    path = [path[-i] for i in range(depth)]
        
    return path, depth, nodes_expanded, max_depth, max_mem



if __name__ == '__main__':
    t = time.time()
    method = sys.argv[1]
    board = [int(x) for x in sys.argv[2].split(',')]
    
    output = solve(method, board)
    
    with open('output.txt', 'w')as f:
        f.write(
                f"path_to_goal: {output[0]}\n\
                cost_of_path: {output[1]}\n\
                nodes_expanded: {output[2]}\n\
                search_depth: {output[1]}\n\
                max_search_depth: {output[3]}\n\
                running_time: {time.time() - t}\n\
                max_ram_usage: {output[4]}"
                )
    
        
