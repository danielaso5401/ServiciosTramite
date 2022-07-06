from flask import Flask, render_template, request
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, render_template, request
from flask import Flask,request, jsonify


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class curso(db.Model):
    idCurso=db.Column(db.Integer, primary_key=True)
    Cursonombre=db.Column(db.String(45), nullable=False, unique=True)
    Cursomodalidad=db.Column(db.String(45), nullable=False, unique=True)
    def __init__(self, idCurso, Cursonombre,Cursomodalidad):
        self.idCurso=idCurso
        self.Cursonombre=Cursonombre
        self.Cursomodalidad=Cursomodalidad

class Usuario(db.Model):
    idUsuario = db.Column(db.Integer, primary_key=True)
    UsuarioName =db.Column(db.String(45), nullable=False, unique=True)
    UsuarioApellidos =db.Column(db.String(45), nullable=False)
    UsuarioContraseña = db.Column(db.String(45), nullable=False)
    UsuarioDni = db.Column(db.Integer, nullable=False)
    Usuariosede = db.Column(db.String(45), nullable=False)
    Usuariocorreo = db.Column(db.String(45), nullable=False)
    Curso_idCurso = db.Column(db.String(45),nullable=False)
    def __init__(self, idUsuario, UsuarioName, UsuarioApellidos, UsuarioContraseña,UsuarioDNI,Usuariosede,Usuariocorreo,Curso_idCurso):
        self.idUsuario = idUsuario
        self.UsuarioName = UsuarioName
        self.UsuarioApellidos = UsuarioApellidos
        self.UsuarioContraseña = UsuarioContraseña
        self.UsuarioDNI = UsuarioDNI
        self.Usuariosede = Usuariosede
        self.Usuariocorreo = Usuariocorreo
        self.Curso_idCurso=Curso_idCurso

class tramitetipo(db.Model):
    idTramitetipo=db.Column(db.Integer, primary_key=True)
    Nombretipo=db.Column(db.String(45), nullable=False, unique=True)
    def __init__(self, idTramitetipo, Nombretipo):
        self.idTramitetipo=idTramitetipo
        self.Nombretipo=Nombretipo

class estadodeltramite(db.Model):
    idEstadodeltramite=db.Column(db.Integer, primary_key=True)
    Fecha=db.Column(db.DateTime, nullable=False, unique=True)
    Asunto=db.Column(db.String(45), nullable=False, unique=True)
    def __init__(self, idEstadodeltramite, Fecha, Asunto):
        self.idEstadodeltramite=idEstadodeltramite
        self.Fecha=Fecha                
        self.Asunto=Asunto

class tramite(db.Model):
    idTramite = db.Column(db.Integer, primary_key=True)
    Tramiteremitente =db.Column(db.String(45), nullable=False, unique=True)
    Tramiteasunto =db.Column(db.String(45), nullable=False)
    Tramitefecha = db.Column(db.DateTime, nullable=False)
    Tramiteredestino = db.Column(db.Integer, nullable=False)
    Usuario_idUsuario = db.Column(db.String(45), nullable=False)
    Estadodeltramite_idEstadodeltramite = db.Column(db.String(45), nullable=False)
    Tramitetipo_idTramitetipo = db.Column(db.String(45),nullable=False)
    def __init__(self, idTramite, Tramiteremitente, Tramiteasunto, Tramitefecha,Tramiteredestino,Usuario_idUsuario,Estadodeltramite_idEstadodeltramite,Tramitetipo_idTramitetipo):
        self.idTramite = idTramite
        self.Tramiteremitente = Tramiteremitente
        self.Tramiteasunto = Tramiteasunto
        self.Tramitefecha = Tramitefecha
        self.Tramiteredestino = Tramiteredestino
        self.Usuario_idUsuario = Usuario_idUsuario
        self.Estadodeltramite_idEstadodeltramite = Estadodeltramite_idEstadodeltramite
        self.Tramitetipo_idTramitetipo=Tramitetipo_idTramitetipo

db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("idUsuario", "UsuarioName", "UsuarioApellidos", "UsuarioContraseña","UsuarioDNI","Usuariosede","Usuariocorreo","Curso_idCurso")

