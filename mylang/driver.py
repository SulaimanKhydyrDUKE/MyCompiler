"""Command-line driver: run a MyLang program, or emit it as Python.

    python -m mylang.driver Examples/matrix.ml
    python -m mylang.driver Examples/matrix.ml --emit out.py
"""

import argparse
import sys

from mylang.lexer import Lexer
from mylang.parser import Parser
from mylang.typecheck import TypeChecker
from mylang.interpreter import Interpreter
from mylang.codegen import generate_python

DEFAULT_SOURCE = """
let a = 10;
let b = 20;
let c = a + b * 2;
print("C is:");
print(c);
if (c == 50) {
    print("Success: c is 50");
} else {
    print("Failure: c is not 50");
}

let m = [[1, 2], [3, 4]];
print("Matrix m:");
print(m);
let t = m.Transpose();
print("Transposed m:");
print(t);

let inv = m.isInvertible();
print("Is m invertible?");
print(inv);
"""


def front_end(source):
    """Lex, parse and type-check; returns the checked Program."""
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    TypeChecker().check(program)
    return program


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m mylang.driver", description="Run a MyLang program.")
    parser.add_argument("file", nargs="?", help="MyLang source file (default: a built-in demo program)")
    parser.add_argument("--emit", metavar="OUT.py", help="write the program as Python source instead of running it")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, "r") as handle:
            source = handle.read()
    else:
        source = DEFAULT_SOURCE

    try:
        program = front_end(source)
        if args.emit:
            with open(args.emit, "w") as handle:
                handle.write(generate_python(program))
            return 0
        Interpreter().interpret(program)
        return 0
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
