from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

api = Blueprint('api', __name__)

# Nasza "pamięć" - jak notatnik na biurku
orders = []

@api.route('/orders', methods=['GET'])
def get_orders():
    """Pobiera wszystkie zlecenia"""
    return jsonify(orders)

@api.route('/orders', methods=['POST'])
def create_order():
    """Tworzy nowe zlecenie"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Brakuje tytułu'}), 400
    
    order = {
        'id': str(uuid.uuid4())[:8],
        'title': data['title'],
        'description': data.get('description', ''),
        'status': 'nowe',
        'created_at': datetime.now().isoformat(),
        'deadline': data.get('deadline')
    }
    
    orders.append(order)
    return jsonify(order), 201

@api.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Pobiera konkretne zlecenie"""
    order = next((o for o in orders if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'error': 'Zlecenie nie znalezione'}), 404
    
    return jsonify(order)

@api.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    """Aktualizuje status zlecenia"""
    order = next((o for o in orders if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'error': 'Zlecenie nie znalezione'}), 404
    
    data = request.get_json()
    if 'status' in data:
        order['status'] = data['status']
    
    return jsonify(order)

@api.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Usuwa zlecenie"""
    global orders
    order = next((o for o in orders if o['id'] == order_id), None)
    
    if not order:
        return jsonify({'error': 'Zlecenie nie znalezione'}), 404
    
    orders = [o for o in orders if o['id'] != order_id]
    return jsonify({'message': 'Zlecenie usunięte'})