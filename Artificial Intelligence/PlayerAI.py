#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 15:36:31 2020

@author: DannySwift
"""
import math

from BaseAI import BaseAI


class Node:
    def __init__(self, grid):
        self.grid = grid

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
        return len(grid.getAvailableCells())

    def alphabeta(self, grid, depth, alpha=-math.inf, beta=math.inf, max_turn=True):
        if (depth == 0) or (not grid.canMove()):
            return self.heuristic(grid), 0
        if max_turn:
            val = -math.inf
            chosen_move = 0
            for child, move in self.get_max_children(grid):
                ival = val
                val = max(val, self.alphabeta(child, depth - 1, alpha, beta, False)[0])
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
