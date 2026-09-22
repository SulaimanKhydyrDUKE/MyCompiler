# MyCompiler

A small compiler front end and tree-walking interpreter for **MyLang**, a toy language with immutable integers, strings, booleans and integer matrices. Built to learn how compilers work.

## Pipeline

```
source ──▶ Lexer ──▶ Parser ──▶ TypeChecker ──▶ Interpreter
           lexer.py   parser.py   typecheck.py    interpreter.py (+ runtime.py for Matrix)
```

`codegen.py` is reserved for a future code-generation backend and is currently empty.

## Run

```bash
python -m mylang.driver Examples/matrix.ml
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
