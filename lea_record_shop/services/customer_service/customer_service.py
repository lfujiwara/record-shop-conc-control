import datetime
from uuid import uuid4

import lea_record_shop.services.customer_service.customer_service_exceptions as customer_service_exceptions
from lea_record_shop.entities import Customer
from lea_record_shop.services.customer_service.customer_service_repository import ICustomerServiceRepository
from lea_record_shop.services.customer_service.dto import SignUpCustomerRequestDto, UpdateCustomerRequestDto, \
    CustomerDto


class CustomerService:
    _repository: ICustomerServiceRepository

    def __init__(self, repository: ICustomerServiceRepository):
        self._repository = repository

    async def signup_customer(self, data: SignUpCustomerRequestDto):
        customer = Customer(_id=str(uuid4()), document=data.document, name=data.name,
                            birth_date=datetime.date.fromisoformat(data.birth_date), email=data.email, phone=data.phone,
                            is_active=True)

        # this probably could be wrapped somewhere else
        try:
            await self._repository.save(customer)
        except Exception as e:
            raise customer_service_exceptions.ProviderException(e)

        response = CustomerDto(_id=customer.id, document=customer.document, name=customer.name,
                               birth_date=customer.birth_date.isoformat(), email=customer.email, phone=customer.phone,
                               is_active=customer.is_active)

        return response

    async def update_customer(self, data: UpdateCustomerRequestDto):
        customer = await self._repository.get_by_id(data.id)
        if customer is None:
            raise customer_service_exceptions.RequestedCustomerNotFound(data.id)

        customer.document = data.document
        customer.name = data.name
        customer.birth_date = data.birth_date
        customer.email = data.email
        customer.phone = data.phone
        customer.is_active = data.is_active

        try:
            await self._repository.update(customer)
        except Exception as e:
            raise customer_service_exceptions.ProviderException(e)

        response = CustomerDto(_id=customer.id, document=customer.document, name=customer.name,
                               birth_date=customer.birth_date.isoformat(), email=customer.email, phone=customer.phone,
                               is_active=customer.is_active)

        return response
