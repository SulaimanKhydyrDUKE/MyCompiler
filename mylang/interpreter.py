from .runtime import Matrix

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Undefined variable '{name}'")

class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, node):
        try:
            method_name = f"visit_{type(node).__name__}"
            visitor = getattr(self, method_name, self.generic_visit)
            return visitor(node)
        except Exception as e:
            # Re-raise with line info if possible
            if hasattr(node, 'line') and node.line:
                raise Exception(f"Runtime error at line {node.line}: {e}")
            raise e

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_Program(self, node):
        for stmt in node.statements:
            self.interpret(stmt)

    def visit_LetStatement(self, node):
        value = self.interpret(node.expression)
        self.environment.define(node.name, value)

    def visit_IfStatement(self, node):
        condition = self.interpret(node.condition)
        if condition:
            previous_env = self.environment
            self.environment = Environment(previous_env)
            self.interpret(node.then_branch)
            self.environment = previous_env
        elif node.else_branch:
            previous_env = self.environment
            self.environment = Environment(previous_env)
            self.interpret(node.else_branch)
            self.environment = previous_env

    def visit_WhileStatement(self, node):
        while self.interpret(node.condition):
            previous_env = self.environment
            self.environment = Environment(previous_env)
            self.interpret(node.body)
            self.environment = previous_env

    def visit_PrintStatement(self, node):
        value = self.interpret(node.expression)
        if value is True:
            print("#t")
        elif value is False:
            print("#f")
        else:
            print(value)

    def visit_ExpressionStatement(self, node):
        self.interpret(node.expression)

    def visit_UnaryExpression(self, node):
        value = self.interpret(node.right)
        if node.operator == "-":
            return -value
        raise Exception(f"Unknown unary operator {node.operator}")

    def visit_Block(self, node):
        previous_env = self.environment
        self.environment = Environment(previous_env)
        for stmt in node.statements:
            self.interpret(stmt)
        self.environment = previous_env

    def visit_IntegerLiteral(self, node):
        return node.value

    def visit_StringLiteral(self, node):
        return node.value

    def visit_BooleanLiteral(self, node):
        return node.value

    def visit_MatrixLiteral(self, node):
        data = []
        for row_exprs in node.rows:
            row = [self.interpret(expr) for expr in row_exprs]
            data.append(row)
        return Matrix(data)

    def visit_Identifier(self, node):
        return self.environment.get(node.name)

    def visit_BinaryExpression(self, node):
        left = self.interpret(node.left)
        right = self.interpret(node.right)
        
        op = node.operator
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "*": return left * right
        if op == "/": return left // right # Integer division
        if op == "==": return left == right
        if op == "!=": return left != right
        
        raise Exception(f"Unknown operator {op}")

    def visit_MemberCallExpression(self, node):
        obj = self.interpret(node.object)
        if not isinstance(obj, Matrix):
            raise Exception("Member call only supported on Matrix")
        
        if node.method == "Transpose":
            return obj.transpose()
        if node.method == "Reduce":
            return obj.reduce()
        if node.method == "isInvertible":
            return obj.is_invertible()
        if node.method == "hasNull":
            return obj.has_null()
            
        raise Exception(f"Unknown method {node.method}")

