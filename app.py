from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models
from models import User, Product

# Import routes
import routes

# Initialize database on import
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)