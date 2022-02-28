import datetime


class Customer:
    id: str
    document: str
    name: str
    birth_date: datetime.date
    email: str
    phone: str
    is_active: bool

    def __init__(self, _id: str, document: str, name: str, birth_date: datetime.date, email: str, phone: str,
                 is_active: bool = True):
        self.id = _id
        self.document = document
        self.name = name
        self.birth_date = birth_date
        self.email = email
        self.phone = phone
        self.is_active = is_active

    def to_json(self):
        return {'id': str(self.id), 'document': self.document, 'name': self.name,
                'birth_date': self.birth_date.isoformat(), 'email': self.email, 'phone': self.phone,
                'is_active': self.is_active}
