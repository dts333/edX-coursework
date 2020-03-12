#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:36:31 2020

@author: DannySwift
"""
import math

from BaseAI import BaseAI


class Node:
    def __init__(self, grid, parent=None):
        self.grid = grid
        self.alpha = -math.inf
        self.beta = math.inf
        if parent:
            self.parent = parent
            self.depth = self.parent.depth + 1
            self.turn = -1 * self.parent.turn
        else:
            self.depth = 0
            self.turn = 1

    def get_children(self):
        if self.turn == 1:
            return self.get_max_children()
        return self.get_min_children()

    def get_max_children(self):
        children = []
        moves = self.grid.getAvailableMoves()
        for move in moves:
            new = self.grid.clone()
            new.move(move)
            children.append((new, move))

        return children

    def get_min_children(self):
        children = []
        cells = self.grid.getAvailableCells()
        for c in cells:
            new = self.grid.clone()
            new.setCellValue(c, 2)
            children.append(new)
            new = self.grid.clone()
            new.setCellValue(c, 4)
            children.append(new)

        return children


class PlayerAI(BaseAI):
    def __init__(self, depth=5):
        self.depth = depth

    def getMove(self, grid):
        return self.alphabeta(Node(grid.clone()), self.depth)[1]

    def heuristic(self, grid):
        return len(grid.getAvailableCells())

    def alphabeta(self, node, depth, alpha=-math.inf, beta=math.inf):
        if (depth == 0) or (not node.grid.canMove()):
            return self.heuristic(node.grid), 0
        if node.turn == 1:
            val = -math.inf
            chosen_move = 0
            for child, move in node.get_children():
                ival = val
                val = max(val, self.alphabeta(Node(child, parent=node), depth - 1, alpha, beta)[0])
                if ival != val:
                    chosen_move = move
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val, chosen_move
        else:
            val = math.inf
            for child in node.get_children():
                cval, move = self.alphabeta(Node(child, parent=node), depth - 1, alpha, beta)
                val = min(val, cval)
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val, move
