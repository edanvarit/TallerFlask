from flask import Flask, render_template, request, abort

app = Flask(__name__)

def calcular_estado(nota1, nota2, nota3, asistencia):
    promedio = (nota1 + nota2 + nota3) / 3
    estado = "Aprobado" if promedio >= 40 and asistencia >= 75 else "Reprobado"
    return promedio, estado

def nombre_mas_largo(nombres):
    cantidades = [sum(c.isalpha() for c in n) for n in nombres]
    maximo = max(cantidades)
    ganadores = [n for n, c in zip(nombres, cantidades) if c == maximo]
    return ganadores, maximo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejercicio1', methods=['GET', 'POST'])
def ejercicio1():
    if request.method == 'POST':
        try:
            nota1 = float(request.form['nota1'])
            nota2 = float(request.form['nota2'])
            nota3 = float(request.form['nota3'])
            asistencia = float(request.form['asistencia'])
        except (KeyError, ValueError):
            abort(400)
        if not all(10 <= n <= 70 for n in (nota1, nota2, nota3)) or not 0 <= asistencia <= 100:
            abort(400)
        promedio, estado = calcular_estado(nota1, nota2, nota3, asistencia)
        return render_template('resultado1.html', promedio=round(promedio, 1),
                                asistencia=asistencia, estado=estado)
    return render_template('ejercicio1.html')

@app.route('/ejercicio2', methods=['GET', 'POST'])
def ejercicio2():
    if request.method == 'POST':
        nombres = [request.form.get(f'nombre{i}', '').strip() for i in (1, 2, 3)]
        if not all(nombres) or not all(any(c.isalpha() for c in n) for n in nombres):
            abort(400)
        ganadores, cantidad = nombre_mas_largo(nombres)
        return render_template('resultado2.html', ganadores=ganadores, cantidad=cantidad)
    return render_template('ejercicio2.html')

@app.errorhandler(400)
def datos_invalidos(_):
    return render_template('error.html'), 400

if __name__ == '__main__':
    app.run(debug=True)