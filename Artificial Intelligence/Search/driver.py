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
        children.append(Node(child, node, "Up"))
    if zero < 6:
        child = board.copy()
        child[zero], child[zero + 3] = child[zero + 3], 0
        children.append(Node(child, node, "Down"))
    if zero in [1, 2, 4, 5, 7, 8]:
        child = board.copy()
        child[zero], child[zero - 1] = child[zero - 1], 0
        children.append(Node(child, node, "Left"))
    if zero in [0, 1, 3, 4, 6, 7]:
        child = board.copy()
        child[zero], child[zero + 1] = child[zero + 1], 0
        children.append(Node(child, node, "Right"))

    return children


def solve(method, board):
    t = time.time()
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    root = Node(board)
    if method == "ast":
        frontier = [(root.f, 0, 0, root)]
    else:
        frontier = [root]
    explored = [root.board]
    path = []
    current = root
    nodes_expanded = -1
    max_depth = 0
    max_mem = 0
    start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    while current.board != goal:
        if current.depth >= max_depth:
            max_depth += 1
        try:
            if method == "bfs":
                current = frontier.pop(0)
                for child in get_children(current):
                    if child.board not in explored:
                        frontier.append(child)
                        explored.append(child.board)
            elif method == "dfs":
                current = frontier.pop()
                children = get_children(current)
                children.reverse()
                for child in children:
                    if child.board not in explored:
                        frontier.append(child)
                        explored.append(child.board)
            elif method == "ast":
                current = heappop(frontier)[3]
                i = 0
                for child in get_children(current):
                    if child.board not in explored:
                        i += 1
                        heappush(frontier, (child.f, i, 4 * nodes_expanded, child))
                        explored.append(child.board)
        except IndexError:
            return "FAILURE"

        nodes_expanded += 1
        mem = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) - start_mem
        if mem > max_mem:
            max_mem = mem

    path.append(current.move)
    while current.parent:
        path.append(current.parent.move)
        current = current.parent
    depth = len(path) - 1
    path = [path[-2 - i] for i in range(depth)]

    s = f"path_to_goal: {path}\n"
    s += f"cost_of_path: {depth}\n"
    s += f"nodes_expanded: {nodes_expanded}\n"
    s += f"search_depth: {depth}\n"
    s += f"max_search_depth: {max_depth}\n"
    s += f"running_time: {time.time() - t}\n"
    s += f"max_ram_usage: {max_mem}"

    return s


if __name__ == "__main__":
    method = sys.argv[1]
    board = [int(x) for x in sys.argv[2].split(",")]

    output = solve(method, board)
    print(output)
    with open("output.txt", "w") as f:
        f.write(output)
