from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, Product, Round, Member

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_order():
    active_round = Round.query.filter_by(status='open').first()
    if not active_round:
        flash('There is no active order round. Please wait for the coordinator to open a round.', 'error')
        return redirect(url_for('main.index'))
    products = Product.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        order = Order(member_id=current_user.id, round_id=active_round.id)
        db.session.add(order)
        db.session.flush()
        total = 0.0
        for product in products:
            qty = request.form.get(f'qty_{product.id}', '0')
            if qty and float(qty) > 0:
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=float(qty),
                    unit_price=product.price,
                    pricing_unit=product.pricing_unit
                )
                db.session.add(item)
                total += float(qty) * product.price
        order.total = total
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('orders.my_orders'))
    return render_template('orders/new.html', products=products, active_round=active_round, user=current_user)

@orders_bp.route('/my')
@login_required
def my_orders():
    orders = Order.query.filter_by(member_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/my.html', orders=orders, user=current_user)

@orders_bp.route('/all')
@login_required
def all_orders():
    if not current_user.is_coordinator:
        flash('Only coordinators can view all orders', 'error')
        return redirect(url_for('orders.my_orders'))
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders/all.html', orders=orders, user=current_user)

@orders_bp.route('/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.member_id != current_user.id and not current_user.is_coordinator:
        flash('You can only edit your own orders', 'error')
        return redirect(url_for('orders.my_orders'))
    products = Product.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        for item in order.items:
            db.session.delete(item)
        total = 0.0
        for product in products:
            qty = request.form.get(f'qty_{product.id}', '0')
            if qty and float(qty) > 0:
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=float(qty),
                    unit_price=product.price,
                    pricing_unit=product.pricing_unit
                )
                db.session.add(item)
                total += float(qty) * product.price
        order.total = total
        db.session.commit()
        flash('Order updated successfully', 'success')
        return redirect(url_for('orders.my_orders'))
    return render_template('orders/edit.html', order=order, products=products, user=current_user)

@orders_bp.route('/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.member_id != current_user.id and not current_user.is_coordinator:
        flash('You can only delete your own orders', 'error')
        return redirect(url_for('orders.my_orders'))
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted', 'info')
    return redirect(url_for('orders.my_orders'))

@orders_bp.route('/totals')
@login_required
def totals():
    if not current_user.is_coordinator:
        flash('Only coordinators can view totals', 'error')
        return redirect(url_for('orders.my_orders'))
    active_round = Round.query.filter_by(status='open').first()
    if not active_round:
        flash('No active round', 'error')
        return redirect(url_for('main.index'))
    orders = Order.query.filter_by(round_id=active_round.id).all()
    product_totals = {}
    for order in orders:
        for item in order.items:
            if item.product_id not in product_totals:
                product_totals[item.product_id] = {
                    'name': item.product_name,
                    'quantity': 0,
                    'unit_price': item.unit_price,
                    'pricing_unit': item.pricing_unit,
                    'total': 0
                }
            product_totals[item.product_id]['quantity'] += item.quantity
            product_totals[item.product_id]['total'] += item.quantity * item.unit_price
    return render_template('orders/totals.html', product_totals=product_totals, active_round=active_round, user=current_user)

@orders_bp.route('/packing')
@login_required
def packing():
    if not current_user.is_coordinator:
        flash('Only coordinators can view packing sheets', 'error')
        return redirect(url_for('orders.my_orders'))
    active_round = Round.query.filter_by(status='open').first()
    if not active_round:
        flash('No active round', 'error')
        return redirect(url_for('main.index'))
    orders = Order.query.filter_by(round_id=active_round.id).all()
    packing_data = {}
    for order in orders:
        member = Member.query.get(order.member_id)
        for item in order.items:
            if item.product_id not in packing_data:
                packing_data[item.product_id] = {
                    'name': item.product_name,
                    'bay_location': item.product.bay_location if item.product else '',
                    'pricing_unit': item.pricing_unit,
                    'members': {}
                }
            if member.username not in packing_data[item.product_id]['members']:
                packing_data[item.product_id]['members'][member.username] = 0
            packing_data[item.product_id]['members'][member.username] += item.quantity
    return render_template('orders/packing.html', packing_data=packing_data, active_round=active_round, user=current_user)
