from flask import Blueprint, request, jsonify
from app.models import Order
from app import db
from datetime import datetime
import uuid

api = Blueprint('api', __name__)

@api.route("/")    
def root():
    return {"DTP-automation": "Gotowe"}   

@api.route('/orders', methods=['GET'])
def get_orders():
    """Pobiera wszystkie zlecenia"""
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@api.route('/orders', methods=['POST'])
def create_order():
    """Tworzy nowe zlecenie"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Brakuje tytułu'}), 400

    order = Order.from_dict(data)
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify(order.to_dict()), 201

@api.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Pobiera konkretne zlecenie"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Zlecenie nie znalezione'}), 404
    
    return jsonify(order.to_dict())

@api.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Aktualizuje status zlecenia"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Zlecenie nie znalezione'}), 404
    
    data = request.get_json()
    
    if 'status' in data:
        order.status = data['status']
    
    if 'title' in data:
        order.title = data['title']
    
    if 'description' in data:
        order.description = data['description']
    
    db.session.commit()
    return jsonify(order.to_dict())

@api.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Usuwa zlecenie"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Zlecenie nie znalezione'}), 404
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': 'Zlecenie usunięte'})