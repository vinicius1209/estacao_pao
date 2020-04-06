from app.models import Usuario
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
    return "produtos: {}".format(current_identity)