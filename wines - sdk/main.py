from flask import jsonify, request
import pyrebase
from time import time
import pandas as pd
import matplotlib.pyplot as plt

config = {
    "apiKey": "AIzaSyA-oHM215fOdRvGnj1CnZih8WulHWzMuBU",
    "authDomain": "wines-1ebb1.firebaseapp.com",
    "databaseURL": "https://wines-1ebb1.firebaseio.com",
    "projectId": "wines-1ebb1",
    "storageBucket": "wines-1ebb1.appspot.com",
    "messagingSenderId": "387958068625",
    "appId": "1:387958068625:web:de23eb9805ba480d57f630",
    "measurementId": "G-BZ00KD04EV"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

def addimagem(nome):
    try:
        dir = "C:/Users/Denise_/Downloads/" + nome
        tmp = int(time())
        storage.child("images/{}.png".format(tmp)).put(dir)
        return "Imagem {} inserida com sucesso.".format(tmp), 200
    except:
        return "Não foi possível inserir a imagem", 500

def consultar_points():
    try:
        todos = db.child("wines_sem_id").get()
        df = pd.DataFrame(todos.val())
        df = df.T
        df['points'] = df['points'].astype(int)
        df = df.sort_values(by=['points'], ascending=True)
        df = df.head(15)
        
        return df.to_json(orient='records'), 200
    except:
        return "Não foi possível consultar os dados", 500

def consultar_province(province):
    try:
        todos = db.child("wines_sem_id").get()
        df = pd.DataFrame(todos.val())
        df = df.T
        df = df.loc[df['province'] == province]
        return df.to_json(orient='records'), 200
    except:
        return "Não foi possível consultar os dados", 500

def deletar_no(no):
    try:
        db.child("wines_sem_id").child(int(no)).remove()
        return "Nó {} deletado com sucesso!".format(no), 200
    except:
        return "O nó não foi informado no dado recebido.", 400

def atualizar_no(no, request):
    post_args = request.json
    try:
        if "country" in post_args:
            db.child("wines_sem_id").child(int(no)).update({"country":post_args["country"]})
        if "description" in post_args:
            db.child("wines_sem_id").child(int(no)).update({"description":post_args["description"]})
        if "designation" in post_args:
            db.child("wines_sem_id").child(int(no)).update({"designation":post_args["designation"]})
        return "Nó atualizado com sucesso!", 200
    except:
        return "O nó não foi informado no dado recebido.", 400

def wines(request):
    req = request.path.split('/')
    if request.method == 'DELETE' and req[2] is not None:
        return deletar_no(req[2])
    if request.method == 'PUT' and req[2] is not None:
        return atualizar_no(req[2], request)
    if request.method == 'GET':
        if "points" in request.path:
            return consultar_points()
        elif "province" in request.path and req[2] is not None:
            return consultar_province(req[2])
        elif "addimagem" in request.path and req[2] is not None:
            return addimagem(req[2])
    else:
        return 'Método não suportado.', 400