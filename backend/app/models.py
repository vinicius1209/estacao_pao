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
    preco = db.Column(db.Float(precision=10))
    qtd_estoque = db.Column(db.String(45))
    qtd_min = db.Column(db.String(45))
    ativado = db.Column(db.Boolean, unique=False, default=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade_medida.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'), nullable=False)
    unidade = db.relationship('UnidadeMedida')
    categoria = db.relationship('Categorias')
    fornecedores = db.relationship('Fornecedores')

class Categorias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)

class Fornecedores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(45), nullable=False)
    nome = db.Column(db.String(45), nullable=False)

class UnidadeMedida(db.Model):
    __tablename__ = 'unidade_medida'
    id = db.Column(db.Integer, primary_key=True)
    abreviacao = db.Column(db.String(3), nullable=False)
    descricao = db.Column(db.String(45), nullable=False)
    fracionavel = db.Column(db.Boolean, unique=False, default=False)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
