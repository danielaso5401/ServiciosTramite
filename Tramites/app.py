from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from functools import wraps
from flask.helpers import send_file
from flask_mail import Connection, Mail, Message
from flask import Flask, render_template, request, session, escape, redirect, url_for, flash
import os
from flask import Flask,request,redirect,url_for,make_response,jsonify


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Curso(db.Model):
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

db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("idCurso", "UsuarioName", "UsuarioApellidos", "UsuarioContraseña","UsuarioDNI","Usuariosede","Usuariocorreo","Curso_idCurso")

usuario_schema = UsuarioSchema()
usuario_schemas = UsuarioSchema(many=True)

class CursoSchema(ma.Schema):
    class Meta:
        fields = ("idCurso", "Cursonombre", "Cursomodalidad")

curso_schema = CursoSchema()
curso_schemas = CursoSchema(many=True)

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


@app.route('/create_curso',methods=['POST'])
def create_curso():
    print(request.json)
    idCurso=request.json["idCurso"]
    Cursonombre =request.json["Cursonombre"]
    Cursomodalidad =request.json["Cursomodalidad"]
    new_curso= Curso(idCurso,Cursonombre,Cursomodalidad)
    db.session.add(new_curso)
    db.session.commit()

    return curso_schema.jsonify(new_curso)

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

@app.route('/create_tramitetipo',methods=['POST'])
def create_tramitetipo():
    print(request.json)
    idTramitetipo=request.json["idTramitetipo"]
    Nombretipo =request.json["Nombretipo"]
    new_tramitetipo= tramitetipo(idTramitetipo,Nombretipo)
    db.session.add(new_tramitetipo)
    db.session.commit()

    return tramitetipo_schema.jsonify(new_tramitetipo)

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


if __name__=="__main__":   
    app.run(port=5000, debug=True)