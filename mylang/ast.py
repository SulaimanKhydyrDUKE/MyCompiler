class ASTNode:
    def __init__(self, line=None, column=None):
        self.line = line
        self.column = column

class Expression(ASTNode):
    pass

class Statement(ASTNode):
    pass

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__()
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class IntegerLiteral(Expression):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"IntegerLiteral({self.value})"

class StringLiteral(Expression):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"StringLiteral({repr(self.value)})"

class BooleanLiteral(Expression):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value

    def __repr__(self):
        return f"BooleanLiteral({self.value})"

class MatrixLiteral(Expression):
    def __init__(self, rows, line, column):
        super().__init__(line, column)
        self.rows = rows # List of lists of expressions

    def __repr__(self):
        return f"MatrixLiteral({self.rows})"

class Identifier(Expression):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class BinaryExpression(Expression):
    def __init__(self, left, operator, right, line, column):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"BinaryExpression({self.left}, {self.operator}, {self.right})"

class UnaryExpression(Expression):
    def __init__(self, operator, right, line, column):
        super().__init__(line, column)
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"UnaryExpression({self.operator}, {self.right})"

class LetStatement(Statement):
    def __init__(self, name, expression, line, column):
        super().__init__(line, column)
        self.name = name
        self.expression = expression

    def __repr__(self):
        return f"LetStatement({self.name}, {self.expression})"

class IfStatement(Statement):
    def __init__(self, condition, then_branch, else_branch, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfStatement({self.condition}, {self.then_branch}, {self.else_branch})"

class WhileStatement(Statement):
    def __init__(self, condition, body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.body})"

class PrintStatement(Statement):
    def __init__(self, expression, line, column):
        super().__init__(line, column)
        self.expression = expression

    def __repr__(self):
        return f"PrintStatement({self.expression})"

class Block(Statement):
    def __init__(self, statements, line, column):
        super().__init__(line, column)
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class CallExpression(Expression):
    def __init__(self, callee, arguments, line, column):
        super().__init__(line, column)
        self.callee = callee
        self.arguments = arguments

    def __repr__(self):
        return f"CallExpression({self.callee}, {self.arguments})"

class MemberCallExpression(Expression):
    def __init__(self, object, method, arguments, line, column):
        super().__init__(line, column)
        self.object = object
        self.method = method
        self.arguments = arguments

    def __repr__(self):
        return f"MemberCallExpression({self.object}, {self.method}, {self.arguments})"


class ExpressionStatement(Statement):
    def __init__(self, expression, line, column):
        super().__init__(line, column)
        self.expression = expression

    def __repr__(self):
        return f"ExpressionStatement({self.expression})"
