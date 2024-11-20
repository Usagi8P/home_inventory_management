from flask import (Blueprint, redirect, render_template, request, g, session)
from app.auth import login_required
from app.db import get_db


bp = Blueprint('view_inventory', __name__)

@bp.route('/inventory', methods=['GET'])
@login_required
def inventory():
    db = get_db()
    inventory = db.execute(
        'SELECT id, user_id, item, amount'
        ' FROM inventory'
        ' WHERE user_id = ?', (g.user['id'],)
    ).fetchall()
    
    return render_template('index.html',inventory=inventory)
