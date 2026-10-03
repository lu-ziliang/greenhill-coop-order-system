from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
@login_required
def list_products():
    if current_user.is_coordinator:
        products = Product.query.all()
    else:
        products = Product.query.filter_by(is_active=True).all()
    return render_template('products/list.html', products=products)

@products_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if not current_user.is_coordinator:
        flash('Only coordinator can add products.', 'error')
        return redirect(url_for('products.list_products'))
    if request.method == 'POST':
        product = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            pricing_unit=request.form['pricing_unit'],
            bay_location=request.form.get('bay_location', '')
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/new.html')

@products_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_coordinator:
        flash('Only coordinator can edit products.', 'error')
        return redirect(url_for('products.list_products'))
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.pricing_unit = request.form['pricing_unit']
        product.bay_location = request.form.get('bay_location', '')
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/edit.html', product=product)

@products_bp.route('/<int:id>/deactivate', methods=['POST'])
@login_required
def deactivate_product(id):
    if not current_user.is_coordinator:
        flash('Only coordinator can withdraw products.', 'error')
        return redirect(url_for('products.list_products'))
    product = Product.query.get_or_404(id)
    product.deactivate()
    db.session.commit()
    flash(f'Product "{product.name}" has been withdrawn.', 'success')
    return redirect(url_for('products.list_products'))
