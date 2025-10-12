## MyLang Tokens

##OPERATORS
PLUS = "PLUS"
MIN = "MIN"
MUL = "MUL"
DIV = "DIV" 
EQUALS = "EQUALS"
EQUALS_EQUALS = "EQUALS_EQUALS"
NOT_EQUALS = "NOT_EQUALS"


##KEYWORDS
LET = "LET"
IF = "IF"
ELSE = "ELSE"
PRINT = "PRINT"
TRANSPOSE = "TRANSPOSE"
DOT_PRODUCT = "DOT_PRODUCT"
REDUCE = "REDUCE"
ECHELON = "ECHELON"
TRUE_S = "TRUE"
FALSE_S = "FALSE"


WHILE = "WHILE"
RETURN = "RETURN"


##TYPE
IDENT = "IDENT"
INTEGER = "INTEGER"
STRING = "STRING"
MATRIX = "MATRIX"

#GRAMM
COMMA = "COMMA"
SEMI = "SEMI"
L_PAREN = "L_PAREN"
R_PAREN = "R_PAREN"
L_BRACK = "L_BRACK"
R_BRACK = "R_BRACK"
L_BRACE = "L_BRACE"
R_BRACE = "R_BRACE"
COLON = "COLON"
PERIOD = "PERIOD"

numbers = '0123456789'
characters = 'zxcvbnmasdfghjklqwertyuiop'

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = -1
        self.current_char = None

        Tokens = []

        return self
         
    def move(self):
        self.pos += 1
        self.current_char = self.source_code[pos] if self.pos < len(self.source_code) else None 

    def tokenizer(self):

        my_tokens = []
        while(self.current_char != None):
            if(self.current_char=="+"):
                my_tokens.append = PLUS
            elif self.current_char == "-":
                my_tokens.append = MIN
            elif self.current_char == "*":
                my_tokens.append = MUL
            elif self.current_char == "/":
                my_tokens.append = DIV
            elif self.current_char == "(":
                my_tokens.append = L_PAREN
            elif self.current_char == ")":
                my_tokens.append = R_PAREN
            elif self.current_char == "-":
                my_tokens.append = MIN
            
            
