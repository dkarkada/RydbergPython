# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 00:05:49 2017

@author: Dhruva
"""
import re
import lattice_data


def create(params, data):
    if len(params) == 1:
        if (isinstance(params[0], int)):
            if (0 < params[0] <= 200):
                data.create_lattice(params[0])
            else:
                raise TypeError("One or more params out of acceptable range.")
        else:
            raise TypeError("One or more params is of wrong type.")
    else:
        raise TypeError("Does not take %i params." % len(params))


def add_seed(params, data):
    if data.lattice is not None:
        if len(params) == 2:
            if (isinstance(params[0], int) and isinstance(params[1], int)):
                data.add_seed(params[0], params[1])
            else:
                raise TypeError("One or more params is of wrong type.")
        else:
            raise TypeError("Does not take %i params." % len(params))
    else:
        raise ValueError("Lattice not initialized. Use \"create\" command.")


def evolve(params, data):
    if data.lattice is not None:
        if len(params) == 3:
            if (isinstance(params[0], float) and
                    isinstance(params[1], float) and
                    isinstance(params[2], float)):
                if (0 <= params[0] <= 1 and 0 <= params[1] <= 1 and
                        0 <= params[2] <= 1):
                    data.generate_changes(params[0], params[1], params[2])
                else:
                    raise TypeError("One or more params out of acceptable "
                                    "range.")
            else:
                raise TypeError("One or more params is of wrong type.")
        elif len(params) == 2:
            if (isinstance(params[0], float) and isinstance(params[1], float)):
                if (0 < params[0] <= 1 and 0 <= params[1] <= 1):
                    data.generate_changes(params[0], params[0], params[1])
                else:
                    raise TypeError("One or more params out of acceptable "
                                    "range.")
            else:
                raise TypeError("One or more params is of wrong type.")
        else:
            raise TypeError("Does not take %i params." % len(params))
    else:
        raise ValueError("Lattice not initialized. Use \"create\" command.")


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

# This has all the data!!!!
data = lattice_data.LatticeData()
inp_history = []
command_history = []
# Maps user string input to the appropriate function to run.
command_dict = {"create": create,
                "addseed": add_seed,
                "add_seed": add_seed,
                "evolve": evolve}
exit = False
while (not exit):
    inp_history.append(input(">>"))
    new_commands = []
    # If line is unparsable, execute nothing.
    try:
        new_commands = translate_input(inp_history)
    except SyntaxError as e:
        print(e.message)
        print("Did not execute.")
    # If line is parsed, try to execute each command. Log each successful.
    for command_attempt in new_commands:
        try:
            if command_attempt[0] == "exit":
                exit = True
            else:
                command_dict[command_attempt[0]](command_attempt[1], data)
                command_history.append(command_attempt)
        except KeyError:
            print("Command \"%s\" not found."
                  % command_attempt[0])
        except TypeError as e:
            print("Command \"%s\": " % command_attempt[0] + e.message)
        except ValueError as e:
            print("Command \"%s\": " % command_attempt[0] + e.message)
