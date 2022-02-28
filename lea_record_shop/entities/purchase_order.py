import datetime

from lea_record_shop.entities.customer import Customer
from lea_record_shop.entities.disc import Disc


class PurchaseOrder:
    id: str
    customer: Customer
    disc: Disc
    quantity: int
    timestamp: datetime.datetime

    def __init__(self, _id: str, customer: Customer, disc: Disc, quantity: int,
                 timestamp: datetime.datetime = datetime.datetime.now()):
        self.id = _id
        self.customer = customer
        self.disc = disc
        self.quantity = quantity
        self.timestamp = timestamp
