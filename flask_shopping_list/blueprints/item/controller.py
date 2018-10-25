from flask import Blueprint, jsonify
from app import Item
items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/')
@items_bp.route('/list')
def get_all():
	items = list(map(lambda x: x.serialize(), Item.query.all()))
	return jsonify(items=items)
