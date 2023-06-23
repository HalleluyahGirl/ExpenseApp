from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/reminder_expense_app'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
mongo = PyMongo(app)
jwt = JWTManager(app)

# User Registration
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    existing_user = mongo.db.users.find_one({'email': data['email']})
    if existing_user:
        return jsonify(message='Email already exists'), 409
    data['password'] = generate_password_hash(data['password'])  # Use a secure password hashing library
    mongo.db.users.insert_one(data)
    return jsonify(message='User registered'), 201

# User Login
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data['email']})
    if not user or not check_password_hash(user['password'], data['password']):  # Use the appropriate password verification method
        return jsonify(message='Invalid credentials'), 401
    token = create_access_token(identity=str(user['_id']))
    return jsonify(token=token), 200

# Reminder Creation
@app.route('/reminders', methods=['POST'])
@jwt_required()
def create_reminder():
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    mongo.db.reminders.insert_one(data)
    return jsonify(message='Reminder created'), 201

# Update Reminder
@app.route('/reminders/<reminder_id>', methods=['PUT'])
@jwt_required()
def update_reminder(reminder_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    reminder = mongo.db.reminders.find_one({'_id': reminder_id, 'user_id': user_id})
    if not reminder:
        return jsonify(message='Reminder not found'), 404
    mongo.db.reminders.update_one({'_id': reminder_id}, {'$set': data})
    return jsonify(message='Reminder updated'), 200

# Delete Reminder
@app.route('/reminders/<reminder_id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(reminder_id):
    user_id = get_jwt_identity()
    reminder = mongo.db.reminders.find_one({'_id': reminder_id, 'user_id': user_id})
    if not reminder:
        return jsonify(message='Reminder not found'), 404
    mongo.db.reminders.delete_one({'_id': reminder_id})
    return jsonify(message='Reminder deleted'), 200

# Expense Tracking
@app.route('/expenses', methods=['POST'])
@jwt_required()
def track_expense():
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    data['timestamp'] = datetime.now()
    mongo.db.expenses.insert_one(data)
    return jsonify(message='Expense tracked'), 201

# Update Expense
@app.route('/expenses/<expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    expense = mongo.db.expenses.find_one({'_id': expense_id, 'user_id': user_id})
    if not expense:
        return jsonify(message='Expense not found'), 404
    mongo.db.expenses.update_one({'_id': expense_id}, {'$set': data})
    return jsonify(message='Expense updated'), 200

# Delete Expense
@app.route('/expenses/<expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    user_id = get_jwt_identity()
    expense = mongo.db.expenses.find_one({'_id': expense_id, 'user_id': user_id})
    if not expense:
        return jsonify(message='Expense not found'), 404
    mongo.db.expenses.delete_one({'_id': expense_id})
    return jsonify(message='Expense deleted'), 200

# Expense Reporting with Filtering
@app.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    filters = {}

    # Apply filtering based on query parameters
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    category = request.args.get('category')
    amount_min = request.args.get('amount_min')
    amount_max = request.args.get('amount_max')

    if date_from:
        filters['timestamp'] = {'$gte': datetime.fromisoformat(date_from)}
    if date_to:
        if 'timestamp' in filters:
            filters['timestamp'].update({'$lte': datetime.fromisoformat(date_to)})
        else:
            filters['timestamp'] = {'$lte': datetime.fromisoformat(date_to)}
    if category:
        filters['category'] = category
    if amount_min:
        filters['amount'] = {'$gte': float(amount_min)}
    if amount_max:
        if 'amount' in filters:
            filters['amount'].update({'$lte': float(amount_max)})
        else:
            filters['amount'] = {'$lte': float(amount_max)}

    expenses = list(mongo.db.expenses.find({'user_id': user_id, **filters}))
    return jsonify(expenses=expenses), 200

# Category Management
@app.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    data['user_id'] = get_jwt_identity()
    mongo.db.categories.insert_one(data)
    return jsonify(message='Category created'), 201

@app.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    user_id = get_jwt_identity()
    categories = list(mongo.db.categories.find({'user_id': user_id}))
    return jsonify(categories=categories), 200

@app.route('/categories/<category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    category = mongo.db.categories.find_one({'_id': category_id, 'user_id': user_id})
    if not category:
        return jsonify(message='Category not found'), 404
    mongo.db.categories.update_one({'_id': category_id}, {'$set': data})
    return jsonify(message='Category updated'), 200

@app.route('/categories/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    user_id = get_jwt_identity()
    category = mongo.db.categories.find_one({'_id': category_id, 'user_id': user_id})
    if not category:
        return jsonify(message='Category not found'), 404
    mongo.db.categories.delete_one({'_id': category_id})
    return jsonify(message='Category deleted'), 200

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
