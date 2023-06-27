# import json
# import os
# # import requests
# #import all modules from app.py
# from app import *
# # from flask import Flask, render_template, request, jsonify
# def register():
    
#     """Handle user registration."""
#     if request.method == 'POST':
#         data = request.form
#         existing_user = next((user for user in users if user['email'] == data['email']), None)
#         if existing_user:
#             return jsonify(message='Email already exists'), 409
#         users.append(data)
#         # Save the updated user data to the file
#         with open(USERS_FILE, 'w') as file:
#             json.dump(users, file)
#         return jsonify(message='User registered'), 201
#     return render_template('register.html')



# # register(), but will have a password functionality. input passwprd, if password is not == password in file, return error, else create user

# def reister():
#     #ask user for password
#     password  = 
#     return render_template('register.html')

