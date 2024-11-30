from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..dao.database import SessionLocal
from ..templates.models import Order

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/', methods=['GET'])
def get_orders():
    db: Session = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return jsonify([order.as_dict() for order in orders])

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    db: Session = SessionLocal()
    new_order = Order(user_id=data['user_id'], total_amount=data['total_amount'])
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()
    return jsonify(new_order.as_dict()), 201

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    db: Session = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        order.user_id = data.get('user_id', order.user_id)
        order.total_amount = data.get('total_amount', order.total_amount)
        db.commit()
        db.refresh(order)
    db.close()
    return jsonify(order.as_dict()) if order else ('Order not found', 404)

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    db: Session = SessionLocal()
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    db.close()
    return ('', 204) if order else ('Order not found', 404)
