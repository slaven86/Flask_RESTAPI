from flask import request, jsonify
from app import db, app
from app.models import Category, CategorySchema, Product, ProductSchema, User
from flask_jwt_extended import jwt_required, get_jwt_identity

@app.errorhandler(code_or_exception=404)
def handle_404(e):
    return jsonify({'Error': 'Not found'})


#CRUD OPERACIJA ZA TABELU PRODUCT
@app.route('/product', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()

    if user:
        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']
        category_id = request.json['category_id']
        user_id = user.id

        new_product = Product(name=name, description=description, price=price, qty=qty,
                              category_id=category_id, user_id=user_id)
        db.session.add(new_product)
        db.session.commit()
        product_schema = ProductSchema()
        return product_schema.jsonify(new_product)

@app.route('/product', methods=['GET'])
@jwt_required()
def get_products():

    all_products = Product.query.all()
    products_schema = ProductSchema(many=True)
    result = products_schema.dump(all_products)
    return jsonify(result)


@app.route('/product/<int:id>', methods=['GET'])
@jwt_required()
def get_one_product(id):
        current_user = get_jwt_identity()
        single_product = Product.query.filter_by(user_id=current_user, id=id).first()

        if single_product:
            product_schema = ProductSchema()
            return product_schema.jsonify(single_product)

        return jsonify({"Error": "Only owner can see this product!"})



@app.route('/product/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()

    if user:
        product = Product.query.filter_by(user_id=current_user, id=id).first()
        name = request.json['name']
        description = request.json['description']
        price = request.json['price']
        qty = request.json['qty']
        category_id = request.json['category_id']
        user_id = user.id

        product.name = name
        product.description = description
        product.price = price
        product.qty = qty
        product.category_id = category_id
        product.user_id = user.id

        db.session.commit()
        product_schema = ProductSchema()
        return product_schema.jsonify(product)



@app.route('/product/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    current_user = get_jwt_identity()
    if current_user:
        product = Product.query.filter_by(user_id=current_user, id=id).first()
        db.session.delete(product)
        db.session.commit()

        product_schema = ProductSchema()
        return product_schema.jsonify(product)


# ISPIS KATEGORIJA
@app.route('/category')
def get_all_categories():
    all_cat = Category.query.all()
    products_schema = CategorySchema(many=True)
    result = products_schema.dump(all_cat)
    return jsonify(result)


