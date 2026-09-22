"""Recursive-descent parser for MyLang.

Grammar (see MyLang.txt):

    program     := statement* EOF
    statement   := 'let' IDENT '=' expression ';'
                 | 'if' '(' expression ')' block ('else' (block | if_statement))?
                 | 'while' '(' expression ')' block
                 | 'print' '(' expression ')' ';'
                 | block
                 | expression ';'
    block       := '{' statement* '}'
    expression  := assignment
    assignment  := equality ('=' assignment)?
    equality    := additive (('==' | '!=') additive)*
    additive    := term (('+' | '-') term)*
    term        := unary (('*' | '/') unary)*
    unary       := '-' unary | postfix
    postfix     := primary ('.' IDENT '(' arguments? ')')*
    primary     := INTEGER | STRING | '#t' | '#f'
                 | IDENT ('(' arguments? ')')?
                 | '(' expression ')'
                 | matrix
    matrix      := '[' row (',' row)* ']'
    row         := '[' expression (',' expression)* ']'
    arguments   := expression (',' expression)*

Assignment is parsed so the type checker can reject it: MyLang values are
immutable, and "a = b" is a type error rather than a syntax error.
"""

from .lexer import TokenType
from .ast import (
    Program,
    IntegerLiteral,
    StringLiteral,
    BooleanLiteral,
    MatrixLiteral,
    Identifier,
    BinaryExpression,
    UnaryExpression,
    CallExpression,
    MemberCallExpression,
    LetStatement,
    IfStatement,
    WhileStatement,
    PrintStatement,
    ExpressionStatement,
    Block,
)


class ParseError(Exception):
    pass


def _describe(token):
    if token.type == TokenType.EOF:
        return "end of input"
    if token.value is not None:
        return repr(token.value)
    return token.type.name


