from CRUD import Crud


class Product:
    def __init__(self, name, quantity, description=None):
        self.description = description
        self.quantity = quantity
        self.name = name

    def __dict__(self):
        return {
            "name": self.name,
            "quantity": self.quantity,
            "description": self.description
        }


db = Crud("mongodb://docker02.xelk.me:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")

p1 = Product("salame", 2, "ottimo salame")
p2 = Product("mortadella", 10)
p3 = Product("pane", 5)

# print(p1.__dict__())
print(db.create(p1.__dict__()))
print(db.create(p2.__dict__()))

# print(db.delete(p1.__dict__()))

print(db.retrieve(p1.__dict__()))
print(db.retrieve(p2.__dict__()))
print(db.retrieve(p3.__dict__()))

print(db.create(p3.__dict__()))
p3.quantity = 20
# print(db.update(p3.__dict__()))

# print(db.delete(p3.__dict__()))


import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def home():
    return "<h1>LISTA DELLA SPESA</h1>"


@app.route("/api/products", methods=['GET'])
def search_one():
    products = request.args
    print(products)
    result = db.retrieve(products)
    if result['Code'] == 'OK':
        return jsonify(result['Msg'])
    return result


@app.route("/api/products", methods=['POST'])
def create():
    req_json = request.json
    if not req_json:
        return error(404)
    product = {
        "name": req_json['name'],
        "quantity": req_json['quantity'],
        "description": req_json['description']
    }
    result = db.create(product)
    return result


@app.route("/api/products", methods=['PUT'])
def update():
    req_json = request.json
    print("cane: ", req_json)
    if not req_json:
        return error(404)
    product_from = {
        "name": req_json[0]['name'],
        "quantity": req_json[0]['quantity'],
        "description": req_json[0]['description']
    }
    product_to = {
        "name": req_json[1]['name'],
        "quantity": req_json[1]['quantity'],
        "description": req_json[1]['description']
    }
    result = db.update(product_from, product_to)
    return result


@app.route('/api/products', methods=['DELETE'])
def delete():
    params = request.json
    query = {}
    query['name'] = params.get('name')
    query['quantity'] = params.get('quantity')
    query['description'] = params.get('description')
    print(query)
    result = db.delete(query)
    return result


@app.errorhandler(404)
def error(e):
    return "<h1>404</h1><p>Impossibile trovare " \
           "la risorsa desiderata.</p>", 404


app.run()
