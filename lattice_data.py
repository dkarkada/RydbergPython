# -*- coding: utf-8 -*-
"""
Created on Sun Sep 03 16:30:16 2017

@author: Dhruva
"""
import numpy as np
import random as rnd


class LatticeData:
    def __init__(self):
        self.lattice = None
        self.consideration = None
        self.excited = None
        # equivalent to checking if further evolvable
        self.done = False

    def create_lattice(self, extent):
        size = 2*extent + 1
        self.lattice = np.zeros((size, size), dtype=np.int8)
        self.consideration = set()
        self.excited = set()
        self.done = False

    def add_seed(self, x, y):
        if self.lattice is not None:
            try:
                self.flip_on(x, y)
                if self.on_edge(x, y):
                    self.done = True
                else:
                    self.consider_neighbors((x, y))
            except IndexError:
                print("Index/indices for command \"addSeed\" out of bounds. "
                      "Skipped over.")
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

    def generate_changes(self, px, py, g):
        if self.lattice is not None:
            if len(self.excited) == 0:
                self.add_seed(0, 0)
            step = 0
            while step < 200 and not self.done:  # 2000 lol
                step += 1
                nextx = set()
                nexty = set()
                # consider REAL good here
                new_excited = set()
                for atom in self.excited:
                    if rnd.random < g:
                        self.flip_off(atom)
                        self.consider_neighbors(atom)
                        # is this^ necessary if i dont keep a perm next list?
                        # ie if not p then move back to consideration
                    else:
                        new_excited.add(atom)
                self.excited = new_excited
                for atom in nextx:
                    print()
                    # do shit
            print(self.lattice)
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

    def flip_on(self, x, y):
        if self.lattice is not None:
            rc = self.get_rc(x, y)
            self.lattice[rc[0], rc[1]] = 1
            self.excited.add((x, y))
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

    def flip_off(self, atom):
        if self.lattice is not None:
            x = atom[0]
            y = atom[1]
            rc = self.get_rc(x, y)
            self.lattice[rc[0], rc[1]] = 0
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

    def on_edge(self, x, y):
        if self.lattice is not None:
            extent = (self.lattice.shape[0] - 1) // 2
            return x == -extent or x == extent or y == -extent or y == extent
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

    def consider_neighbors(self, atom):
        x = atom[0]
        y = atom[1]
        self.consideration.add((x + 1, y))
        self.consideration.add((x, y + 1))
        self.consideration.add((x - 1, y))
        self.consideration.add((x, y - 1))

    def get_rc(self, x, y):
        if self.lattice is not None:
            sz = self.lattice.shape[0]
            return sz//2 - y, x + sz//2
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

    def get_xy(self, r, c):
        if self.lattice is not None:
            sz = self.lattice.shape[0]
            return sz//2 - r, c - sz//2
        else:
            raise ValueError("Lattice not initialized. Use \"create\" "
                             "command.")

"""
Implementation of nodes for a LinkedList which represent a coordinate
position on the lattice. LinkedList implementation useful for fast O(1)
removal. to_list function is a necessary O(n) cost in order to traverse
and remove (e.g. convert to list, traverse list, remove from linkedlist)
"""


class CoordinateNode:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None
        self.prev = None

    def set_next(self, node):
        self.next = node

    def set_prev(self, node):
        self.prev = node

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev


class CoordinateLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, x, y):
        node = CoordinateNode(x, y)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.set_next(node)
            node.set_prev(self.tail)
            self.tail = node

    def remove(self, node):
        if node is self.head and node is self.tail:
            self.head = None
            self.tail = None
        elif node is self.head:
            self.head = node.get_next()
            self.head.set_prev(None)
        elif node is self.tail:
            self.tail = node.get_prev()
            self.tail.set_next(None)
        else:
            node.get_prev.set_next(node.get_next())
            node.get_next.set_prev(node.get_prev())
        del node

    def to_list(self):
        result = []
        node = self.head
        while node is not None:
            result.append(node)
            node = node.get_next()
        return result
