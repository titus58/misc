from flask import Blueprint, jsonify, render_template, request, current_app, abort
from app import Item, db
items_bp = Blueprint('items', __name__, url_prefix='/items')

@items_bp.route('/', methods=["GET"])
@items_bp.route('/list', methods=["GET"])
def get_all():
	print(request.method)
	return render_template('items.html', items=Item.query.all())

@items_bp.route('/', methods=['POST'])
def add_new():
	name = request.form.get("name")
	quantity = request.form.get("quantity")
	if not name or not quantity:
		abort(400)
	i = Item(name=name, quantity=quantity)
	current_app.logger.debug(f"vlad <{name}> <{quantity}>")
	db.session.add(i)
	db.session.commit()
	return "Okay"