from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import subprocess
import sys
import os

# Importar la configuración de Django para acceder a BASE_DIR
from django.conf import settings

@csrf_exempt
def index(request):
    output = ''
    expr = ''
    if request.method == 'POST':
        expr = request.POST.get('expr','')
        code = f"print({expr})\n"
        try:
            result = subprocess.run(
                [sys.executable, '/home/vicc/ANTLR/Calcu/main.py'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd='/home/vicc/ANTLR/Calcu',
                timeout=10
            )
            output = result.stdout.decode('utf-8') + '\n' + result.stderr.decode('utf-8')
        except Exception as e:
            output = f'Error: {e}'
    return render(request, 'index.html', {'output': output, 'expr': expr})