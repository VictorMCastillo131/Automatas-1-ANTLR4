from django.shortcuts import render
import subprocess
import sys
import os
from django.conf import settings

def index(request):
    output = ''
    error_output = ''
    expr = ''

    if request.method == 'POST':
        expr = request.POST.get('expr', '')
        
        try:
            if expr.strip():
                # Calculadora simple y segura
                allowed_chars = set('0123456789+-*/.() ')
                if all(c in allowed_chars for c in expr):
                    # Reemplaza división por cero
                    if '/0' in expr.replace(' ', ''):
                        error_output = "Error: División por cero"
                    else:
                        resultado = eval(expr)
                        output = str(resultado)
                else:
                    error_output = "Error: Caracteres no permitidos"
            else:
                error_output = "Error: Expresión vacía"
                
        except Exception as e:
            error_output = f"Error en cálculo: {str(e)}"

    context = {
        'output': output, 
        'error_output': error_output, 
        'expr': expr
    }
    return render(request, 'index.html', context)  # ✅ Busca en interpreter/templates/