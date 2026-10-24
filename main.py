import sys

from antlr4 import CommonTokenStream, FileStream
from antlr4.error.ErrorListener import ErrorListener

from oosLexer import oosLexer
from oosParser import oosParser


class CompilerErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.error_count = 0

    def syntaxError(
        self, recognizer, offendingSymbol, line, column, msg, e
    ):
        self.error_count += 1
        print(
            f"Error at line {line}, column {column + 1}: {msg}",
            file=sys.stderr,
        )


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <source.oos>", file=sys.stderr)
        return 1

    try:
        source = FileStream(sys.argv[1], encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"Cannot read source file: {error}", file=sys.stderr)
        return 1

    errors = CompilerErrorListener()

    lexer = oosLexer(source)
    lexer.removeErrorListeners()
    lexer.addErrorListener(errors)

    tokens = CommonTokenStream(lexer)

    parser = oosParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(errors)

    parser.startRule()

    if errors.error_count > 0:
        print(f"Analysis failed: {errors.error_count} error(s).")
        return 1

    print("Syntax analysis completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())