'''Python program to "parse" java files'''


import re

# Define a regular expression pattern to match Java method declarations
method_pattern = re.compile(r'(?:(?:public|private|protected|static|final|native|synchronized|abstract|transient)+\s+)+[$_\w<>\[\]\s]*\s+[\$_\w]+\([^\)]*\)?\s*\{?[^\}]*\}?')
if_pattern = re.compile(r'^\s*if\s*\(.+\)\s*\{?$')
else_if_pattern = re.compile(r'^\s*else\s*if\s*\(.+\)\s*\{?$')
else_pattern = re.compile(r'^\s*else\s*\{?$')
for_pattern = re.compile(r'for *\(.*;.*;.*\)')
while_pattern = re.compile(r'while *\(.*\)')

def is_decision_or_loop_or_method(line):
    # Remove leading and trailing whitespaces
    line = line.strip()

    decision_and_loop_patterns = [
        if_pattern,
        else_if_pattern,
        else_pattern,
        for_pattern,
        method_pattern,
        # Need to test while still and 'do while'
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
        # The stack just stores an array of indent counts
        # When you reach a spot where you need a closing brace, you just pop the number and use it for the indent count
        self.brace_indent_stack = []

    def check_line(self, line):
        stripped_line = line.strip()

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

        if is_decision_or_loop_or_method(line):
            self.method_indent_count = get_indent_count(line)

            # Check to see if there is a brace at the end of the line
            last_char = stripped_line[-1]
            if last_char != "{":
                self.method_missing_starting_brace = True

        return line

    def check_structure_by_line(self, file_lines):
        count = 0
        for line in file_lines:
            count += 1
            # Prints line count for easier debugging. We can remove this and count variable before submitting
            print(count)
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
