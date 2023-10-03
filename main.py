'''Python program to "parse" java files'''


import re

# Define a regular expression pattern to match Java method declarations
method_pattern = re.compile(r'\s*(public|private|protected|static)?\s*[\w<>,]+\s+(\w+)\s*\([^)]*\)\s*{')
if_pattern = re.compile(r'^\s*if\s*\(.+\)\s*\{?$')
else_if_pattern = re.compile(r'^\s*else\s*if\s*\(.+\)\s*\{?$')
else_pattern = re.compile(r'^\s*else\s*\{?$')
for_pattern = re.compile(r'for *\(.*;.*;.*\)')
while_pattern = re.compile(r'while *\(.*\)')

def is_decision_or_loop_structure(line):
    # Remove leading and trailing whitespaces
    line = line.strip()

    decision_and_loop_patterns = [
        if_pattern,
        else_if_pattern,
        else_pattern,
        for_pattern,
        # while_pattern
    ]

    # Regular expressions to match common decision structures
    # Check if the line matches any of the patterns
    for pattern in decision_and_loop_patterns:
        if pattern.match(line):
            return True

    return False


# Function to check if a line contains a method declaration
def is_method_declaration(line):
    return method_pattern.match(line)

def get_indent_count(line):
    return len(line) - len(line.lstrip())

def is_line_a_comment(stripped_line):
    return stripped_line.startswith("//")

class JavaParser:
    def __init__(self):
        # self.inside_method = False
        # self.method_depth = 0
        self.method_missing_starting_brace = False
        self.method_indent_count = 0
        self.output_file = None
        self.brace_stack = []

    def check_line(self, line):
        stripped_line = line.strip()
        # if is_line_a_comment(stripped_line):
            # return ""
            # return line

        if stripped_line == "":
            return line

        if self.method_missing_starting_brace and not stripped_line.startswith("{"):
            line = (" " * self.method_indent_count) + "// 1 MISSING '{' BRACE WAS ADDED HERE \n" + (" " * self.method_indent_count) + "{\n" + line

        self.method_missing_starting_brace = False

        if get_indent_count(line) < self.method_indent_count and not stripped_line.startswith("}"):
            indent_count = self.method_indent_count if self.method_indent_count < get_indent_count(line) else get_indent_count(line)
            line = (" " * indent_count) + "// 2 MISSING '}' BRACE WAS ADDED HERE \n" + (" " * (indent_count + 4)) + "}\n" + line
            self.method_indent_count = get_indent_count(line)

        if is_decision_or_loop_structure(line):
            self.inside_method = True
            self.method_indent_count = get_indent_count(line)
            self.method_depth = self.method_depth + 1

            # Check to see if there is a brace at the end of the line
            last_char = stripped_line[-1]
            if last_char != "{":
                self.method_missing_starting_brace = True

        return line

    def check_structure_by_line(self, file_lines):
        count = 0
        for line in file_lines:
            count += 1
            updated_line = self.check_line(line)
            output_file.write(updated_line)

    def start(self):
        self.output_file = open('output.java', 'w')
        lines = read_file('sample.java')
        self.check_structure_by_line(lines)
        self.output_file.close()


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    return lines


if __name__ == '__main__':
    output_file = open('output.java', 'w')

    parser = JavaParser()
    parser.start()
