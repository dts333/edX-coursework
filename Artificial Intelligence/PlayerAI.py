#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:36:31 2020

@author: DannySwift
"""
import math
import sys
import time

from BaseAI import BaseAI


class PlayerAI(BaseAI):
    def __init__(self, depth=5):
        self.depth = depth
        sys.setrecursionlimit(sys.getrecursionlimit() * 2)

    def getMove(self, grid):
        self.time = time.clock()
        return self.alphabeta(grid.clone(), self.depth)[1]

    def get_max_children(self, grid):
        children = []
        moves = grid.getAvailableMoves()
        for move in moves:
            new = grid.clone()
            new.move(move)
            children.append((new, move))

        return children

    def get_min_children(self, grid):
        children = []
        cells = grid.getAvailableCells()
        for c in cells:
            new = grid.clone()
            new.setCellValue(c, 2)
            children.append(new)
            new = grid.clone()
            new.setCellValue(c, 4)
            children.append(new)

        return children

    def heuristic(self, grid):
        val = 0
        tile = 0
        mono = True
        map = grid.map
        for x in range(4):
            z = 0
            for y in range(4):
                cur = map[x][y]
                if cur < z:
                    mono = False
                z = cur
                if z == 0:
                    val += 1
                if x < 3:
                    if map[x + 1][y] == z:
                        val += 0.5
                    # if map[x+1][y] == z/2:
                    #    val += 0.1
                if y < 3:
                    if map[x][y + 1] == z:
                        val += 0.5
                    # if map[x][y+1] == z/2:
                    #    val += 0.1
                else:
                    tile = max(tile, z)
            if mono == True:
                val += 0.1
        val += tile
        return val

    def alphabeta(self, grid, depth, alpha=-math.inf, beta=math.inf, max_turn=True):
        if (time.clock() - self.time >= 0.19) or (not grid.canMove()):
            return self.heuristic(grid), 0
        if max_turn:
            val = -math.inf
            chosen_move = 0
            for child, move in self.get_max_children(grid):
                ival = val
                cval, _ = self.alphabeta(child, depth - 1, alpha, beta, False)
                val = max(val, cval)
                if ival != val:
                    chosen_move = move
                alpha = max(alpha, val)
                if alpha >= beta:
                    break
            return val, chosen_move
        else:
            val = math.inf
            for child in self.get_min_children(grid):
                cval, move = self.alphabeta(child, depth - 1, alpha, beta, True)
                val = min(val, cval)
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return val, move
