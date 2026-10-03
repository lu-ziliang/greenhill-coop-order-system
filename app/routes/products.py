from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def list_products():
    products = Product.query.filter_by(is_active=True).all()
    return render_template('products/list.html', products=products, user=current_user)

@products_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if not current_user.is_coordinator:
        flash('Only coordinators can add products', 'error')
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
        flash('Product added successfully', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/new.html', user=current_user)

@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_coordinator:
        flash('Only coordinators can edit products', 'error')
        return redirect(url_for('products.list_products'))
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.pricing_unit = request.form['pricing_unit']
        product.bay_location = request.form.get('bay_location', '')
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('products/edit.html', product=product, user=current_user)

@products_bp.route('/<int:product_id>/deactivate', methods=['POST'])
@login_required
def deactivate_product(product_id):
    if not current_user.is_coordinator:
        flash('Only coordinators can deactivate products', 'error')
        return redirect(url_for('products.list_products'))
    product = Product.query.get_or_404(product_id)
    product.deactivate()
    db.session.commit()
    flash('Product deactivated', 'info')
    return redirect(url_for('products.list_products'))
