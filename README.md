# MyCompiler

A small compiler front end and tree-walking interpreter for **MyLang**, a toy language with immutable integers, strings, booleans and integer matrices. Built to learn how compilers work.

## Pipeline

```
source ──▶ Lexer ──▶ Parser ──▶ TypeChecker ──▶ Interpreter        (run)
           lexer.py   parser.py   typecheck.py    interpreter.py + runtime.py
                                              └─▶ PythonCodegen      (--emit)
                                                  codegen.py
```

`codegen.py` is a first backend: it emits the checked program as Python source that calls the same `runtime.Matrix`, so the generated program prints exactly what the interpreter prints. Block scoping is preserved by renaming each `let` to a fresh Python name.

## Run

```bash
python -m mylang.driver Examples/matrix.ml                  # interpret
python -m mylang.driver Examples/matrix.ml --emit out.py    # compile to Python
PYTHONPATH=. python out.py                                  # the output imports mylang.runtime
```

## Test

```bash
python -m pip install pytest
python -m pytest tests -q
```

## The language

See [`MyLang.txt`](MyLang.txt) for the informal spec. In short:

- `let name = expr;` binds an immutable value. Assignment (`a = 2;`) is a type error.
- Types: integer, string, boolean (`#t` / `#f`), matrix of integers (`[[1, 2], [3, 4]]`).
- Operators: `+ - * /` on integers, `+` on two strings, `==` / `!=` on equal types, unary `-`.
- Matrix methods: `.Transpose()`, `.Reduce()`, `.isInvertible()`, `.hasNull()`.
- Statements: `if (...) { } else { }`, `while (...) { }`, `print(...)`, blocks.

## Known limitations

- Values are immutable and `let` inside a block shadows rather than updates, so a `while` loop has no way to change its own condition and cannot terminate. The loop is parsed and type-checked but is not useful yet.
- `Reduce()` produces floats even though the spec says matrices hold integers.
- No user-defined functions; calling one is a type error.
