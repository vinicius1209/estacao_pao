from app.models import User
from app import app
from flask import request, abort, redirect, jsonify, send_file, make_response
import json

@app.route('/produtos', methods=['GET', 'POST'])
def produtos():
    return "produtos"