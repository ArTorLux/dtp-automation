from app import db
from datetime import date, datetime, timezone
import uuid

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='nowe')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    deadline = db.Column(db.Date, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def to_dict(self):
        """Konwertuje obiekt na słownik (do JSON)"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Tworzy obiekt Order z dict (np. z JSON)"""
        # Sprawdzenie tytułu
        if not data.get('title'):
            raise ValueError("Brakuje tytułu")
        
        # Konwersja daty
        deadline = data.get('deadline')
        if deadline and isinstance(deadline, str):
            try:
                deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Nieprawidłowy format daty. Użyj YYYY-MM-DD")
        
        return cls(
            title=data['title'],
            description=data.get('description', ''),
            deadline=deadline,
            status=data.get('status', 'nowe')
        )
    
    def __repr__(self):
        return f'<Order {self.id}: {self.title}>'