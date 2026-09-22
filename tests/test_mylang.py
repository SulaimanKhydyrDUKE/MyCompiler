"""End-to-end and parser tests for MyLang. Run with `python -m pytest tests -q`."""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mylang import ast as A                      # noqa: E402
from mylang.interpreter import Interpreter       # noqa: E402
from mylang.lexer import Lexer                   # noqa: E402
from mylang.parser import ParseError, Parser     # noqa: E402
from mylang.typecheck import TypeChecker         # noqa: E402


def parse(source):
    return Parser(Lexer(source).tokenize()).parse()


def run(source, capsys):
    program = parse(source)
    TypeChecker().check(program)
    Interpreter().interpret(program)
    return capsys.readouterr().out.splitlines()


def test_example_program_runs_end_to_end():
    result = subprocess.run(
        [sys.executable, "-m", "mylang.driver", "Examples/matrix.ml"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == [
        "C is:", "50", "Success: c is 50",
        "Negated:", "-50",
        "Matrix m:", "[[1, 2], [3, 4]]",
        "Transposed m:", "[[1, 3], [2, 4]]",
        "Is m invertible?", "#t",
        "Does s have a null space?", "#t",
        "Reduced s:", "[[1.0, 2.0], [0.0, 0.0]]",
        "Hello, MyLang",
    ]


def test_multiplication_binds_tighter_than_addition():
    program = parse("let c = a + b * 2;")
    (let,) = program.statements
    assert isinstance(let, A.LetStatement) and let.name == "c"
    plus = let.expression
    assert isinstance(plus, A.BinaryExpression) and plus.operator == "+"
    assert isinstance(plus.left, A.Identifier) and plus.left.name == "a"
    assert isinstance(plus.right, A.BinaryExpression) and plus.right.operator == "*"


def test_member_calls_chain_left_to_right():
    program = parse("print(m.Transpose().Reduce());")
    (stmt,) = program.statements
    outer = stmt.expression
    assert isinstance(outer, A.MemberCallExpression) and outer.method == "Reduce"
    assert isinstance(outer.object, A.MemberCallExpression) and outer.object.method == "Transpose"
    assert isinstance(outer.object.object, A.Identifier)


def test_else_if_chains():
    program = parse("if (a == 1) { print(1); } else if (a == 2) { print(2); } else { print(3); }")
    (if_stmt,) = program.statements
    assert isinstance(if_stmt.else_branch, A.IfStatement)
    assert isinstance(if_stmt.else_branch.else_branch, A.Block)


def test_missing_semicolon_is_a_parse_error():
    with pytest.raises(ParseError, match="Expected ';'"):
        parse("let a = 1")


def test_ragged_matrix_is_a_parse_error():
    with pytest.raises(ParseError, match="same length"):
        parse("let m = [[1, 2], [3]];")


def test_assignment_is_rejected_because_values_are_immutable():
    program = parse("let a = 1; a = 2;")
    with pytest.raises(Exception, match="immutable"):
        TypeChecker().check(program)


def test_unary_minus_and_string_concatenation(capsys):
    assert run('print(-3); print("a" + "b");', capsys) == ["-3", "ab"]


def test_booleans_print_in_scheme_style(capsys):
    assert run("print(1 == 1); print(1 != 1);", capsys) == ["#t", "#f"]


def test_matrix_methods(capsys):
    out = run("let m = [[2, 0], [0, 2]]; print(m.isInvertible()); print(m.hasNull());", capsys)
    assert out == ["#t", "#f"]
