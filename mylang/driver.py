import sys
from mylang.lexer import Lexer
from mylang.parser import Parser
from mylang.typecheck import TypeChecker
from mylang.interpreter import Interpreter

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            source = f.read()
    else:
        source = """
        let a = 10;
        let b = 20;
        let c = a + b * 2;
        print("C is:");
        print(c);
        if (c == 50) {
            print("Success: c is 50");
        } else {
            print("Failure: c is not 50");
        }
        
        let m = [[1, 2], [3, 4]];
        print("Matrix m:");
        print(m);
        let t = m.Transpose();
        print("Transposed m:");
        print(t);
        
        let inv = m.isInvertible();
        print("Is m invertible?");
        print(inv);
        """
    
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        checker = TypeChecker()
        checker.check(ast)
        
        interpreter = Interpreter()
        interpreter.interpret(ast)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

