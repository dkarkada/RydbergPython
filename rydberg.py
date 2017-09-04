# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 00:05:49 2017

@author: Dhruva
"""
import re
import lattice_data


def generate(params, data):
    if len(params) == 3:
        if (isinstance(params[0], int) and isinstance(params[1], float) and
                isinstance(params[2], float)):
            if (0 < params[0] <= 400 and 0 <= params[1] <= 1 and
                    0 <= params[2] <= 1):
                data.create_lattice(params[0])
                data.generate_changes(params[1], params[2])
            else:
                raise TypeError("One or more params out of acceptable range.")
        else:
            raise TypeError("One or more params is of wrong type.")
    else:
        raise TypeError("Does not take %i params." % len(params))
    # cant run xyz method yet


def translate_input(inp_history):
    commands = []
    last_inp = str.lower(inp_history[-1])
    parsed_input = [s.strip() for s in last_inp.split(";")]
    for command in parsed_input:
        parsed_command = [s.strip() for s in re.split("[\[\]]", command)]
        parsed_command = [s for s in parsed_command if s is not ""]
        if len(parsed_command) > 2:
            raise SyntaxError("Invalid syntax. Command should terminate after "
                              "parameter list.")
        elif len(parsed_command) == 2:
            parsed_params = [s.strip() for s in re.split("[, ]",
                             parsed_command[1])]
            parsed_params = [numerify(s) for s in parsed_params if s is not ""]
            commands.append([parsed_command[0], parsed_params])
        elif len(parsed_command) == 1:
            commands.append([parsed_command[0], []])
    return commands


def numerify(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s

data = lattice_data.LatticeData()
inp_history = []
command_history = []
command_dict = {"generate": generate}
exit = False
temp = 0
while (not exit) and temp < 5:
    temp += 1
    inp_history.append(raw_input(">>"))
    new_commands = []
    try:
        new_commands = translate_input(inp_history)
    except SyntaxError as e:
        print(e.message)
        print("Did not execute.")
    for command_attempt in new_commands:
        try:
            if command_attempt[0] == "exit":
                exit = True
            else:
                command_dict[command_attempt[0]](command_attempt[1], data)
                command_history.append(command_attempt)
        except KeyError:
            print("Command \"%s\" not found. Skipped over."
                  % command_attempt[0])
        except TypeError as e:
            print("Command \"%s\": " % command_attempt[0] + e.message)
