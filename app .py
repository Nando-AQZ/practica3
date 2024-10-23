from flask import Flask,request,render_template,url_for,redirect,session

app = Flask(__name__)
app.secret_key='fernando45'


@app.route("/")
def index():
    if 'lista' not in session:
        # Inicializar carrito como lista
        session['lista'] = []
           
    return render_template('index.html',lista = session['lista'])
   
@app.route("/procesa",methods=['POST'])
def procesa():
    fecha = request.form.get('fecha')
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    turno = request.form.get('turno')
    seminario = request.form.get('seminario')
    
    if 'lista' not in session:
        # Inicializar carrito como lista
        session['lista'] = []
        
    # Agregar el producto al carrito
    session['lista'].append({'fecha':fecha,'nombre':nombre,'apellido':apellido,'turno':turno,'seminario':seminario })
    session.modified = True
    
    return redirect(url_for("index"))


@app.route("/eliminar/<int:item_index>", methods=['POST'])
def eliminar(item_index):
    if 'lista' in session and 0 <= item_index < len(session['lista']):
        del session['lista'][item_index]
        session.modified = True
    return redirect(url_for("index"))

@app.route("/modificar/<int:item_index>", methods=['GET', 'POST'])
def modificar(item_index):
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.form.get('fecha')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        turno = request.form.get('turno')
        seminarios = request.form.getlist('seminario')  # Obtiene la lista de seminarios seleccionados

        # Verifica si 'lista' existe en la sesión
        if 'lista' not in session:
            session['lista'] = []

        # Modifica solo los campos especificados
        if fecha:
            session['lista'][item_index]['fecha'] = fecha
        if nombre:
            session['lista'][item_index]['nombre'] = nombre
        if apellido:
            session['lista'][item_index]['apellido'] = apellido
        if turno:
            session['lista'][item_index]['turno'] = turno
        if seminarios:
            session['lista'][item_index]['seminario'] = ", ".join(seminarios)  # Concatena la lista en una cadena

        session.modified = True
        
        return redirect(url_for("index"))  # Redirige a la página principal después de la modificación

    # Si es un GET, muestra el formulario con los datos actuales
    item = session['lista'][item_index]
    return render_template('modificar.html', item=item, item_index=item_index)


@app.route('/registro')
def registro():
    return render_template('registro.html')
if __name__=="__main__":
    app.run(debug=True)

