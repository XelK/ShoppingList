from pymongo import MongoClient


class Crud:
    """
    implement CRUD functions
    """

    def resp(self, code, msg):
        return {
            "Code": code,
            "Msg": msg
        }

    def __init__(self, url: str):
        self.client = MongoClient(url)
        self.db = self.client.products

    def create(self, product):
        if self.db.products.find_one({"name": product['name']}):
            return self.resp("ERROR", f"Object {product['name']} ALREADY PRESENT!")
        result = self.db.products.insert_one(product)
        if result:
            return self.resp("OK", f"Object {product['name']} INSERTED")
        return result

    def extract_params(self, params):
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

    def retrieve(self, product=None):
        query = self.extract_params(product)
        result = self.db.products.find(query, {"_id": False})
        if result:
            return self.resp("OK", list(result))
        return self.resp("ERROR", f"Object {product['name']} NOT FOUND")

    #    def update(self, product):
    #        result = self.db.products.update_one({"name": product['name']}, {"$set": product})
    #        if result.modified_count:
    #            return self.resp("OK", f"Object {product['name']} UPDATED")
    #        return self.resp("ERROR", f"Object {product['name']} NOT FOUND")

    def update(self, product_from, product_to):
        result = self.db.products.update_one({"name": product_from['name']}, {"$set": product_to})
        if result.modified_count:
            return self.resp("OK", f"Object {product_from['name']} UPDATED")
        return self.resp("ERROR", f"Object {product_from['name']} NOT FOUND")

    def delete(self, product):
        result = self.db.products.find_one_and_delete(product)
        if result:
            return self.resp("OK", f"Object {product['name']} DELETED")
        return self.resp("ERROR", f"Object {product['name']} NOT FOUND")
