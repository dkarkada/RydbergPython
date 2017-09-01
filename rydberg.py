# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 00:05:49 2017

@author: Dhruva
"""


def execute(inp):
    parsed_inp_1 = inp.split(";")
    


inp = ""
while inp != "close":
    inp = raw_input(">>")
    execute(inp)