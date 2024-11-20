from flask import (Blueprint, redirect, render_template, request, flash, url_for, g)
from app.auth import login_required
from app.db import get_db


bp = Blueprint('shopping_list', __name__, url_prefix='/shopping_list')

@bp.route('',methods=['GET'])
@login_required
def shopping_list():
    db = get_db()
    shopping_list = db.execute(
        'SELECT id, item, amount, user_id' 
        ' FROM shopping_list'
        ' WHERE user_id = ?', (g.user['id'],)
    ).fetchall()

    return render_template('shopping_list.html',inventory=shopping_list)

@bp.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    item = request.form['item']
    amount = request.form['amount']
    error = None

    if not item:
        error = 'Item name is required.'
    if not amount:
        error = 'Amount is required.'

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'INSERT INTO shopping_list (item, amount)'
            'VALUES (?,?)',
            (item, amount)
        )
        db.commit()

        return redirect(url_for('shopping_list.shopping_list'))

    return redirect(url_for('shopping_list.shopping_list'))

@bp.route('/update_amount', methods=['POST'])
def update_amount():
    pass

@bp.route('/<int:id>/increase_amount', methods=['POST'])
@login_required
def increase_amount(id):
    id = id
    error = None

    if not id:
        error = "Item does not exist. Reload page."

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
                'UPDATE shopping_list'
                ' SET amount = amount + 1'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('shopping_list.shopping_list'))

    return redirect(url_for('shopping_list.shopping_list'))

@bp.route('/<int:id>/decrease_amount', methods=['POST'])
@login_required
def decrease_amount(id):
    id = id
    error = None

    if not id:
        error = "Item does not exist. Reload page."

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
                'UPDATE shopping_list'
                ' SET amount = amount - 1'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('shopping_list.shopping_list'))

    return redirect(url_for('shopping_list.shopping_list'))

@bp.route('/<int:id>/delete_item', methods=['POST'])
@login_required
def delete_item(id):
    id = id
    error = None

    if not id:
        error = "Item does not exist. Reload page."

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
                'DELETE FROM shopping_list'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('shopping_list.shopping_list'))

    return redirect(url_for('shopping_list.shopping_list'))

@bp.route('/<int:id>/add_to_inventory', methods=['POST'])
@login_required
def add_to_inventory(id):
    id = id
    error = None

    if not id:
        error = "Item does not exist. Reload page."

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
                'INSERT INTO inventory (item, amount, user_id)'
                'SELECT item, amount, user_id FROM shopping_list'
                ' WHERE id = ?'
                'ON CONFLICT(item) DO UPDATE SET amount = amount + excluded.amount',
                (id,)
            )
        
        db.execute(
                'DELETE FROM shopping_list'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('shopping_list.shopping_list'))
    
    return redirect(url_for('shopping_list.shopping_list'))