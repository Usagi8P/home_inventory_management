from flask import (Blueprint, redirect, render_template, request)
from app.db import get_db


bp = Blueprint('view_inventory', __name__)

@bp.route('/inventory', methods=['GET'])
def inventory():
    db = get_db()
    inventory = db.execute(
        'SELECT id, item, amount FROM inventory'
    ).fetchall()
    return render_template('index.html',inventory=inventory)