from pymongo import MongoClient


def resp(code, msg):
    return {
        "Code": code,
        "Msg": msg
    }


def extract_params(params):
    name = params.get("name")
    quantity = params.get("quantity")
    description = params.get("description")
    query = {}
    if name:
        query['name'] = name
    if quantity:
        query['quantity'] = int(quantity)
    if description:
        query['description'] = description
    return query


class Crud:
    """
    implement CRUD functions
    """

    def __init__(self, url: str):
        self.client = MongoClient(url)
        self.db = self.client.products

    def create(self, product):
        if self.db.products.find_one({"name": product['name']}):
            return resp("ERROR", f"Object {product['name']} ALREADY PRESENT!")
        result = self.db.products.insert_one(product)
        if result:
            return resp("OK", f"Object {product['name']} INSERTED")
        return result

    def retrieve(self, product=None):
        query = extract_params(product)
        result = self.db.products.find(query, {"_id": False})
        if result:
            return resp("OK", list(result))
        return resp("ERROR", f"Object {product['name']} NOT FOUND")

    def update(self, product_from, product_to):
        result = self.db.products.update_one({"name": product_from['name']}, {"$set": product_to})
        if result.modified_count:
            return resp("OK", f"Object {product_from['name']} UPDATED")
        return resp("ERROR", f"Object {product_from['name']} NOT FOUND")

    def delete(self, product):
        result = self.db.products.find_one_and_delete(product)
        if result:
            return resp("OK", f"Object {product['name']} DELETED")
        return resp("ERROR", f"Object {product['name']} NOT FOUND")
