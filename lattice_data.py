# -*- coding: utf-8 -*-
"""
Created on Sun Sep 03 16:30:16 2017

@author: Dhruva
"""
import numpy as np


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

    def add_seed(self, x, y):
        try:
            self.flip_on(x, y)
            # check if done, update self.done accordingly
            # following code only executed if not done
            self.consideration.add((x + 1, y))
            self.consideration.add((x, y + 1))
            self.consideration.add((x - 1, y))
            self.consideration.add((x, y - 1))
        except IndexError:
            print("Index/indices for command \"addSeed\" out of bounds. "
                  "Skipped over.")

    def generate_changes(self, px, py, g):
        if len(self.excited) == 0:
            self.add_seed(0, 0)
        print(self.lattice)

    def flip_on(self, x, y):
        rc = self.get_rc(x, y)
        self.lattice[rc[0], rc[1]] = 1
        self.excited.add((x, y))

    def get_rc(self, x, y):
        if self.lattice is not None:
            sz = self.lattice.shape[0]
            return sz//2 - y, x + sz//2
        else:
            return None

    def get_xy(self, r, c):
        if self.lattice is not None:
            sz = self.lattice.shape[0]
            return sz//2 - r, c - sz//2
        else:
            return None

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
