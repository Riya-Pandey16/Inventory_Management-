from flask import render_template, request, redirect, url_for, session, flash
from functools import wraps

from app import app
from models import db, User, Product


# Authentication decorator
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logged_in' not in session:
                flash("You need to log in first.", "danger")
                return redirect(url_for('login'))
            if role and session.get('role') != role:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['logged_in'] = True
            session['username'] = user.username
            session['role'] = user.role
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required()
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required()
def dashboard():
    return render_template('dashboard.html', role=session.get('role'))

@app.route('/products')
@login_required()
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@login_required(role='Admin')
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        new_product = Product(name=name, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('products'))
    return render_template('add_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required(role='Admin')
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = request.form['quantity']
        product.price = request.form['price']
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('products'))
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:id>', methods=['POST'])
@login_required(role='Admin')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for('products'))