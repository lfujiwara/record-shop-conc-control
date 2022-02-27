class CustomerDto:
    id: str
    document: str
    name: str
    birth_date: str
    email: str
    phone: str
    is_active: bool

    def __init__(self, _id: str, document: str, name: str, birth_date: str, email: str, phone: str, is_active: bool):
        self.id = _id
        self.document = document
        self.name = name
        self.birth_date = birth_date
        self.email = email
        self.phone = phone
        self.is_active = is_active
