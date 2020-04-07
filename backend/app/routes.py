from app.models import Usuario, Produto, Fornecedor, UnidadeMedida
from app import app, db
from flask import request, abort, redirect, jsonify, send_file, make_response
from flask_jwt import jwt_required, current_identity
import json

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(silent=True)

    if "username" not in data:
        return abort(400)
    if "password" not in data:
        return abort(400)

    username = data["username"]
    password = data["password"]

    try:
        # Verifica usuário
        user = Usuario.query.filter_by(username=username).first()
        if user is not None:
            return jsonify({"status": 404, "msg": "Usuário não disponível"})

        # Cria usuário e brinquedo
        user = Usuario(username=username)
        user.set_password(password)        
        db.session.add(user)
        db.session.commit()

        return jsonify({"status": 200})
    except Exception as e:
        print(e)
        return abort(500)


@app.route('/produtos', methods=['GET', 'POST'])
@jwt_required()
def produtos():
    if request.method == 'GET':
        produtos = Produto.query.all()
        response = []
        if produtos:
            response.append([prod.to_json() for prod in produtos])
            return jsonify(response)
        else:
            return jsonify(response), 304
    else:
        return abort(404)

@app.route('/fornecedores', methods=['GET', 'POST'])
@jwt_required()
def fornecedores():
    if request.method == 'GET':
        fornecedores = Fornecedor.query.all()
        response = []
        if fornecedores:
            response = [fornecedor.to_json() for fornecedor in fornecedores]
            return jsonify(response)
        else:
            return jsonify(response), 304
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        
        if "deletedId" in data:
            deletedId = data["deletedId"]
            
            fornecedor = Fornecedor.query.get(deletedId)
            
            if fornecedor is None:
                return jsonify({"status": 404, "msg": "Fornecedor não encontrado"})

            db.session.delete(fornecedor)
            db.session.commit()

            return jsonify({"status": 200})

        if "cnpj" not in data:
            return abort(400)
        if "nome" not in data:
            return abort(400)

        cnpj = data["cnpj"]
        nome = data["nome"]

        fornecedor = Fornecedor.query.filter_by(cnpj=abreviacao).first()
        
        if fornecedor is not None:
            fornecedor.cnpj = cnpj
            fornecedor.nome = nome
            db.session.commit()
            return jsonify({"status": 200})

        fornecedor = Fornecedor(cnpj=cnpj, nome=nome)
        db.session.add(fornecedor)
        db.session.commit()

        return jsonify({"status": 200})

@app.route('/unidade-medida', methods=['GET', 'POST'])
@jwt_required()
def unidade_medida():
    if request.method == 'GET':
        unidades = UnidadeMedida.query.all()
        response = []
        if unidades:
            response = [un.to_json() for un in unidades]
            return jsonify(response)
        else:
            return jsonify(response), 304
    elif request.method == 'POST':
        data = request.get_json(silent=True)

        if "deletedId" in data:
            deletedId = data["deletedId"]
            
            unidade = UnidadeMedida.query.get(deletedId)
            
            if unidade is None:
                return jsonify({"status": 404, "msg": "Unidade de medida não encontrada"})

            db.session.delete(unidade)
            db.session.commit()

            return jsonify({"status": 200})

        if "abreviacao" not in data:
            return abort(400)
        if "descricao" not in data:
            return abort(400)
        if "fracionavel" not in data:
            return abort(400)

        abreviacao = data["abreviacao"]
        descricao = data["descricao"]
        fracionavel = data["fracionavel"]

        unidade = UnidadeMedida.query.filter_by(abreviacao=abreviacao, descricao=descricao).first()
        
        if unidade is not None:
            unidade.abreviacao = abreviacao
            unidade.descricao = descricao
            unidade.fracionavel = fracionavel
            db.session.commit()
            return jsonify({"status": 200})

        unidade = UnidadeMedida(abreviacao=abreviacao, descricao=descricao, fracionavel=fracionavel)
        db.session.add(unidade)
        db.session.commit()

        return jsonify({"status": 200})
    else:
        return abort(404)