from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Round
from datetime import date

rounds_bp = Blueprint('rounds', __name__)

@rounds_bp.route('/')
@login_required
def list_rounds():
    rounds = Round.query.order_by(Round.start_date.desc()).all()
    return render_template('rounds/list.html', rounds=rounds)

@rounds_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_round():
    if not current_user.is_coordinator:
        flash('Only coordinator can create rounds.', 'error')
        return redirect(url_for('rounds.list_rounds'))
    if request.method == 'POST':
        existing_open = Round.query.filter_by(status='open').first()
        if existing_open:
            existing_open.status = 'closed'
        round = Round(
            name=request.form['name'],
            start_date=date.fromisoformat(request.form['start_date']) if request.form['start_date'] else None,
            end_date=date.fromisoformat(request.form['end_date']) if request.form['end_date'] else None,
            status='open'
        )
        db.session.add(round)
        db.session.commit()
        flash(f'Round "{round.name}" created and is now open.', 'success')
        return redirect(url_for('rounds.list_rounds'))
    return render_template('rounds/new.html')

@rounds_bp.route('/<int:id>/close', methods=['POST'])
@login_required
def close_round(id):
    if not current_user.is_coordinator:
        flash('Only coordinator can close rounds.', 'error')
        return redirect(url_for('rounds.list_rounds'))
    round = Round.query.get_or_404(id)
    round.status = 'closed'
    db.session.commit()
    flash(f'Round "{round.name}" closed.', 'info')
    return redirect(url_for('rounds.list_rounds'))

@rounds_bp.route('/<int:id>/pack', methods=['POST'])
@login_required
def mark_packed(id):
    if not current_user.is_coordinator:
        flash('Only coordinator can mark rounds as packed.', 'error')
        return redirect(url_for('rounds.list_rounds'))
    round = Round.query.get_or_404(id)
    round.status = 'packed'
    db.session.commit()
    flash(f'Round "{round.name}" marked as packed.', 'info')
    return redirect(url_for('rounds.list_rounds'))
