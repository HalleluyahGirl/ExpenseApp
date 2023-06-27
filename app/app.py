import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

USERS_FILE = 'users.json'
REMINDERS_FILE = 'reminders.json'
EXPENSES_FILE = 'expenses.json'
CATEGORIES_FILE = 'categories.json'

# Check if the files exist and load existing data
try:
    with open(USERS_FILE, 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = []

try:
    with open(REMINDERS_FILE, 'r') as file:
        reminders = json.load(file)
except FileNotFoundError:
    reminders = []

try:
    with open(EXPENSES_FILE, 'r') as file:
        expenses = json.load(file)
except FileNotFoundError:
    expenses = []

try:
    with open(CATEGORIES_FILE, 'r') as file:
        categories = json.load(file)
except FileNotFoundError:
    categories = []

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    """Handle user registration."""
    if request.method == 'POST':
        data = request.form
        existing_user = next((user for user in users if user['email'] == data['email']), None)
        if existing_user:
            return jsonify(message='Email already exists'), 409
        users.append(data)
        # Save the updated user data to the file
        with open(USERS_FILE, 'w') as file:
            json.dump(users, file)
        return jsonify(message='User registered'), 201
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        data = request.form
        user = next((user for user in users if user['email'] == data['email']), None)
        if not user or user['password'] != data['password']:
            return jsonify(message='Invalid credentials'), 401
        return jsonify(message='Login successful'), 200
    return render_template('login.html')

@app.route('/reminders', methods=['GET', 'POST'])
def reminder():
    """Handle reminder creation and listing."""
    if request.method == 'POST':
        data = request.form
        reminders.append(data)
        # Save the updated reminder data to the file
        with open(REMINDERS_FILE, 'w') as file:
            json.dump(reminders, file)
        return jsonify(message='Reminder created'), 201
    return render_template('reminder.html', reminders=reminders)

@app.route('/expenses', methods=['GET', 'POST'])
def expense():
    """Handle expense tracking and listing."""
    if request.method == 'POST':
        data = request.form
        expenses.append(data)
        # Save the updated expense data to the file
        with open(EXPENSES_FILE, 'w') as file:
            json.dump(expenses, file)
        return jsonify(message='Expense tracked'), 201
    
    # prompting the user to input their expense/sum of expenses
    def add_expense():
        # let the user input their income, it should be an integer, not a string. if the user input a string, return an error
        income = int(request.form['income: '])
        if not isinstance(income, int):
            return jsonify(message='Income must be an integer'), 400
        else:
            return jsonify(message='Expense tracked'), 201
        
    return render_template('expense.html', expenses=expenses)
        
        

expense()






    

@app.route('/categories', methods=['GET', 'POST'])
def category():
    """Handle category creation and listing."""
    if request.method == 'POST':
        data = request.form
        categories.append(data)
        # Save the updated category data to the file
        with open(CATEGORIES_FILE, 'w') as file:
            json.dump(categories, file)
        return jsonify(message='Category created'), 201
    return render_template('category.html', categories=categories)

@app.route('/reminders/<reminder_id>', methods=['PUT', 'DELETE'])
def update_reminder(reminder_id):
    """Handle updating and deleting a reminder."""
    if request.method == 'PUT':
        data = request.form
        reminder = next((rem for rem in reminders if rem['id'] == reminder_id), None)
        if not reminder:
            return jsonify(message='Reminder not found'), 404
        reminder.update(data)
        # Save the updated reminder data to the file
        with open(REMINDERS_FILE, 'w') as file:
            json.dump(reminders, file)
        return jsonify(message='Reminder updated'), 200
    elif request.method == 'DELETE':
        reminder = next((rem for rem in reminders if rem['id'] == reminder_id), None)
        if not reminder:
            return jsonify(message='Reminder not found'), 404
        reminders.remove(reminder)
        # Save the updated reminder data to the file
        with open(REMINDERS_FILE, 'w') as file:
            json.dump(reminders, file)
        return jsonify(message='Reminder deleted'), 200
    


@app.route('/expenses/<expense_id>', methods=['PUT', 'DELETE'])
def update_expense(expense_id):
    """Handle updating and deleting an expense."""
    if request.method == 'PUT':
        data = request.form
        expense = next((exp for exp in expenses if exp['id'] == expense_id), None)
        if not expense:
            return jsonify(message='Expense not found'), 404
        expense.update(data)
        # Save the updated expense data to the file
        with open(EXPENSES_FILE, 'w') as file:
            json.dump(expenses, file)
        return jsonify(message='Expense updated'), 200
    elif request.method == 'DELETE':
        expense = next((exp for exp in expenses if exp['id'] == expense_id), None)
        if not expense:
            return jsonify(message='Expense not found'), 404
        expenses.remove(expense)
        # Save the updated expense data to the file
        with open(EXPENSES_FILE, 'w') as file:
            json.dump(expenses, file)
        return jsonify(message='Expense deleted'), 200


    # Tests that a category can be created successfully
def test_create_category_successfully(self, mocker):
    data = {'name': 'test_category'}
    mocker.patch('builtins.open', mocker.mock_open())
    response = self.client.post('/categories', data=data)
    assert response.status_code == 201
    assert response.json == {'message': 'Category created'}


    

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
