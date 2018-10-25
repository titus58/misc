from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	quantity = db.Column(db.String(100))

	def __repr__(self):
		return f"<{self.name}, {self.quantity}>"

	def serialize(self):
		return {'name': self.name, 'quantity': self.quantity}
	
from blueprints.item.controller import items_bp
app.register_blueprint(items_bp)