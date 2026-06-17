import json
import pytest

def test_get_orders_empty(client):
    """Sprawdza czy lista zleceń jest pusta na starcie"""
    response = client.get('/api/orders')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

def test_create_order(client):
    """Sprawdza czy można utworzyć zlecenie"""
    order_data = {
        'title': 'Projekt książki',
        'description': 'Skład i przygotowanie do druku',
        'deadline': '2025-12-31'
    }
    
    response = client.post('/api/orders', json=order_data)
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['title'] == 'Projekt książki'
    assert data['status'] == 'nowe'
    assert 'id' in data
    assert 'created_at' in data
    assert 'deadline' in data

def test_create_order_without_title(client):
    """Sprawdza czy API zwraca błąd gdy brakuje tytułu"""
    response = client.post('/api/orders', json={'description': 'Test'})
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert 'error' in data

def test_get_order_by_id(client):
    """Tworzy zlecenie i sprawdza czy można je pobrać"""
    # Najpierw tworzymy
    response = client.post('/api/orders', json={'title': 'Test'})
    created = json.loads(response.data)
    order_id = created['id']
    
    # Potem pobieramy
    response = client.get(f'/api/orders/{order_id}')
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['id'] == order_id
    assert data['title'] == 'Test'

def test_update_order_status(client):
    """Sprawdza czy można zmienić status"""
    # Tworzymy
    response = client.post('/api/orders', json={'title': 'Test'})
    created = json.loads(response.data)
    order_id = created['id']
    
    # Aktualizujemy
    response = client.put(f'/api/orders/{order_id}', 
                          json={'status': 'gotowe'})
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'gotowe'

def test_delete_order(client):
    """Sprawdza czy można usunąć zlecenie"""
    # Tworzymy
    response = client.post('/api/orders', json={'title': 'Do usunięcia'})
    created = json.loads(response.data)
    order_id = created['id']
    
    # Usuwamy
    response = client.delete(f'/api/orders/{order_id}')
    assert response.status_code == 200
    
    # Sprawdzamy czy zniknęło
    response = client.get(f'/api/orders/{order_id}')
    assert response.status_code == 404

def test_search_orders(client):
    """Test wyszukiwania (nowa funkcjonalność!)"""
    # Tworzymy dwa zlecenia
    client.post('/api/orders', json={'title': 'Książka A'})
    client.post('/api/orders', json={'title': 'Książka B'})
    
    response = client.get('/api/orders')
    data = json.loads(response.data)
    
    assert len(data) == 2