usuario_schema = UsuarioSchema()
usuario_schemas = UsuarioSchema(many=True)

class cursoSchema(ma.Schema):
    class Meta:
        fields = ("idCurso", "Cursonombre", "Cursomodalidad")

curso_schema = cursoSchema()
curso_schemas = cursoSchema(many=True)

class TramiteTipoSchema(ma.Schema):
    class Meta:
        fields = ("idTramitetipo", "Nombretipo")

tramitetipo_schema = TramiteTipoSchema()
tramitetipo_schemas = TramiteTipoSchema(many=True)

class estadodeltramiteSchema(ma.Schema):
    class Meta:
        fields = ("idEstadodeltramite", "Fecha", "Asunto")

estadodeltramite_schema = estadodeltramiteSchema()
estadodeltramite_schemas = estadodeltramiteSchema(many=True)

class tramiteSchema(ma.Schema):
    class Meta:
        fields = ("idTramite","Tramiteremitente","Tramiteasunto","Tramitefecha","Tramiteredestino","Usuario_idUsuario","Estadodeltramite_idEstadodeltramite","Tramitetipo_idTramitetipo")

tramite_schema = tramiteSchema()
tramite_schemas = tramiteSchema(many=True)


@app.route('/create_curso',methods=['POST'])
def create_curso():
    print(request.json)
    idCurso=request.json["idCurso"]
    Cursonombre =request.json["Cursonombre"]
    Cursomodalidad =request.json["Cursomodalidad"]
    new_curso= curso(idCurso,Cursonombre,Cursomodalidad)
    db.session.add(new_curso)
    db.session.commit()

    return curso_schema.jsonify(new_curso)

@app.route('/read_curso',methods=['GET'])
def read_curso():
    all_curso = curso.query.all()
    result = curso_schemas.dump(all_curso)
    return jsonify(result)

@app.route('/delete_curso/<int:ide>', methods=['DELETE'])
def delete_curso(ide):
    deleteCurso=curso.query.filter_by(idCurso=ide).one()
    db.session.delete(deleteCurso)
    db.session.commit()
    return "eliminado correctamente"


@app.route('/create_usuario', methods=['POST'])
def create_cliente():
    print(request.json)
    idUsuario=request.json["idUsuario"]
    UsuarioName =request.json["UsuarioName"]
    UsuarioApellidos =request.json["UsuarioApellidos"]
    UsuarioContraseña = request.json["UsuarioContraseña"]
    UsuarioDNI = request.json["UsuarioDNI"]
    Usuariosede = request.json["Usuariosede"]
    Usuariocorreo = request.json["Usuariocorreo"]
    #Usuario_idCurso = request.json["Usuario_idCurso"]
    new_usuario = Usuario(idUsuario, UsuarioName, UsuarioApellidos, UsuarioContraseña,UsuarioDNI,Usuariosede,Usuariocorreo,1)

    db.session.add(new_usuario)
    db.session.commit()

    return usuario_schema.jsonify(new_usuario)

@app.route('/read_usuario',methods=['GET'])
def read_usuario():
    all_usuario = Usuario.query.all()
    result = usuario_schemas.dump(all_usuario)
    return jsonify(result)

@app.route('/read_usuario_es',methods=['POST'])
def read_usuario_es():
    name=request.form["user_name"]
    password=request.form["password"]
    try:
        only_usuario = Usuario.query.filter_by(UsuarioName=name,UsuarioContraseña=password).one()
    except:
        return ("Usuario o contraseña incorrecto")
    result = usuario_schema.dump(only_usuario)
    read_tramite=read_tramite2()
    return render_template('tramites.html', read_tramite=read_tramite)
        

@app.route('/delete_usuario/<int:ide>', methods=['DELETE'])
def delete_usuario(ide):
    delete_usuario=Usuario.query.filter_by(idUsuario=ide).one()
    db.session.delete(delete_usuario)
    db.session.commit()
    return "eliminado correctamente"

