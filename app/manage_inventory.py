from flask import (Blueprint, redirect, render_template, request, flash, url_for)
from app.db import get_db

bp = Blueprint('manage_inventory', __name__)

@bp.route('/add_entry', methods=['POST'])
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
            'INSERT INTO inventory (item, amount)'
            'VALUES (?,?)',
            (item, amount)
        )
        db.commit()

        return redirect('/')

    return redirect('/')

@bp.route('/update_amount', methods=['POST'])
def update_amount():
    pass

@bp.route('/<int:id>/increase_amount', methods=['POST'])
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

        return redirect('/')

    return redirect('/')

@bp.route('/<int:id>/decrease_amount', methods=['POST'])
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

        return redirect('/')

    return redirect('/')

@bp.route('/<int:id>/delete_item', methods=['POST'])
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

        return redirect('/')

    return redirect('/')

@bp.route('/<int:id>/add_to_shopping_list', methods=['POST'])
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
                'INSERT INTO shopping_list (item, amount)'
                'SELECT item, 1 FROM inventory'
                ' WHERE id = ?',
                (id,)
            )
        
        db.commit()

        return redirect('/')
    
    return redirect('/')