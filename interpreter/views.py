from django.shortcuts import render
import subprocess
import sys
import os
from django.conf import settings

# @csrf_exempt  <-- ¡Eliminado! Es una mala práctica de seguridad.
# Usaremos {% csrf_token %} en el template en su lugar.
def index(request):
    output = ''
    error_output = ''
    expr = ''

    # Construir rutas dinámicas para que funcione en cualquier entorno (local o Render)
    # Esto asume que el proyecto 'Calcu' está en el mismo nivel que 'minilang_django'
    calcu_project_path = settings.BASE_DIR.parent / 'Calcu'
    main_py_path = calcu_project_path / 'main.py'

    if request.method == 'POST':
        expr = request.POST.get('expr', '')
        # ADVERTENCIA DE SEGURIDAD: Ejecutar código directamente del usuario
        # es extremadamente peligroso (Inyección de Código).
        # Esto es aceptable solo si es un proyecto personal y confías 100% en la entrada.
        # Ya no necesitamos "print()", solo pasamos la expresión directamente.

        try:
            result = subprocess.run(
                [sys.executable, main_py_path],
                input=expr.encode('utf-8'), # Enviamos la expresión directamente
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=calcu_project_path, # Ejecutar desde el directorio del script
                timeout=10, # Previene que el proceso se cuelgue indefinidamente
                check=False # No lanza excepción si el script falla, lo manejamos manualmente
            )
            output = result.stdout.decode('utf-8')
            error_output = result.stderr.decode('utf-8')
        except Exception as e:
            error_output = f'Error al ejecutar el subproceso: {e}'

    context = {'output': output, 'error_output': error_output, 'expr': expr}
    return render(request, 'index.html', context)