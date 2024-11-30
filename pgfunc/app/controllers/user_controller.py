from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from ..dao.database import SessionLocal
from ..templates.models import User

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    db: Session = SessionLocal()
    users = db.query(User).all()
    db.close()
    return jsonify([user.as_dict() for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    db: Session = SessionLocal()
    new_user = User(username=data['username'], email=data['email'])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return jsonify(new_user.as_dict()), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    db: Session = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.commit()
        db.refresh(user)
    db.close()
    return jsonify(user.as_dict()) if user else ('User not found', 404)

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    return ('', 204) if user else ('User not found', 404)
