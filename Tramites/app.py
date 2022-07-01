from flask import Flask, render_template, request, redirect, url_for, flash
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask,request,jsonify
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@127.0.0.1/mydb'
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

@app.route('/create_curso',methods=['post'])
def create_curso():
    print(request.json)
    idCurso=request.json["idCurso"]
    Cursonombre =request.json["Cursonombre"]
    Cursomodalidad =request.json["Cursomodalidad"]
    new_curso= Curso(idCurso,Cursonombre,Cursomodalidad)
    db.session.add(new_curso)
    db.session.commit()

    return curso_schema.jsonify(new_curso)

@app.route('/read_curso',methods=['get'])
def read_curso():
    all_curso = Curso.query.all()
    result = curso_schemas.dump(all_curso)
    return jsonify(result)

@app.route('/delete_curso/<int:ide>', methods=['DELETE'])
def delete_curso(ide):
    deleteCurso=Curso.query.filter_by(idCurso=ide).one()
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
def read_curso():
    all_curso = Curso.query.all()
    result = curso_schemas.dump(all_curso)
    return jsonify(result)

@app.route('/delete_usuario/<ide:int>', methods=['POST'])
def delete_usuario(ide):
    deleteUsuario=Curso.query.filter_by(idUsuario=ide).one()
    db.session.delete(deleteUsuario)
    db.session.commit()
    return "eliminado correctamente"


if __name__=="__main__":   
    app.run(port=5000, debug=True)