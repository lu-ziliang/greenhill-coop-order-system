from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Round
from datetime import datetime

rounds_bp = Blueprint('rounds', __name__)

@rounds_bp.route('/')
def list_rounds():
    rounds = Round.query.order_by(Round.start_date.desc()).all()
    return render_template('rounds/list.html', rounds=rounds, user=current_user)

@rounds_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_round():
    if not current_user.is_coordinator:
        flash('Only coordinators can create rounds', 'error')
        return redirect(url_for('rounds.list_rounds'))
    if request.method == 'POST':
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        round_obj = Round(
            name=request.form['name'],
            start_date=start_date,
            end_date=end_date,
            status='open'
        )
        db.session.add(round_obj)
        db.session.commit()
        flash('Order round created successfully', 'success')
        return redirect(url_for('rounds.list_rounds'))
    return render_template('rounds/new.html', user=current_user)

@rounds_bp.route('/<int:round_id>/close', methods=['POST'])
@login_required
def close_round(round_id):
    if not current_user.is_coordinator:
        flash('Only coordinators can close rounds', 'error')
        return redirect(url_for('rounds.list_rounds'))
    round_obj = Round.query.get_or_404(round_id)
    round_obj.status = 'closed'
    db.session.commit()
    flash('Order round closed', 'info')
    return redirect(url_for('rounds.list_rounds'))
