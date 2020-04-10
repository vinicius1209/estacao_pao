from . import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
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
    cod_venda = db.Column(db.Integer, index=True, unique=True)
    preco_compra = db.Column(db.String(45), nullable=False)
    preco_venda = db.Column(db.String(45), nullable=False)
    qtd_estoque = db.Column(db.String(45), nullable=False)
    qtd_min = db.Column(db.String(45))
    ativado = db.Column(db.Boolean, unique=False, default=True)
    unidade_id = db.Column(db.Integer, db.ForeignKey('unidade_medida.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)
    unidade = db.relationship('UnidadeMedida')
    categoria = db.relationship('Categoria')
    fornecedor = db.relationship('Fornecedor')

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cod_venda": self.cod_venda,
            "preco_compra": self.preco_compra,
            "preco_venda": self.preco_venda,
            "qtd_estoque": self.qtd_estoque,
            "qtd_min": self.qtd_min,
            "ativado": self.ativado,
            "unidade": self.unidade.to_json(),
            "categoria": self.categoria.to_json(),
            "fornecedor": self.fornecedor.to_json()
        }


class Entrada(db.Model):
    __tablename__ = 'entrada'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario')


class EntradaProduto(db.Model):
    __tablename__ = 'entrada_produto'
    id = db.Column(db.Integer, primary_key=True)
    entrada_id = db.Column(db.Integer, db.ForeignKey('entrada.id'), nullable=False)
    qtd_entrada = db.Column(db.Integer, nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    entrada = db.relationship('Entrada')
    produto = db.relationship('Produto')

    def to_json(self):
        return {
            "id": self.id,
            "qtd_entrada": self.qtd_entrada,
            "produto": self.produto.to_json(),
            "entrada": self.entrada.to_json()
        }



class VendaProduto(db.Model):
    __tablename__ = 'venda_produto'
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('venda.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), nullable=False)
    venda = db.relationship('Venda')
    produto = db.relationship('Produto')

class Venda(db.Model):
    __tablename__ = 'venda'
    id = db.Column(db.Integer, primary_key=True)
    valor_total = db.Column(db.Float(precision=10), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pagamento_id = db.Column(db.Integer, db.ForeignKey('pagamento.id'), nullable=False)
    vendedor = db.relationship('Usuario')
    pagamento = db.relationship('Pagamento')


class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    id = db.Column(db.Integer, primary_key=True)
    forma_pagamento = db.Column(db.String(45), nullable=False)


class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "nome": self.nome
        }


class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'
    id = db.Column(db.Integer, primary_key=True)
    cnpj = db.Column(db.String(45), nullable=False)
    nome = db.Column(db.String(45), nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "cnpj": self.cnpj,
            "nome": self.nome
        }

class UnidadeMedida(db.Model):
    __tablename__ = 'unidade_medida'
    id = db.Column(db.Integer, primary_key=True)
    abreviacao = db.Column(db.String(3), nullable=False)
    descricao = db.Column(db.String(45), nullable=False)
    fracionavel = db.Column(db.Boolean, unique=False, default=False)

    def to_json(self):
        return {
            "id": self.id,
            "abreviacao": self.abreviacao,
            "descricao": self.descricao,
            "fracionavel": self.fracionavel
        }


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    acao = db.Column(db.String(1), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

