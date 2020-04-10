from app.models import Usuario, Produto, Entrada, EntradaProduto, Fornecedor, UnidadeMedida, Categoria
from app import app, db
from sqlalchemy import or_, desc
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
            response = [prod.to_json() for prod in produtos]
            return jsonify(response)
        else:
            return jsonify(response), 304
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        
        # Removendo
        if "deletedId" in data:
            deletedId = data["deletedId"]
            produto = Produto.query.get(deletedId)
            
            if produto is None:
                return jsonify({"status": 404, "msg": "Produto não encontrado"})

            db.session.delete(produto)
            db.session.commit()
            return jsonify({"status": 200})
        
        if "id" not in data:
            return abort(400)
        if "nome" not in data:
            return abort(400)
        if "cod_venda" not in data:
            return abort(400)
        if "preco_compra" not in data:
            return abort(400)
        if "preco_venda" not in data:
            return abort(400)            
        if "ativado" not in data:
            return abort(400)
        if "qtd_min" not in data:
            return abort(400)     
        if "unidade" not in data:
            return abort(400)
        if "categoria" not in data:
            return abort(400)
        if "fornecedor" not in data:
            return abort(400)       

        produto_id = data["id"]
        nome = data["nome"]
        cod_venda = data["cod_venda"]
        preco_compra = data["preco_compra"]
        preco_venda = data["preco_venda"]
        ativado = data["ativado"]
        qtd_min = data["qtd_min"]
        unidade = data["unidade"]
        categoria= data["categoria"]
        fornecedor = data["fornecedor"]

        # Editando
        if produto_id != '':
            produto = Produto.query.get(produto_id)
            if produto is not None:
                produto.cod_venda = cod_venda
                produto.nome = nome
                produto.preco_compra = preco_compra
                produto.preco_venda = preco_venda
                produto.ativado = ativado
                produto.qtd_min = qtd_min
                produto.unidade_id = unidade["id"]
                produto.categoria_id = categoria["id"]
                produto.fornecedor_id = fornecedor["id"]

                db.session.commit()
                return jsonify({"status": 200, "msg": "Produto editado com sucesso"})
        
        # Inserindo
        produto = Produto.query.filter(or_(Produto.nome==nome, Produto.cod_venda==cod_venda)).first()
        if produto is not None:
            return jsonify({"status": 404, "msg": "Produto já cadastrado"})

        produto = Produto(
            nome=nome, cod_venda=cod_venda, preco_compra=preco_compra, preco_venda=preco_venda, 
            qtd_min=qtd_min, unidade_id=unidade["id"],
            fornecedor_id=fornecedor["id"], categoria_id=categoria["id"], qtd_estoque=0
        )

        db.session.add(produto)
        db.session.commit()
        return jsonify({"status": 200, "msg": "Produto cadastrado com sucesso"})

    else:
        return abort(404)

@app.route('/entradas', methods=['GET', 'POST'])
@jwt_required()
def entradas():
    if request.method == 'GET':
        entradas = Entrada.query.all()
        response = []
        if entradas:
            for entrada in entradas:
                entrada_produto = EntradaProduto.query.filter_by(entrada_id=entrada.id).all()
                response.append(registro.to_json() for registro in entrada_produto)
            return jsonify(response)
        else:
            return jsonify(response), 304
    elif request.method == 'POST':
        data = request.get_json(silent=True)

        usuario_id = current_identity.id
        if "produtos" not in data:
            return abort(400)


    else:
        return abort(404)


