from flask import Flask, render_template, request, redirect, url_for
import os
import json 
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/template')
def template():
    return render_template('perfil_template.html')

@app.route('/profesion')
def profesion():
    return render_template('profesion.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/ubicacion')
def ubicacion():
    return render_template('ubicacion.html')

cargarimagen = 'static/uploads'
app.config['cargarimagen'] = cargarimagen

# Carpeta donde se guardarán las imágenes subidas
app.config['guardarimagen'] = 'static/uploads'
app.config['extensionpermitida'] = {'png', 'jpg', 'jpeg', 'gif'}

# Lista para almacenar los expertos
expertos = []

# Ruta del archivo JSON
JSON_FILE = 'static/json/expertos.json'

# Función para guardar la lista de expertos en un archivo JSON
def guardar_expertos_en_json():
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(expertos, f, ensure_ascii=False, indent=4)

# Función para verificar si el archivo tiene una extensión permitida
def archivopermitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['extensionpermitida']


@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    telefono = request.form['telefono']
    ciudad = request.form['ciudad']
    imagen = request.files['imagen']
    
    # Determinamos la profesión en función de la URL donde nos encontramos
    referer = request.headers.get('Referer')
    profesion = determinar_profesion(referer)

    if imagen and archivopermitido(imagen.filename):
        
        archivobase = nombre.replace(" ", "_") + os.path.splitext(imagen.filename)[1]
        filepath = os.path.join(app.config['guardarimagen'], archivobase)
        
        # Verificar si el archivo ya existe y generar un nombre único si es necesario
        counter = 1
        while os.path.exists(filepath):
            filename = f"{nombre.replace(' ', '_')}_{counter}{os.path.splitext(imagen.filename)[1]}"
            filepath = os.path.join(app.config['guardarimagen'], filename)
            counter += 1
        imagen.save(filepath)

        # Agregar la información del experto a la lista
        experto = {
            'nombre': nombre,
            'descripcion': descripcion,
            'telefono': telefono,
            'ciudad': ciudad,
            'profesion': profesion,
            'imagen': os.path.basename(filepath)
        }
        expertos.append(experto)

        # Guardar los expertos en el archivo JSON
        guardar_expertos_en_json()

        # Crear una página HTML para el experto
        crearpagexperto(experto)

    # Redirigir a la página principal para mostrar las nuevas cards
    return redirect(url_for('profesion'))

@app.route('/ubicacion/pereira')
def pereira():
    pereira = [experto for experto in expertos if experto['ciudad'] == 'Pereira']
    return render_template('pereira.html', expertos=pereira)

@app.route('/ubicacion/dosquebradas')
def dosquebradas():
    dosquebradas = [experto for experto in expertos if experto['ciudad'] == 'Dosquebradas']
    return render_template('dosquebradas.html', expertos=dosquebradas)

@app.route('/profesion/fontaneros')
def fontaneros():
    # Filtrar expertos por la profesión "fontanero"
    fontaneros = [experto for experto in expertos if experto['profesion'] == 'fontanero']
    return render_template('fontaneros.html', expertos=fontaneros)

@app.route('/profesion/carpinteros')
def carpinteros():
    # Filtrar expertos por la profesión "carpinteros"
    carpinteros = [experto for experto in expertos if experto['profesion'] == 'carpintero']
    return render_template('carpinteros.html', expertos=carpinteros)

@app.route('/profesion/electricistas')
def electricistas():
    # Filtrar expertos por la profesión "electricista"
    electricistas = [experto for experto in expertos if experto['profesion'] == 'electricista']
    return render_template('electricistas.html', expertos=electricistas)

@app.route('/perfil/<nombre>')
def perfil(nombre):
    # Generamos el nombre del archivo HTML del experto
    filename = nombre.replace(" ", "_").lower() + '.html'
    
    # Comprobamos si el archivo existe
    filepath = os.path.join('templates/perfiles', filename)
    if os.path.exists(filepath):
        # Si existe, lo renderizamos como una página HTML
        return render_template('perfiles/'+filename)  # Flask buscará el archivo en la carpeta templates
    else:
        # Si el archivo no existe, redirigimos a la página principal
        return redirect(url_for('index.html'))

def crearpagexperto(experto):
    # Creamos el nombre del archivo basándonos en el nombre del experto y reemplazamos los espacios por guiones bajos
    arvhicobase = experto['nombre'].replace(" ", "_").lower()
    filename = arvhicobase + '.html'
    
    # Definimos la ruta del archivo HTML en la carpeta templates
    filepath = os.path.join('templates/perfiles', filename)
    
    # Si el archivo ya existe, generar un nuevo nombre único
    counter = 1
    while os.path.exists(filepath):
        filename = f"{arvhicobase}_{counter}.html"
        filepath = os.path.join('templates/perfiles', filename)
        counter += 1

    # Crear el contenido de la página HTML para el experto
    content = render_template('perfil_template.html', experto=experto)

    # Guardar el archivo HTML en la carpeta templates/perfiles
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# función para agregar internamente la profesión al usuario que se registra, dependiendo de la página que lo haga
def determinar_profesion(referer):
    if referer:
        path = urlparse(referer).path
        if 'electricistas' in path:
            return 'electricista'
        elif 'fontaneros' in path:
            return 'fontanero'
        elif 'carpinteros' in path:
            return 'carpintero'
    return 'desconocida'  # Valor predeterminado si no se reconoce la profesión
    
if __name__ == '__main__':
    # Cargar los expertos desde el archivo JSON si existe
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            expertos = json.load(f)
            
    app.run(debug=True)
