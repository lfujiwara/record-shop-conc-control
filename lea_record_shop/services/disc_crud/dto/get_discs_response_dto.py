from lea_record_shop.services.disc_crud.dto.get_discs_request_dto import GetDiscsRequestDto
from lea_record_shop.services.disc_crud.dto.disc_dto import DiscDto


class GetDiscsResponseDto():
    params: GetDiscsRequestDto
    data: [DiscDto]

    offset: int = 0
    limit: int = 20