@app.route('/create_tramitetipo',methods=['POST'])
def create_tramitetipo():
    print(request.json)
    idTramitetipo=request.json["idTramitetipo"]
    Nombretipo =request.json["Nombretipo"]
    new_tramitetipo= tramitetipo(idTramitetipo,Nombretipo)
    db.session.add(new_tramitetipo)
    db.session.commit()
    return tramitetipo_schema.jsonify(new_tramitetipo)

@app.route('/read_tramitetipo',methods=['GET'])
def read_tramitetipo():
    all_tramitetipo = tramitetipo.query.all()
    result = tramitetipo_schemas.dump(all_tramitetipo)
    return jsonify(result)

@app.route('/delete_tramitetipo/<int:ide>', methods=['DELETE'])
def delete_tramitetipo(ide):
    delete_tramitetipo=tramitetipo.query.filter_by(idTramitetipo=ide).one()
    db.session.delete(delete_tramitetipo)
    db.session.commit()
    return "eliminado correctamente"

@app.route('/create_estadodeltramite',methods=['POST'])
def create_estadodeltramite():
    print(request.json)
    idEstadodeltramite=request.json["idEstadodeltramite"]
    Fecha =request.json["Fecha"]
    Asunto =request.json["Asunto"]
    new_estadodeltramite= estadodeltramite(idEstadodeltramite,Fecha,Asunto)
    db.session.add(new_estadodeltramite)
    db.session.commit()

    return estadodeltramite_schema.jsonify(new_estadodeltramite)

@app.route('/read_estadodeltramite',methods=['GET'])
def read_estadodeltramite():
    all_estadodeltramite = estadodeltramite.query.all()
    result = estadodeltramite_schemas.dump(all_estadodeltramite)
    return jsonify(result)

@app.route('/delete_estadodeltramite/<int:ide>', methods=['DELETE'])
def delete_estadodeltramite(ide):
    delete_tramite=tramite.query.filter_by(idTramite=ide).one()
    db.session.delete(delete_tramite)
    db.session.commit()
    return "eliminado correctamente"

@app.route('/create_tramite', methods=['POST'])
def create_tramite():
    print(request.json)
    idTramite=request.json["idTramite"]
    Tramiteremitente =request.json["Tramiteremitente"]
    Tramiteasunto =request.json["Tramiteasunto"]
    Tramitefecha = request.json["Tramitefecha"]
    Tramiteredestino = request.json["Tramiteredestino"]
    #Usuario_idUsuario = request.json["Usuario_idUsuario"]
    #Estadodeltramite_idEstadodeltramite = request.json["Estadodeltramite_idEstadodeltramite"]
    #Tramitetipo_idTramitetipo = request.json["Tramitetipo_idTramitetipo"]
    new_tramite = tramite(idTramite, Tramiteremitente, Tramiteasunto, Tramitefecha, Tramiteredestino,1,1,1)

    db.session.add(new_tramite)
    db.session.commit()

    return tramite_schema.jsonify(new_tramite)

def read_tramite2():
    all_tramite = tramite.query.all()
    result = tramite_schemas.dump(all_tramite)
    return result

@app.route('/read_tramite',methods=['GET'])
def read_tramite():
    all_tramite = tramite.query.all()
    result = tramite_schemas.dump(all_tramite)
    return jsonify(result)

@app.route('/delete_tramite/<int:ide>', methods=['POST'])
def delete_tramite(ide):
    delete_tramite=tramite.query.filter_by(idTramite=ide).one()
    db.session.delete(delete_tramite)
    db.session.commit()
    return "eliminado correctamente"

@app.route('/update_tramite/<ide>', methods=["POST"])
def update_tramite(ide):
    name=request.json["name"]
    fecha=request.json["fecha"]
    destino=request.json["destino"]
    asunto=request.json["asunto"]

    tramite.query.filter_by(idTramite=ide).update(dict(
        Tramiteremitente=name,
        Tramitefecha=fecha,
        Tramiteredestino=destino,
        Tramiteasunto=asunto
    ))
    db.session.commit()
    return "actualizacion correcta"


@app.route('/')
def home() :
   return render_template('login.html')

#print ("Holis")
if __name__=="__main__":   
    app.run(port=5000, debug=True)