from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from ..templates.models import Item
from ..dao.database import SessionLocal

item_bp = Blueprint('item', __name__, url_prefix='/items')

@item_bp.route('/', methods=['GET'])
def read_items():
    db: Session = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return jsonify([item.as_dict() for item in items])
