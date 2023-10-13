"""
Python program to "parse" java files
Team Cosmic Carousel
This program assumes that the file being read has correct indentation in order to determine where a missing brace is
When executed, it pulls in a file and reads it line by line
If one of the decision/loop/method regex patterns is detected in a line, it will start to check for braces
If a brace is exists, it will push the indent count of that line onto the stack
If a brace is missing, it will add the brace and push the indent count onto that line of the stack
"""

import re

# Define a regular expression pattern to match Java method declarations
method_pattern = re.compile(r'^(?:(?:public|private|protected|static|final|native|synchronized|abstract|transient)+\s+)+[$_\w<>\[\]\s]*\s+[\$_\w]+\([^\)]*\)?\s*\{?[^\}]*\}?$')
public_method_pattern = re.compile(r'^.*(?:(?:public)\s+).*$')
if_pattern = re.compile(r'^\s*if\s*\(.+\)\s*\{?$')
else_if_pattern = re.compile(r'^\s*else\s*if\s*\(.+\)\s*\{?$')
else_pattern = re.compile(r'^\s*else\s*\{?$')
for_pattern = re.compile(r'^\s*for*\(.*;.*;.*\).*$')
switch_pattern = re.compile(r'^\s*switch *\(.*\).*$')
while_pattern = re.compile(r'^\s*while *\(.*\)')
do_pattern = re.compile(r'^\s*do.*$')


def is_decision_or_loop_or_method(line):
    # Remove leading and trailing whitespaces
    line = line.strip()

    decision_and_loop_patterns = [
        if_pattern,
        else_if_pattern,
        else_pattern,
        for_pattern,
        method_pattern,
        switch_pattern,
        while_pattern,
        do_pattern,
    ]

    # Regular expressions to match common decision structures
    # Check if the line matches any of the patterns
    for pattern in decision_and_loop_patterns:
        if pattern.match(line):
            return True

    return False


def is_method_declaration(line):
    return method_pattern.match(line)


def is_public_method_declaration(line):
    return public_method_pattern.match(line)


def get_indent_count(line):
    return len(line) - len(line.lstrip())


def is_line_start_of_javadoc_comment(stripped_line):
    return stripped_line.startswith("/*")


def is_line_end_of_javadoc_comment(stripped_line):
    return stripped_line.endswith("*/")


class JavaParser:
    def __init__(self):
        self.is_inside_javadoc_comment = False
        self.method_missing_starting_brace = False
        self.method_indent_count = 0
        self.output_file = None
        self.public_method_count = 0
        self.is_first_line_of_method = False
        # The stack just stores an array of indent counts
        # When you reach a spot where you need a closing brace, you just pop the number and use it for the indent count
        self.brace_indent_stack = []

    def check_line(self, line):
        stripped_line = line.strip()

        if is_public_method_declaration(line):
            self.public_method_count = self.public_method_count + 1

        if self.is_inside_javadoc_comment:
            if is_line_end_of_javadoc_comment(stripped_line):
                self.is_inside_javadoc_comment = False
            return line

        if is_line_start_of_javadoc_comment(stripped_line) and not is_line_end_of_javadoc_comment(stripped_line):
            self.is_inside_javadoc_comment = True
            return line

        if stripped_line == "":
            return line

        if self.method_missing_starting_brace and not stripped_line.startswith("{"):
            line = (" " * self.method_indent_count) + "// ***** MISSING '{' BRACE WAS ADDED HERE \n" + (" " * self.method_indent_count) + "{\n" + line
            self.brace_indent_stack.append(self.method_indent_count)
        elif stripped_line.startswith("{"):
            self.brace_indent_stack.append(get_indent_count(line))

        self.method_missing_starting_brace = False

        if get_indent_count(line) < self.method_indent_count and not stripped_line.startswith("}"):
            indent_count = self.brace_indent_stack.pop()
            line = (" " * indent_count) + "// ***** MISSING '}' BRACE WAS ADDED HERE \n" + (" " * indent_count) + "}\n" + line
            self.method_indent_count = get_indent_count(line)
        elif stripped_line.startswith("}"):
            self.brace_indent_stack.pop()
            self.method_indent_count = get_indent_count(line)

        if self.is_first_line_of_method and not stripped_line.startswith("//") and not self.is_inside_javadoc_comment:
            self.is_first_line_of_method = False
            self.method_indent_count = get_indent_count(line)

        if is_decision_or_loop_or_method(line):
            self.method_indent_count = get_indent_count(line)
            self.is_first_line_of_method = True

            # Check to see if there is a brace at the end of the line
            last_char = stripped_line[-1]
            if last_char != "{":
                self.method_missing_starting_brace = True

        return line

    def check_structure_by_line(self, file_lines):
        for line in file_lines:
            updated_line = self.check_line(line)
            self.output_file.write(updated_line)

    def start(self):
        self.output_file = open('output.txt', 'w')

        # Change this to the path of the file you want to read
        lines = read_file('sample.java')
        self.output_file.write(f"**********ORIGINAL TEXT:********** \n\n")
        for line in lines:
            self.output_file.write(line)
        self.output_file.write(f"\n\n **********CORRECTED TEXT:********** \n\n")
        self.check_structure_by_line(lines)

        self.output_file.write(f"\n\n Public method count: {self.public_method_count}")
        print(f"Public method count: {self.public_method_count}")

        self.output_file.close()


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    return lines


if __name__ == '__main__':

    java_parser = JavaParser()
    java_parser.start()
