from uuid import uuid4

from lea_record_shop.entities import PurchaseOrder
from lea_record_shop.services.customer_service.customer_service_repository import ICustomerServiceRepository
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository
from lea_record_shop.services.purchase_order_service.dto import PlacePurchaseOrderRequestDto
from lea_record_shop.services.purchase_order_service.purchase_order_repository import IPurchaseOrderRepository
from lea_record_shop.services.purchase_order_service.unit_of_work import \
    IUnitOfWork


class PurchaseOrderService:
    _uow: IUnitOfWork
    _purchase_order_repository: IPurchaseOrderRepository
    _customer_repository: ICustomerServiceRepository
    _disc_repository: IDiscCrudRepository

    def __init__(self, uow: IUnitOfWork, purchase_order_repository: IPurchaseOrderRepository,
                 customer_repository: ICustomerServiceRepository, disc_repository: IDiscCrudRepository):
        self._uow = uow
        self._purchase_order_repository = purchase_order_repository
        self._customer_repository = customer_repository
        self._disc_repository = disc_repository

    async def place_purchase_order(self, data: PlacePurchaseOrderRequestDto):
        await self._uow.begin()

        customer = await self._customer_repository.get_by_id(data.customer_id)
        if customer is None:
            await self._handle_customer_not_found()

        disc = await self._disc_repository.get_by_id(data.disc_id)
        if disc is None:
            await self._handle_disc_not_found()

        if data.quantity <= 0:
            raise ValueError("Quantity must be greater than 0.")
        if disc.quantity < data.quantity:
            raise ValueError("Not enough discs in stock.")
        disc.quantity -= data.quantity
        purchase_order = PurchaseOrder(uuid4(), customer, disc, data.quantity)

        await self._purchase_order_repository.save(purchase_order)
        await self._disc_repository.update(disc)

        await self._uow.complete()

        return purchase_order

    async def _handle_customer_not_found(self):
        await self._uow.reset()
        raise Exception("Customer not found")

    async def _handle_disc_not_found(self):
        await self._uow.reset()
        raise Exception("Disc not found")
