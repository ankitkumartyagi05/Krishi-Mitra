# auth.py
from flask import Blueprint, request, jsonify
from models import User  # Import User from models only
from utils.database import db
from utils.security import generate_token
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)

# Removed duplicate User class definition

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        identifier = data.get('identifier')  # Can be username or email
        password = data.get('password')

        if not identifier or not password:
            return jsonify({'error': 'Username/email and password are required'}), 400

        # Find user by email or username
        user = User.query.filter_by(email=identifier).first()
        if not user:
            user = User.query.filter_by(username=identifier).first()

        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Log in user and generate token
        login_user(user)
        token = generate_token(user.id)

        return jsonify({
            'message': 'Login successful',
            'access_token': token
        }), 200

    except Exception as e:
        return jsonify({'error': 'Login failed', 'message': str(e)}), 500