from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..dao.database import SessionLocal
from ..templates.models import Product

product_bp = Blueprint('product', __name__, url_prefix='/products')

@product_bp.route('/', methods=['GET'])
def get_products():
    db: Session = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return jsonify([product.as_dict() for product in products])

@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    db: Session = SessionLocal()
    new_product = Product(product_name=data['product_name'], price=data['price'], stock=data['stock'])
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    db.close()
    return jsonify(new_product.as_dict()), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    db: Session = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product:
        product.product_name = data.get('product_name', product.product_name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.commit()
        db.refresh(product)
    db.close()
    return jsonify(product.as_dict()) if product else ('Product not found', 404)

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    db: Session = SessionLocal()
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    db.close()
    return ('', 204) if product else ('Product not found', 404)
