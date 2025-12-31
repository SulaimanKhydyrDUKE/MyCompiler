from enum import Enum, auto

class Type(Enum):
    INTEGER = auto()
    STRING = auto()
    BOOLEAN = auto()
    MATRIX = auto()
    VOID = auto()

    def __repr__(self):
        return self.name

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def define(self, name, type):
        self.symbols[name] = type

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

class TypeChecker:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def check(self, node):
        method_name = f"check_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_check)
        return visitor(node)

    def generic_check(self, node):
        raise Exception(f"No check_{type(node).__name__} method defined")

    def check_Program(self, node):
        for stmt in node.statements:
            self.check(stmt)
        return Type.VOID

    def check_LetStatement(self, node):
        if node.name in self.symbol_table.symbols:
            raise Exception(f"Variable '{node.name}' already defined at line {node.line}")
        
        expr_type = self.check(node.expression)
        self.symbol_table.define(node.name, expr_type)
        return Type.VOID

    def check_IfStatement(self, node):
        cond_type = self.check(node.condition)
        if cond_type != Type.BOOLEAN:
            raise Exception(f"If condition must be BOOLEAN, got {cond_type} at line {node.line}")
        
        # Save current symbol table for scoping
        previous_table = self.symbol_table
        self.symbol_table = SymbolTable(previous_table)
        self.check(node.then_branch)
        self.symbol_table = previous_table
        
        if node.else_branch:
            self.symbol_table = SymbolTable(previous_table)
            self.check(node.else_branch)
            self.symbol_table = previous_table
            
        return Type.VOID

    def check_WhileStatement(self, node):
        cond_type = self.check(node.condition)
        if cond_type != Type.BOOLEAN:
            raise Exception(f"While condition must be BOOLEAN, got {cond_type} at line {node.line}")
        
        previous_table = self.symbol_table
        self.symbol_table = SymbolTable(previous_table)
        self.check(node.body)
        self.symbol_table = previous_table
        return Type.VOID

    def check_PrintStatement(self, node):
        self.check(node.expression)
        return Type.VOID

    def check_Block(self, node):
        previous_table = self.symbol_table
        self.symbol_table = SymbolTable(previous_table)
        for stmt in node.statements:
            self.check(stmt)
        self.symbol_table = previous_table
        return Type.VOID

    def check_IntegerLiteral(self, node):
        return Type.INTEGER

    def check_StringLiteral(self, node):
        return Type.STRING

    def check_BooleanLiteral(self, node):
        return Type.BOOLEAN

    def check_MatrixLiteral(self, node):
        for row in node.rows:
            for element in row:
                if self.check(element) != Type.INTEGER:
                    raise Exception(f"Matrix elements must be INTEGER at line {node.line}")
        return Type.MATRIX

    def check_Identifier(self, node):
        type = self.symbol_table.lookup(node.name)
        if type is None:
            raise Exception(f"Undefined variable '{node.name}' at line {node.line}")
        return type

    def check_BinaryExpression(self, node):
        left_type = self.check(node.left)
        right_type = self.check(node.right)
        
        if node.operator == "=":
            # Immutability check
            raise Exception(f"Cannot assign to immutable variable at line {node.line}")

        if node.operator in ("+", "-", "*", "/"):
            if left_type == Type.INTEGER and right_type == Type.INTEGER:
                return Type.INTEGER
            if node.operator == "+" and left_type == right_type:
                # Based on MyLang.txt: "+" adds two data units of the same type
                return left_type
            raise Exception(f"Invalid types for operator '{node.operator}': {left_type} and {right_type} at line {node.line}")

        if node.operator in ("==", "!="):
            if left_type == right_type:
                return Type.BOOLEAN
            raise Exception(f"Cannot compare different types: {left_type} and {right_type} at line {node.line}")

        raise Exception(f"Unknown operator '{node.operator}' at line {node.line}")

    def check_MemberCallExpression(self, node):
        obj_type = self.check(node.object)
        if obj_type != Type.MATRIX:
            raise Exception(f"Member call '{node.method}' only allowed on MATRIX, got {obj_type} at line {node.line}")
        
        if node.method in ("isInvertible", "hasNull"):
            return Type.BOOLEAN
        if node.method == "Transpose":
            return Type.MATRIX
        if node.method == "Reduce":
            return Type.MATRIX
            
        raise Exception(f"Unknown matrix method '{node.method}' at line {node.line}")

    def check_CallExpression(self, node):
        # We don't have user-defined functions yet, but we might have built-ins
        raise Exception(f"User defined functions not supported yet at line {node.line}")
