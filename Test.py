from CRUD import Crud
from Product import Product

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
