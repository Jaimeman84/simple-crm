from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Prospect:
    id: Optional[int]
    full_name: str
    phone_number: str
    email: str
    status: str
    notes: str
    created_at: datetime
    updated_at: datetime

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 