class RequestedDiscWithoutEnoughStock(Exception):
    requested_disc_id: str

    def __init__(self, requested_disc_id: str):
        self.requested_disc_id = requested_disc_id


class ProviderException(Exception):
    def __init__(self, reason: Exception):
        self.reason = reason


__all__ = ['RequestedDiscWithoutEnoughStock', 'ProviderException']