@app.route('/categorias', methods=['GET', 'POST'])
@jwt_required()
def categorias():
    if request.method == 'GET':
        categorias = Categoria.query.all()
        response = []
        if categorias:
            response = [cat.to_json() for cat in categorias]
            return jsonify(response)
        else:
            return jsonify(response), 304
    elif request.method == 'POST':
        data = request.get_json(silent=True)
        
        # Removendo
        if "deletedId" in data:
            deletedId = data["deletedId"]
            categoria = Categoria.query.get(deletedId)
            
            if categoria is None:
                return jsonify({"status": 404, "msg": "Categoria não encontrada"})

            db.session.delete(categoria)
            db.session.commit()
            return jsonify({"status": 200, "msg": "Categoria removida com sucesso"})

        if "id" not in data:
            return abort(400)
        if "nome" not in data:
            return abort(400)

        categoria_id = data["id"]
        nome = data["nome"]

        # Editando
        if categoria_id != '':
            categoria = Categoria.query.get(categoria_id)
            if categoria is not None:
                categoria.nome = nome
                db.session.commit()
                return jsonify({"status": 200, "msg": "Categoria editada com sucesso"})
        
        # Inserindo
        categoria = Categoria.query.filter(or_(Categoria.nome==nome)).first()
        if categoria is not None:
            return jsonify({"status": 404, "msg": "Categoria já cadastrada"})

        categoria = Categoria(nome=nome)
        db.session.add(categoria)
        db.session.commit()

        return jsonify({"status": 200, "msg": "Categoria inserida com sucesso"})
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

            return jsonify({"status": 200, "msg": "Fornecedor removido com sucesso"})

        if "id" not in data:
            return abort(400)
        if "cnpj" not in data:
            return abort(400)
        if "nome" not in data:
            return abort(400)

        fornecedor_id = data["id"]
        cnpj = data["cnpj"]
        nome = data["nome"]

        # Editando
        if fornecedor_id != '':
            fornecedor = Fornecedor.query.get(fornecedor_id)
            if fornecedor is not None:
                fornecedor.cnpj = cnpj
                fornecedor.nome = nome
                db.session.commit()
                return jsonify({"status": 200, "msg": "Fornecedor editado com sucesso"})

        # Inserindo
        fornecedor = Fornecedor.query.filter(or_(Fornecedor.cnpj==cnpj, Fornecedor.nome==nome)).first()
        if fornecedor is not None:
            return jsonify({"status": 404, "msg": "Fornecedor já cadastrado"})

        fornecedor = Fornecedor(cnpj=cnpj, nome=nome)
        db.session.add(fornecedor)
        db.session.commit()

        return jsonify({"status": 200, "msg": "Fornecedor cadastrado com sucesso"})
    else:
        return abort(404)

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

        # Removendo
        if "deletedId" in data:
            deletedId = data["deletedId"]
            unidade = UnidadeMedida.query.get(deletedId)
            
            if unidade is None:
                return jsonify({"status": 404, "msg": "Unidade de Medida não encontrada"})

            db.session.delete(unidade)
            db.session.commit()

            return jsonify({"status": 200, "msg": "Unidade de Medida removida com sucesso"})
        
        if "id" not in data:
            return abort(400)
        if "abreviacao" not in data:
            return abort(400)
        if "descricao" not in data:
            return abort(400)
        if "fracionavel" not in data:
            return abort(400)

        unidade_id = data["id"]
        abreviacao = data["abreviacao"]
        descricao = data["descricao"]
        fracionavel = data["fracionavel"]

        # Editando
        if unidade_id != '':
            unidade = UnidadeMedida.query.get(unidade_id)
            if unidade is not None:
                unidade.abreviacao = abreviacao
                unidade.descricao = descricao
                unidade.fracionavel = fracionavel
                db.session.commit()
                return jsonify({"status": 200, "msg": "Unidade de Medida editada com sucesso"})
        
        #Inserindo
        unidade = UnidadeMedida.query.filter(or_(UnidadeMedida.abreviacao==abreviacao, UnidadeMedida.descricao==descricao)).first()
        if unidade is not None:
            return jsonify({"status": 404, "msg": "Unidade de Medida já cadastrada"})
        else:
            unidade = UnidadeMedida(abreviacao=abreviacao, descricao=descricao, fracionavel=fracionavel)
            db.session.add(unidade)
            db.session.commit()
            db.session.commit()

            return jsonify({"status": 200, "msg": "Unidade de Medida cadastrada com sucesso"})
    else:
        return abort(404)
    
