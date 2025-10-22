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

    # --- INICIO DE LA CORRECCIÓN ---

    # Definir las rutas dinámicamente usando BASE_DIR de settings.py
    # (BASE_DIR apunta a la carpeta raíz 'minilang_django/')
    inter_directory = settings.BASE_DIR / 'Inter'
    main_py_script = inter_directory / 'main.py'

    # --- FIN DE LA CORRECCIÓN ---

    if request.method == 'POST':
        expr = request.POST.get('expr','')
        code = f"print({expr})\n"
        try:
            # Usar las rutas dinámicas en lugar de las rutas 'hardcoded'
            result = subprocess.run(
                [sys.executable, main_py_script],  # Ruta corregida
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=inter_directory,               # Ruta corregida
                timeout=10
            )
            output = result.stdout.decode('utf-8') + '\n' + result.stderr.decode('utf-8')
        except Exception as e:
            output = f'Error: {e}'
    return render(request, 'index.html', {'output': output, 'expr': expr})