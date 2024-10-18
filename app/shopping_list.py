from flask import (Blueprint, redirect, render_template, request, flash, url_for)
from app.db import get_db


bp = Blueprint('shopping_list', __name__)

@bp.route('/shopping_list', methods=['GET'])
def shopping_list():
    db = get_db()
    shopping_list = db.execute(
        'SELECT id, item, amount FROM shopping_list'
    ).fetchall()

    return render_template('shopping_list.html',inventory=shopping_list)

@bp.route('/shopping_list/add_entry', methods=['POST'])
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

@bp.route('/shopping_list/update_amount', methods=['POST'])
def update_amount():
    pass

@bp.route('/shopping_list/<int:id>/increase_amount', methods=['POST'])
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

@bp.route('/shopping_list/<int:id>/decrease_amount', methods=['POST'])
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

@bp.route('/shopping_list/<int:id>/delete_item', methods=['POST'])
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

@bp.route('/shopping_list/<int:id>/add_to_inventory', methods=['POST'])
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
                'INSERT INTO inventory (item, amount)'
                'SELECT item, amount FROM shopping_list'
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