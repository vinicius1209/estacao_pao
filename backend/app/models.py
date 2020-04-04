from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), index=True, unique=True)
    preco = db.Column(db.Float(precision=10, scale=2))
    qtd_estoque = db.Column(db.String(45))
    categoria = db.relationship('Categorias')
    fornecedores = db.relationship('Fornecedores')

class Categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=True)

class Fornecedores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(45), nullable=True)
    nome = db.Column(db.String(45), nullable=True)