from app import db, app
from flask import request, jsonify
from app.models import User, ProductSchema, UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import validators


# ISPIS SVIH USERA
@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(all_users)
    return jsonify(result)


# REGISTER_NEW_USER
@app.route('/register', methods=['POST'])
def register_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    # VALIDACIJA
    if len(password) < 6:
        return jsonify({'Error': 'Password is too short!'})

    if not username.isalnum() or " " in username:
        return jsonify({'Error': 'Username must be alphanumeric, also no spaces!'})

    if not validators.email(email):
        return jsonify({"Error": "Email is not valid"})

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"Error": "Email already exist!"})

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"Error": "Username already exist!"})

    hashed_pass = generate_password_hash(password, method='sha256')

    new_user = User(username=username, email=email, password=hashed_pass)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!',
                    'User': username,
                    'Email': email,
                    'password': hashed_pass})


# LOGIN WITH JWT
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            access = create_access_token(identity=user.id)

            return jsonify({'User': {
                'access': access,
                'username': user.username,
                'email': user.email
            }
            })
    return jsonify({"Error": "Wrong credentials!"})


@app.route('/user/<int:id>', methods=['GET'])
@jwt_required()
def user_log(id):
    single_user = User.query.get(id)
    all_products = single_user.products
    products_schema = ProductSchema(many=True)
    result = products_schema.dump(all_products)

    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user).first()
    if single_user == user:
        return jsonify({'username': user.username, 'email': user.email,
                        'All products': result})

    return jsonify({"Error": "Wrong credentials!"})
