from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..dao.database import SessionLocal
from ..templates.models import OrderItem

order_item_bp = Blueprint('order_item', __name__, url_prefix='/order_items')

@order_item_bp.route('/', methods=['GET'])
def get_order_items():
    db: Session = SessionLocal()
    order_items = db.query(OrderItem).all()
    db.close()
    return jsonify([order_item.as_dict() for order_item in order_items])

@order_item_bp.route('/', methods=['POST'])
def create_order_item():
    data = request.json
    db: Session = SessionLocal()
    new_order_item = OrderItem(order_id=data['order_id'], product_id=data['product_id'], quantity=data['quantity'], price=data['price'])
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    db.close()
    return jsonify(new_order_item.as_dict()), 201

@order_item_bp.route('/<int:order_item_id>', methods=['PUT'])
def update_order_item(order_item_id):
    data = request.json
    db: Session = SessionLocal()
    order_item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()
    if order_item:
        order_item.order_id = data.get('order_id', order_item.order_id)
        order_item.product_id = data.get('product_id', order_item.product_id)
        order_item.quantity = data.get('quantity', order_item.quantity)
        order_item.price = data.get('price', order_item.price)
        db.commit()
        db.refresh(order_item)
    db.close()
    return jsonify(order_item.as_dict()) if order_item else ('Order item not found', 404)

@order_item_bp.route('/<int:order_item_id>', methods=['DELETE'])
def delete_order_item(order_item_id):
    db: Session = SessionLocal()
    order_item = db.query(OrderItem).filter(OrderItem.order_item_id == order_item_id).first()
    if order_item:
        db.delete(order_item)
        db.commit()
    db.close()
    return ('', 204) if order_item else ('Order item not found', 404)
