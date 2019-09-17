#!/usr/bin/env python3

import argparse


class MacroNode():
    def __init__(self, value=None):
        self.value = value
        self.children = {}

    def __hash__(self):
        return self.value.__hash__()

    def __str__(self):
        string = "{value: " + str(self.value)
        string += " children: ["
        for key, value in self.children.items():
            string += "{}: {}, ".format(key, value)
        string += "]}"
        return string

    def insert(self, macro_name, value):
        self.children[macro_name] = MacroNode(value)

    def find_child(self, macro_name):
        return self.children[macro_name]

    def find_value(self, macro_name):
        return self.find_child(macro_name).value


def parse_macro_file(filename):
    """
    Parses macro file and returns tree of macros
    """
    macros = MacroNode("")
    with open(filename, "r") as file:
        for line in file:
            # Skip empty lines
            if line == "\n":
                continue
            # Strip newline
            line = line[:-1]
            line = line.split(" ", 1)
            print(line)
            if len(line) > 1:
                macros.insert(line[0], line[1])
            else:
                macros.insert(line[0], "")
    return macros


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--macros",
                            help="File containing macro definitions",
                            required=True)
    arg_parser.add_argument("--filter",
                            help="Optional file specifying macros to include")
    arg_parser.add_argument("--template", help="Template file", required=True)
    args = arg_parser.parse_args()
    args = vars(args)

    macros = parse_macro_file(args["macros"])
    print(macros)
    print(macros.find_value("name"))


if __name__ == "__main__":
    main()
