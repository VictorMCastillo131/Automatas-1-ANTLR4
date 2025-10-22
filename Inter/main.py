import sys
from antlr4 import *
from MiniLangLexer import MiniLangLexer
from MiniLangParser import MiniLangParser
from InterpreterVisitor import InterpreterVisitor

def interpret(code):

    code = code.lstrip()
    if not code.endswith('\n'):
        code = code + '\n'
    input_stream = InputStream(code)

    # 2. Lexer: Divide el flujo en tokens individuales 
    lexer = MiniLangLexer(input_stream)
    stream = CommonTokenStream(lexer)

    # 3. Parser: Construye el árbol sintáctico (AST) 
    parser = MiniLangParser(stream)
    tree = parser.program() # Inicia el parseo 

    # 4. Visitor: Recorre el AST y ejecuta el código 
    visitor = InterpreterVisitor()
    try:
        visitor.visit(tree)
    except (NameError, ValueError) as e:
        print(f"Error de ejecución: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
   
    if not sys.stdin.isatty():
        code = sys.stdin.read()
        interpret(code)
   
    elif len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        interpret(code)
    else:
        
        print("--- Ejecución de MiniLang ---")
        def _ask_int(prompt: str, default: int) -> int:
            while True:
                try:
                    s = input(f"{prompt} [por defecto {default}]: ").strip()
                    if s == "":
                        return default
                    return int(s)
                except ValueError:
                    print("Entrada inválida. Por favor ingresa un entero o presiona Enter para usar el valor por defecto.")
        default_x = 5
        default_y = 3
        print("Introduce valores para las variables:")
        user_x = _ask_int("x", default_x)
        user_y = _ask_int("y", default_y)
        code_input = """
x = 5
y = 3
z = x * y + 10
print(z)
x = x + 1
print(x)
"""
        lines = [ln for ln in code_input.splitlines() if ln.strip() != ""]
        rest_lines = lines[2:] if len(lines) > 2 else []
        rest_lines = [ln.strip() for ln in rest_lines]
        runtime_code = f"x = {user_x}\ny = {user_y}\n" + "\n".join(rest_lines) + "\n"
        interpret(runtime_code)