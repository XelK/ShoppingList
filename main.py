import flask
from flask import request, jsonify

from CRUD import Crud

app = flask.Flask(__name__)
app.config['DEBUG'] = True

db = Crud("mongodb://docker02.xelk.me:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")


def prod_extract(req_json):
    product = {
        "name": req_json['name'],
        "quantity": req_json['quantity'],
        "description": req_json['description']
    }
    return product


@app.route("/", methods=['GET'])
def home():
    return "<h1>LISTA DELLA SPESA</h1>"


@app.route("/api/products", methods=['GET'])
def search_one():
    products = request.args
    result = db.retrieve(products)
    if result['Code'] == 'OK':
        return jsonify(result['Msg'])
    return result


@app.route("/api/products", methods=['POST'])
def create():
    req_json = request.json
    if not req_json:
        return error(404)
    product = prod_extract(req_json)
    result = db.create(product)
    return result


@app.route("/api/products", methods=['PUT'])
def update():
    req_json = request.json
    if not req_json:
        return error(404)
    product_from = prod_extract(req_json[0])
    product_to = prod_extract(req_json[1])
    result = db.update(product_from, product_to)
    return result


@app.route('/api/products', methods=['DELETE'])
def delete():
    params = request.json
    query = prod_extract(params)
    result = db.delete(query)
    return result


@app.errorhandler(404)
def error():
    return "<h1>404</h1><p>Impossibile trovare " \
           "la risorsa desiderata.</p>", 404


app.run()
