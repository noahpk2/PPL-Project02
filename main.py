import antlr4
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from JavaParserListener import JavaParserListener


class JavaCodeModifier(JavaParserListener):

    def __init__(self):
        self.changes = []
        self.public_count = 0

    def enterModifier(self, ctx: JavaParser.ModifierContext):
        if ctx.getText() == "public":
            self.public_count += 1

    def enterStatement(self, ctx: JavaParser.StatementContext):
        if (ctx.IF() or ctx.FOR() or ctx.WHILE() or ctx.DO()) and not ctx.block():
            position_to_add_brace = ctx.stop.tokenIndex + \
                1  # After the last token of this context
            self.changes.append((position_to_add_brace, " {"))

    def exitStatement(self, ctx: JavaParser.StatementContext):
        if ctx.IF() or ctx.FOR() or ctx.WHILE() or ctx.DO():
            if not ctx.block():
                position_to_add_closing_brace = ctx.stop.tokenIndex + \
                    1  # After the last token of this context
                self.changes.append((position_to_add_closing_brace, "}"))

def apply_changes(original_code, changes):
        offset = 0
        for position, change in changes:
            original_code = original_code[:position + offset] + \
                change + original_code[position + offset:]
            offset += len(change)
        return original_code


def process_java_code(input_code):
        # Create lexer and parser
        input_stream = antlr4.InputStream(input_code)
        lexer = JavaLexer(input_stream)
        token_stream = antlr4.CommonTokenStream(lexer)
        parser = JavaParser(token_stream)

        # Create custom listener and connect with parser
        code_modifier = JavaCodeModifier()
        walker = antlr4.ParseTreeWalker()
        tree = parser.compilationUnit()
        walker.walk(code_modifier, tree)

        # Apply changes to the original code
        modified_code = apply_changes(input_code, code_modifier.changes)
        return modified_code, code_modifier.public_count


# Test the function
input_code = open("Test.java", "r").read()


modified_code, public_count = process_java_code(input_code)
# output modified code

open("Test_modified.java", "w").write(modified_code)

print(f"'public' keyword count: {public_count}")
