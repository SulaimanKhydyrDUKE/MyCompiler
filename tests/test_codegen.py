"""The Python backend must print exactly what the interpreter prints."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
# Generated programs import mylang.runtime, so they run with the repo on PYTHONPATH.
ENV = {**os.environ, "PYTHONPATH": str(ROOT)}

from mylang.codegen import CodegenError, generate_python   # noqa: E402
from mylang.driver import front_end                        # noqa: E402
from mylang.interpreter import Interpreter                 # noqa: E402

PROGRAMS = {
    "arithmetic": 'let a = 7; let b = 2; print(a / b); print(a - b * 3); print(-a); print("x" + "y");',
    "booleans": "print(1 == 1); print(1 != 1); if (2 == 2) { print(1); } else { print(0); }",
    "else_if": 'let a = 3; if (a == 1) { print("one"); } else if (a == 3) { print("three"); } else { print("other"); }',
    "matrix": "let m = [[1, 2], [3, 4]]; print(m); print(m.Transpose()); print(m.isInvertible()); print([[1, 2], [2, 4]].hasNull()); print([[2, 4], [1, 3]].Reduce());",
    "shadowing_is_forgotten_after_block": 'let a = 1; if (#t) { let a = 2; print(a); } print(a); { let a = 3; print(a); } print(a);',
    "nested_shadowing": "let a = 1; { let b = a + 1; { let a = b + 1; print(a); } print(b); } print(a);",
    "empty_block": "if (#t) { } print(9);",
}


def interpret(source, capsys):
    Interpreter().interpret(front_end(source))
    return capsys.readouterr().out


def run_generated(source, tmp_path):
    generated = tmp_path / "gen.py"
    generated.write_text(generate_python(front_end(source)))
    result = subprocess.run([sys.executable, str(generated)], cwd=ROOT, capture_output=True, text=True, env=ENV)
    assert result.returncode == 0, result.stderr
    return result.stdout


@pytest.mark.parametrize("name", sorted(PROGRAMS))
def test_generated_python_matches_interpreter(name, tmp_path, capsys):
    source = PROGRAMS[name]
    expected = interpret(source, capsys)
    assert run_generated(source, tmp_path) == expected


@pytest.mark.parametrize("example", sorted(ROOT.glob("Examples/*.ml")))
def test_examples_match_interpreter(example, tmp_path, capsys):
    source = example.read_text()
    expected = interpret(source, capsys)
    assert run_generated(source, tmp_path) == expected


def test_driver_emit_flag_writes_runnable_python(tmp_path):
    out = tmp_path / "matrix.py"
    emit = subprocess.run(
        [sys.executable, "-m", "mylang.driver", "Examples/matrix.ml", "--emit", str(out)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert emit.returncode == 0, emit.stderr
    run = subprocess.run([sys.executable, str(out)], cwd=ROOT, capture_output=True, text=True, env=ENV)
    interp = subprocess.run([sys.executable, "-m", "mylang.driver", "Examples/matrix.ml"], cwd=ROOT, capture_output=True, text=True)
    assert run.stdout == interp.stdout


def test_generated_code_is_deterministic():
    program = front_end(PROGRAMS["matrix"])
    assert generate_python(program) == generate_python(program)


def test_calls_are_rejected():
    from mylang.lexer import Lexer
    from mylang.parser import Parser

    program = Parser(Lexer("print(f(1));").tokenize()).parse()   # parses; the checker would reject it too
    with pytest.raises(CodegenError, match="not supported"):
        generate_python(program)
