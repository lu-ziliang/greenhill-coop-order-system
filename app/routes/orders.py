from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, Product, Round

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_order():
    current_round = Round.query.filter_by(status='open').first()
    if not current_round:
        flash('No open order round available.', 'error')
        return redirect(url_for('main.index'))
    products = Product.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        order = Order(member_id=current_user.id, round_id=current_round.id, status='active')
        db.session.add(order)
        db.session.flush()
        total = 0.0
        for product in products:
            qty = request.form.get(f'qty_{product.id}', '0')
            if qty and float(qty) > 0:
                qty = float(qty)
                line_total = round(product.price * qty, 2)
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=qty,
                    unit_price=product.price,
                    pricing_unit=product.pricing_unit
                )
                db.session.add(item)
                total += line_total
        order.total = round(total, 2)
        db.session.commit()
        flash(f'Order #{order.id} placed successfully! Total: ${order.total:.2f}', 'success')
        return redirect(url_for('orders.my_orders'))
    return render_template('orders/new.html', products=products, current_round=current_round)

@orders_bp.route('/my')
@login_required
def my_orders():
    orders = Order.query.filter_by(member_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders/my.html', orders=orders)

@orders_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    if order.member_id != current_user.id:
        flash('You can only edit your own orders.', 'error')
        return redirect(url_for('orders.my_orders'))
    current_round = Round.query.get(order.round_id)
    if current_round.status != 'open':
        flash('Round is closed — orders cannot be modified.', 'error')
        return redirect(url_for('orders.my_orders'))
    products = Product.query.filter_by(is_active=True).all()
    if request.method == 'POST':
        OrderItem.query.filter_by(order_id=order.id).delete()
        total = 0.0
        for product in products:
            qty = request.form.get(f'qty_{product.id}', '0')
            if qty and float(qty) > 0:
                qty = float(qty)
                line_total = round(product.price * qty, 2)
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    quantity=qty,
                    unit_price=product.price,
                    pricing_unit=product.pricing_unit
                )
                db.session.add(item)
                total += line_total
        order.total = round(total, 2)
        db.session.commit()
        flash('Order updated successfully.', 'success')
        return redirect(url_for('orders.my_orders'))
    return render_template('orders/edit.html', order=order, products=products)

@orders_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_order(id):
    order = Order.query.get_or_404(id)
    if order.member_id != current_user.id:
        flash('You can only cancel your own orders.', 'error')
        return redirect(url_for('orders.my_orders'))
    current_round = Round.query.get(order.round_id)
    if current_round.status != 'open':
        flash('Round is closed — orders cannot be cancelled.', 'error')
        return redirect(url_for('orders.my_orders'))
    order.status = 'cancelled'
    db.session.commit()
    flash('Order cancelled.', 'info')
    return redirect(url_for('orders.my_orders'))

@orders_bp.route('/all')
@login_required
def all_orders():
    if not current_user.is_coordinator:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    current_round = Round.query.filter_by(status='open').first()
    if current_round:
        orders = Order.query.filter_by(round_id=current_round.id, status='active').order_by(Order.member_id).all()
    else:
        orders = []
    return render_template('orders/all.html', orders=orders, current_round=current_round)

@orders_bp.route('/totals')
@login_required
def product_totals():
    if not current_user.is_coordinator:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    current_round = Round.query.filter_by(status='open').first()
    totals = {}
    if current_round:
        items = OrderItem.query.join(Order).filter(
            Order.round_id == current_round.id,
            Order.status == 'active'
        ).all()
        for item in items:
            if item.product_id not in totals:
                totals[item.product_id] = {
                    'name': item.product_name,
                    'unit': item.pricing_unit,
                    'quantity': 0,
                    'value': 0
                }
            totals[item.product_id]['quantity'] += item.quantity
            totals[item.product_id]['value'] += item.quantity * item.unit_price
    return render_template('orders/totals.html', totals=totals, current_round=current_round)

@orders_bp.route('/packing')
@login_required
def packing_sheet():
    if not current_user.is_coordinator:
        flash('Access denied.', 'error')
        return redirect(url_for('main.index'))
    current_round = Round.query.filter(Round.status.in_(['closed', 'packed'])).first()
    orders = []
    if current_round:
        orders = Order.query.filter_by(round_id=current_round.id, status='active').order_by(Order.member_id).all()
    return render_template('orders/packing.html', orders=orders, current_round=current_round)
