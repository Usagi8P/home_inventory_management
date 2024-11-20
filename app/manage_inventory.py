from flask import (Blueprint, redirect, request, flash, url_for, g)
from app.auth import login_required
from app.db import get_db

bp = Blueprint('manage_inventory', __name__, url_prefix='/inventory')

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
            'INSERT INTO inventory (item, amount, user_id)'
            'VALUES (?,?,?)',
            (item, amount, g.user['id'])
        )
        db.commit()

        return redirect(url_for('view_inventory.inventory'))

    return redirect(url_for('view_inventory.inventory'))

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
                'UPDATE inventory'
                ' SET amount = amount + 1'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('view_inventory.inventory'))

    return redirect(url_for('view_inventory.inventory'))

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
                'UPDATE inventory'
                ' SET amount = amount - 1'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('view_inventory.inventory'))

    return redirect(url_for('view_inventory.inventory'))

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
                'DELETE FROM inventory'
                ' WHERE id = ?',
                (id,)
            )
        db.commit()

        return redirect(url_for('view_inventory.inventory'))

    return redirect(url_for('view_inventory.inventory'))

@bp.route('/<int:id>/add_to_shopping_list', methods=['POST'])
@login_required
def add_to_shopping_list(id):
    id = id
    error = None

    if not id:
        error = "Item does not exist. Reload page."

    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
                'INSERT INTO shopping_list (item, amount, user_id)'
                'SELECT item, 1, user_id FROM inventory'
                ' WHERE id = ?',
                (id,)
            )
        
        db.commit()

        return redirect(url_for('view_inventory.inventory'))
    
    return redirect(url_for('view_inventory.inventory'))