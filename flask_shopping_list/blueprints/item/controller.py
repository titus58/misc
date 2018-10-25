from flask import Blueprint, jsonify, render_template
from app import Item
items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
@items_bp.route('/list')
def get_all():
	return render_template('items.html', items=Item.query.all())
