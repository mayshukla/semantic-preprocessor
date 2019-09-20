#!/usr/bin/env python3

import argparse


class MacroNode():
    def __init__(self, value=None):
        self.value = value
        self.children = {}

    def __hash__(self):
        return self.value.__hash__()

    def __str__(self):
        return self._stringify_indented()

    def _stringify_indented(self, indent_level=0):
        indent = " " * (4 * indent_level)
        string = "\n" + indent + "{value: " + str(self.value)
        string += " children: ["
        for key, value in self.children.items():
            string += "\n  " + indent + "{}: {}, ".format(
                key, value._stringify_indented(indent_level + 1))
        string += "]}"
        return string

    def insert(self, macro_name, value=None):
        new_node = MacroNode(value)
        self.children[macro_name] = new_node
        return new_node

    def find_child(self, macro_name):
        return self.children[macro_name]

    def find_value(self, macro_name):
        return self.find_child(macro_name).value

    def set_value(self, value):
        self.value = value


class MacroTree():
    def __init__(self):
        self.top_level_map = MacroNode()

    def __str__(self):
        return str(self.top_level_map)

    def insert(self, qual_macro_name, value):
        """
        Inserts a fully qualified macro name into the macro tree. (e.g. "1.2.3")
        Will create necessary intermediate nodes if they don't exist
        """

        # Split up qualified macro name by level
        macro_path = qual_macro_name.split(".")

        current_macro_node = self.top_level_map
        for i in range(len(macro_path)):
            if macro_path[i] not in current_macro_node.children:
                # Create new node if one doesn't exist
                new_macro_node = current_macro_node.insert(macro_path[i])
                current_macro_node = new_macro_node
            else:
                # If a node exists
                current_macro_node = current_macro_node.find_child(
                    macro_path[i])

            # When we are done traversing the macro tree, insert the value
            if i == len(macro_path) - 1:
                current_macro_node.set_value(value)


def parse_macro_file(filename):
    """
    Parses macro file and returns tree of macros
    """
    macros = MacroTree()
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


if __name__ == "__main__":
    main()
