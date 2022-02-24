from app import db
from app import ma


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __init__(self, name, description, price, qty, category_id, user_id):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty
        self.category_id = category_id
        self.user_id = user_id

    def __repr__(self):
        return '<Product {}>'.format(self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    products = db.relationship('Product', backref='category')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='user')

    def __repr__(self):
            return '<User {}>'.format(self.username)



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty', 'category_id', 'user_id')


class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

