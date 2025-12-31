## MyLang Tokens

from enum import Enum, auto

class TokenType(Enum):
    # OPERATORS
    PLUS = auto()
    MIN = auto()
    MUL = auto()
    DIV = auto()
    EQUALS = auto()
    EQUALS_EQUALS = auto()
    NOT_EQUALS = auto()
    
    # KEYWORDS
    LET = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    RETURN = auto()
    TRUE = auto()
    FALSE = auto()
    
    # MATRIX SPECIFIC (from MyLang.txt)
    TRANSPOSE = auto()
    REDUCE = auto()
    IS_INVERTIBLE = auto()
    HAS_NULL = auto()
    
    # TYPES & LITERALS
    IDENT = auto()
    INTEGER = auto()
    STRING = auto()
    MATRIX = auto()
    
    # PUNCTUATION
    COMMA = auto()
    SEMI = auto()
    L_PAREN = auto()
    R_PAREN = auto()
    L_BRACK = auto()
    R_BRACK = auto()
    L_BRACE = auto()
    R_BRACE = auto()
    COLON = auto()
    PERIOD = auto()
    EOF = auto()

class Token:
    def __init__(self, type, value=None, line=1, column=1):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.value is not None:
            return f"Token({self.type}, {repr(self.value)})"
        return f"Token({self.type})"

KEYWORDS = {
    "let": TokenType.LET,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "#t": TokenType.TRUE,
    "#f": TokenType.FALSE,
}

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source_code[0] if len(source_code) > 0 else None

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
            
        self.pos += 1
        if self.pos >= len(self.source_code):
            self.current_char = None
        else:
            self.current_char = self.source_code[self.pos]

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.source_code):
            return None
        return self.source_code[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ""
        start_column = self.column
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.INTEGER, int(result), self.line, start_column)

    def get_string(self):
        result = ""
        start_column = self.column
        self.advance() # skip opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        if self.current_char is None:
            raise Exception(f"Unterminated string at line {self.line}, column {start_column}")

        self.advance() # skip closing quote
            
        if len(result) > 256:
            raise Exception(f"String length exceeds 256 chars at line {self.line}, column {start_column}")
            
        return Token(TokenType.STRING, result, self.line, start_column)

    def get_identifier(self):
        result = ""
        start_column = self.column
        
        # Handle #t and #f
        if self.current_char == '#':
            result += self.current_char
            self.advance()
            if self.current_char in ('t', 'f'):
                result += self.current_char
                self.advance()
                return Token(KEYWORDS[result], result, self.line, start_column)

        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = KEYWORDS.get(result, TokenType.IDENT)
        return Token(token_type, result, self.line, start_column)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char.isalpha() or self.current_char == '#':
                return self.get_identifier()

            if self.current_char == '"':
                return self.get_string()

            if self.current_char == '+':
                start_column = self.column
                self.advance()
                return Token(TokenType.PLUS, "+", self.line, start_column)
            
            if self.current_char == '-':
                start_column = self.column
                self.advance()
                return Token(TokenType.MIN, "-", self.line, start_column)
                
            if self.current_char == '*':
                start_column = self.column
                self.advance()
                return Token(TokenType.MUL, "*", self.line, start_column)
                
            if self.current_char == '/':
                start_column = self.column
                self.advance()
                return Token(TokenType.DIV, "/", self.line, start_column)

            if self.current_char == '=':
                start_column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQUALS_EQUALS, "==", self.line, start_column)
                return Token(TokenType.EQUALS, "=", self.line, start_column)

            if self.current_char == '!':
                start_column = self.column
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NOT_EQUALS, "!=", self.line, start_column)
                raise Exception(f"Unexpected character '!' at line {self.line}, column {start_column}")

            if self.current_char == ',':
                start_column = self.column
                self.advance()
                return Token(TokenType.COMMA, ",", self.line, start_column)

            if self.current_char == ';':
                start_column = self.column
                self.advance()
                return Token(TokenType.SEMI, ";", self.line, start_column)

            if self.current_char == '(':
                start_column = self.column
                self.advance()
                return Token(TokenType.L_PAREN, "(", self.line, start_column)

            if self.current_char == ')':
                start_column = self.column
                self.advance()
                return Token(TokenType.R_PAREN, ")", self.line, start_column)

            if self.current_char == '[':
                start_column = self.column
                self.advance()
                return Token(TokenType.L_BRACK, "[", self.line, start_column)

            if self.current_char == ']':
                start_column = self.column
                self.advance()
                return Token(TokenType.R_BRACK, "]", self.line, start_column)

            if self.current_char == '{':
                start_column = self.column
                self.advance()
                return Token(TokenType.L_BRACE, "{", self.line, start_column)

            if self.current_char == '}':
                start_column = self.column
                self.advance()
                return Token(TokenType.R_BRACE, "}", self.line, start_column)

            if self.current_char == ':':
                start_column = self.column
                self.advance()
                return Token(TokenType.COLON, ":", self.line, start_column)

            if self.current_char == '.':
                start_column = self.column
                self.advance()
                return Token(TokenType.PERIOD, ".", self.line, start_column)

            raise Exception(f"Unexpected character '{self.current_char}' at line {self.line}, column {self.column}")

        return Token(TokenType.EOF, None, self.line, self.column)

    def tokenize(self):
        tokens = []
        token = self.get_next_token()
        while token.type != TokenType.EOF:
            tokens.append(token)
            token = self.get_next_token()
        tokens.append(token)
        return tokens
