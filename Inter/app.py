from flask import Flask, request, render_template, url_for
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    expr = ''
    if request.method == 'POST':
        expr = request.form['expr']
        code = f"print({expr})\n"
        try:
            result = subprocess.run(
                [sys.executable, 'main.py'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                timeout=10
            )
            output = result.stdout.decode('utf-8') + '\n' + result.stderr.decode('utf-8')
        except Exception as e:
            output = f'Error: {e}'
    return render_template('index.html', output=output, expr=expr)

if __name__ == '__main__':
    app.run(debug=True)
