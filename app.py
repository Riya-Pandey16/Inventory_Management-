from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# Import models
from models import db, User, Product

db.init_app(app)
# Import routes
import routes

# Initialize database on import
with app.app_context():
    db.create_all()

    # Insert sample products if table is empty
    if not Product.query.first():
        sample_products = [
            Product(name="Laptop", quantity=10, price=50000),
            Product(name="Mouse", quantity=50, price=500),
            Product(name="Keyboard", quantity=30, price=1000)
        ]
        db.session.bulk_save_objects(sample_products)
        db.session.commit()
        print("Sample products added.")


if __name__ == '__main__':
    app.run(debug=True)


   
