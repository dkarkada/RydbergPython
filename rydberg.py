# -*- coding: utf-8 -*-
"""
Created on Fri Sep 01 00:05:49 2017

@author: Dhruva
"""
import re


def generate(params):
    print(params)


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
            parsed_params = [s for s in parsed_params if s is not ""]
            commands.append([parsed_command[0], parsed_params])
        elif len(parsed_command) == 1:
            commands.append([parsed_command[0], []])
    return commands


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
                command_dict[command_attempt[0]](command_attempt[1])
                command_history.append(command_attempt)
        except KeyError:
            print("Command \"%s\" not found. Skipped over."
                  % command_attempt[0])
        except TypeError:
            # shit about wrong number of params
        except SomeOtherError:
            # cant run xyz method yet

