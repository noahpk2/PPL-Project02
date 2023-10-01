'''Python program to "parse" java files'''


import re

# Define a regular expression pattern to match Java method declarations
method_pattern = re.compile(r'\s*(public|private|protected|static)?\s*[\w<>,]+\s+(\w+)\s*\([^)]*\)\s*{')

def is_decision_structure(line):
    # Remove leading and trailing whitespaces
    line = line.strip()

    # Regular expressions to match common decision structures
    if_pattern = re.compile(r'^\s*if\s*\(.+\)\s*\{?$')
    else_if_pattern = re.compile(r'^\s*else\s*if\s*\(.+\)\s*\{?$')
    else_pattern = re.compile(r'^\s*else\s*\{?$')

    # Check if the line matches any of the patterns
    if if_pattern.match(line) or else_if_pattern.match(line) or else_pattern.match(line):
        return True

    return False

# Function to check if a line contains a method declaration
def is_method_declaration(line):
    return method_pattern.match(line)


class JavaParser:
    def __init__(self):
        self.inside_method = False
        self.method_missing_starting_brace = False
        self.method_indent_count = 0
        self.output_file = None

    def check_line(self, line):
        stripped_line = line.strip()

        if self.method_missing_starting_brace and not stripped_line.startswith("{"):

            self.method_missing_starting_brace = False
            line = "// MISSING '{' BRACE WAS ADDED HERE \n" + (" " * self.method_indent_count) + "{\n" + line

        if self.inside_method and stripped_line.startswith("}"):
            self.inside_method = False

        if stripped_line.startswith("else") and self.inside_method:
            space_count = len(line) - len(line.lstrip())
            line = "// MISSING '}' BRACE WAS ADDED HERE \n" + (" " * space_count) + "}\n" + line

        if is_decision_structure(line):
            self.inside_method = True

            # Check to see if there is a brace at the end of the line
            last_char = stripped_line[-1]
            if last_char != "{":
                self.method_missing_starting_brace = True
                self.method_indent_count = len(line) - len(line.lstrip())

        return line

    def check_decision_structure(self, file_lines):
        count = 0
        for line in file_lines:
            count += 1
            updated_line = self.check_line(line)
            output_file.write(updated_line)

    def start(self):
        self.output_file = open('output.java', 'w')
        lines = read_file('sample.java')
        self.check_decision_structure(lines)
        self.output_file.close()


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    return lines


if __name__ == '__main__':
    output_file = open('output.java', 'w')

    parser = JavaParser()
    parser.start()