class Parser:
    def __init__(self, tokens):
        if not tokens or tokens[-1].type != TokenType.EOF:
            raise ParseError("Token stream must end with EOF")
        self.tokens = tokens
        self.pos = 0

    # ----- token helpers -------------------------------------------------

    def current(self):
        return self.tokens[self.pos]

    def at(self, *types):
        return self.current().type in types

    def advance(self):
        token = self.current()
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def match(self, *types):
        if self.at(*types):
            return self.advance()
        return None

    def expect(self, token_type, what=None):
        if self.at(token_type):
            return self.advance()
        token = self.current()
        wanted = what or token_type.name
        raise ParseError(
            f"Expected {wanted} but found {_describe(token)} "
            f"at line {token.line}, column {token.column}"
        )

    # ----- entry point ---------------------------------------------------

    def parse(self):
        statements = []
        while not self.at(TokenType.EOF):
            statements.append(self.statement())
        return Program(statements)

    # ----- statements ----------------------------------------------------

    def statement(self):
        if self.at(TokenType.LET):
            return self.let_statement()
        if self.at(TokenType.IF):
            return self.if_statement()
        if self.at(TokenType.WHILE):
            return self.while_statement()
        if self.at(TokenType.PRINT):
            return self.print_statement()
        if self.at(TokenType.L_BRACE):
            return self.block()
        token = self.current()
        expression = self.expression()
        self.expect(TokenType.SEMI, "';'")
        return ExpressionStatement(expression, token.line, token.column)

    def let_statement(self):
        token = self.expect(TokenType.LET, "'let'")
        name = self.expect(TokenType.IDENT, "a variable name").value
        self.expect(TokenType.EQUALS, "'='")
        expression = self.expression()
        self.expect(TokenType.SEMI, "';'")
        return LetStatement(name, expression, token.line, token.column)

    def if_statement(self):
        token = self.expect(TokenType.IF, "'if'")
        self.expect(TokenType.L_PAREN, "'('")
        condition = self.expression()
        self.expect(TokenType.R_PAREN, "')'")
        then_branch = self.block()
        else_branch = None
        if self.match(TokenType.ELSE):
            if self.at(TokenType.IF):
                else_branch = self.if_statement()
            else:
                else_branch = self.block()
        return IfStatement(condition, then_branch, else_branch, token.line, token.column)

    def while_statement(self):
        token = self.expect(TokenType.WHILE, "'while'")
        self.expect(TokenType.L_PAREN, "'('")
        condition = self.expression()
        self.expect(TokenType.R_PAREN, "')'")
        body = self.block()
        return WhileStatement(condition, body, token.line, token.column)

    def print_statement(self):
        token = self.expect(TokenType.PRINT, "'print'")
        self.expect(TokenType.L_PAREN, "'('")
        expression = self.expression()
        self.expect(TokenType.R_PAREN, "')'")
        self.expect(TokenType.SEMI, "';'")
        return PrintStatement(expression, token.line, token.column)

    def block(self):
        token = self.expect(TokenType.L_BRACE, "'{'")
        statements = []
        while not self.at(TokenType.R_BRACE, TokenType.EOF):
            statements.append(self.statement())
        self.expect(TokenType.R_BRACE, "'}'")
        return Block(statements, token.line, token.column)

    # ----- expressions ---------------------------------------------------

    def expression(self):
        return self.assignment()

    def assignment(self):
        left = self.equality()
        token = self.match(TokenType.EQUALS)
        if token:
            right = self.assignment()
            return BinaryExpression(left, "=", right, token.line, token.column)
        return left

    def equality(self):
        left = self.additive()
        while True:
            token = self.match(TokenType.EQUALS_EQUALS, TokenType.NOT_EQUALS)
            if not token:
                return left
            right = self.additive()
            left = BinaryExpression(left, token.value, right, token.line, token.column)

    def additive(self):
        left = self.term()
        while True:
            token = self.match(TokenType.PLUS, TokenType.MIN)
            if not token:
                return left
            right = self.term()
            left = BinaryExpression(left, token.value, right, token.line, token.column)

    def term(self):
        left = self.unary()
        while True:
            token = self.match(TokenType.MUL, TokenType.DIV)
            if not token:
                return left
            right = self.unary()
            left = BinaryExpression(left, token.value, right, token.line, token.column)

    def unary(self):
        token = self.match(TokenType.MIN)
        if token:
            operand = self.unary()
            return UnaryExpression("-", operand, token.line, token.column)
        return self.postfix()

    def postfix(self):
        node = self.primary()
        while True:
            token = self.match(TokenType.PERIOD)
            if not token:
                return node
            method = self.expect(TokenType.IDENT, "a method name").value
            self.expect(TokenType.L_PAREN, "'('")
            arguments = self.arguments()
            self.expect(TokenType.R_PAREN, "')'")
            node = MemberCallExpression(node, method, arguments, token.line, token.column)

    def arguments(self):
        arguments = []
        if self.at(TokenType.R_PAREN):
            return arguments
        arguments.append(self.expression())
        while self.match(TokenType.COMMA):
            arguments.append(self.expression())
        return arguments

    def primary(self):
        token = self.current()

        if self.match(TokenType.INTEGER):
            return IntegerLiteral(token.value, token.line, token.column)
        if self.match(TokenType.STRING):
            return StringLiteral(token.value, token.line, token.column)
        if self.match(TokenType.TRUE):
            return BooleanLiteral(True, token.line, token.column)
        if self.match(TokenType.FALSE):
            return BooleanLiteral(False, token.line, token.column)

        if self.match(TokenType.IDENT):
            identifier = Identifier(token.value, token.line, token.column)
            if self.match(TokenType.L_PAREN):
                arguments = self.arguments()
                self.expect(TokenType.R_PAREN, "')'")
                return CallExpression(identifier, arguments, token.line, token.column)
            return identifier

        if self.match(TokenType.L_PAREN):
            expression = self.expression()
            self.expect(TokenType.R_PAREN, "')'")
            return expression

        if self.at(TokenType.L_BRACK):
            return self.matrix()

        raise ParseError(
            f"Unexpected {_describe(token)} at line {token.line}, column {token.column}"
        )

    def matrix(self):
        token = self.expect(TokenType.L_BRACK, "'['")
        rows = [self.matrix_row()]
        while self.match(TokenType.COMMA):
            rows.append(self.matrix_row())
        self.expect(TokenType.R_BRACK, "']'")
        width = len(rows[0])
        for row in rows:
            if len(row) != width:
                raise ParseError(
                    f"Matrix rows must have the same length at line {token.line}, column {token.column}"
                )
        return MatrixLiteral(rows, token.line, token.column)

    def matrix_row(self):
        self.expect(TokenType.L_BRACK, "'['")
        elements = [self.expression()]
        while self.match(TokenType.COMMA):
            elements.append(self.expression())
        self.expect(TokenType.R_BRACK, "']'")
        return elements
