class RequestedCustomerNotFound(Exception):
    requested_customer_id: str

    def __init__(self, requested_customer_id: str):
        self.requested_customer_id = requested_customer_id


class ProviderException(Exception):
    def __init__(self, reason: Exception):
        self.reason = reason


__all__ = ['RequestedCustomerNotFound', 'ProviderException']
