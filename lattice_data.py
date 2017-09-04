# -*- coding: utf-8 -*-
"""
Created on Sun Sep 03 16:30:16 2017

@author: Dhruva
"""
import numpy as np


class LatticeData:
    def __init__(self):
        self.lattice = None

    def create_lattice(self, size):
        self.lattice = np.zeros((size, size), dtype=np.int8)
        self.flip_on(0, 0)
    
    def generate_changes(self, p, g):
        print(self.lattice)
        
    def flip_on(self, x, y):
        rc = self.get_rc(x, y)
        self.lattice[rc[0], rc[1]] = 1
    
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
        
