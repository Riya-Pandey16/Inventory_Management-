from flask import render_template, request, redirect, url_for, session, flash
from functools import wraps
#from flask_login import login_required

from app import app
from models import db, User, Product


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
            if user.role == 'Admin':
                return redirect(url_for('admin'))
            elif user.role == 'Staff':
                return redirect(url_for('staff'))
            else:
                flash("Invalid user role.", "danger")
                return redirect(url_for('login'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

# Routes
@app.route('/')
def home():
    return render_template('home.html')



@app.route('/logout')

def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch data from the form
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'warning')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))  # After successful registration, redirect to login page
    
    # If GET request, simply render the register page
    return render_template('register.html')




@app.route('/products')
#@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
#@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        new_product = Product(name=name, quantity=quantity, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for('admin'))
    return render_template('add_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
#@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.quantity = request.form['quantity']
        product.price = request.form['price']
        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for('admin'))
    return render_template('edit_product.html', product=product)


@app.route('/products/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully!", "success")
        return redirect(url_for('admin'))
    return render_template('delete_product.html', product=product)

@app.route('/admin')
def admin():
    if 'logged_in' in session and session.get('role') == 'Admin':
        products = Product.query.all()
        return render_template('admin_dashboard.html', products=products)
    else:
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('login'))


@app.route('/staff')
def staff():
    if 'logged_in' in session and session.get('role') == 'Staff':
        products = Product.query.all()
        return render_template('staff_dashboard.html', products=products)
    else:
        flash("Access denied: Staff only.", "danger")
        return redirect(url_for('login'))

