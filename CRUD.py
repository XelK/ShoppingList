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

    def retrieve(self, product):
        result = self.db.products.find_one(product)
        if result:
            return self.resp("OK", f'"name":{result["name"]},'
                                   f'"quantity":{result["quantity"]},'
                                   f'"description":{result["description"]}')
        return self.resp("ERROR", f"Object {product['name']} NOT FOUND")

    def update(self, product):
        result = self.db.products.update_one({"name": product['name']}, {"$set": product})
        if result.modified_count:
            return self.resp("OK", f"Object {product['name']} UPDATED")
        return self.resp("ERROR", f"Object {product['name']} NOT FOUND")

    def delete(self, product):
        result = self.db.products.find_one_and_delete({"name": product['name']})
        if result:
            return self.resp("OK", f"Object {product['name']} DELETED")
        return self.resp("ERROR", f"Object {product['name']} NOT FOUND")
