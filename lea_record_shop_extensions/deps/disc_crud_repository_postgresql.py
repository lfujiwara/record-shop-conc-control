from typing import List, Optional

from asyncpg import Connection

from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud import GetDiscsRequestDto
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository


class DiscCrudRepositoryPostgresql(IDiscCrudRepository):
    _connection: Connection
    _lock_on_get: bool

    def __init__(self, _connection: Connection, lock_on_get: bool = False):
        self._connection = _connection
        self._lock_on_get = lock_on_get

    async def save(self, disc: Disc) -> None:
        query = """
            INSERT INTO discs (id, name, artist, year_of_release, genre, quantity)
            VALUES ($1, $2, $3, $4, $5, $q6)
            """
        await self._connection.execute(query, (
            disc.id, disc.name, disc.artist, disc.year_of_release, disc.genre, disc.quantity))

    async def get_by_id(self, _id: str) -> Optional[Disc]:
        query = f"""
            SELECT id, name, artist, year_of_release, genre, quantity FROM discs WHERE id = $1
            {'FOR UPDATE' if self._lock_on_get else ''};
            """
        args = (_id,)

        data = await self._connection.fetchrow(query, *args)
        if not data:
            return None
        return Disc(_id=data['id'], name=data['name'], artist=data['artist'], year_of_release=data['year_of_release'],
                    genre=data['genre'], quantity=data['quantity'])

    async def get(self, params: GetDiscsRequestDto) -> List[Disc]:

        _where_args = []
        _where_clauses = []

        if params.name_exact:
            _where_clauses.append(f'name = ${len(_where_args) + 1}')
            _where_args.append(params.name)
        if params.name:
            _where_clauses.append(f'name LIKE ${len(_where_args) + 1}')
            _where_args.append(f"%{params.name}%")
        if params.artist:
            _where_clauses.append(f'artist LIKE ${len(_where_args) + 1}')
            _where_args.append(f"%{params.artist}%")
        if params.artist_exact:
            _where_clauses.append(f'artist = ${len(_where_args) + 1}')
            _where_args.append(params.artist)
        if params.genre:
            _where_clauses.append(f'genre LIKE ${len(_where_args) + 1}')
            _where_args.append(f"%{params.genre}%")
        if params.genre_exact:
            _where_clauses.append(f'genre = ${len(_where_args) + 1}')
            _where_args.append(params.genre)
        if params.year_of_release_min:
            _where_clauses.append(f'year_of_release >= ${len(_where_args) + 1}')
            _where_args.append(params.year_of_release_min)
        if params.year_of_release_max:
            _where_clauses.append(f'year_of_release <= ${len(_where_args) + 1}')
            _where_args.append(params.year_of_release_max)

        _where = ''
        if len(_where_clauses):
            _where = f'WHERE {" AND ".join(_where_clauses)}'

        query = f'''
            SELECT id, name, artist, year_of_release, genre, quantity FROM discs
            {_where} LIMIT ${len(_where_args) + 1} OFFSET ${len(_where_args) + 2}
            '''

        args = (*_where_args, params.limit, params.offset)
        results = await self._connection.fetch(query, *args)

        return [Disc(_id=result['id'], name=result['name'], artist=result['artist'],
                     year_of_release=result['year_of_release'], genre=result['genre'], quantity=result['quantity']) for
                result in results]

    async def update(self, disc: Disc) -> bool:
        query = """
            UPDATE discs 
                SET name = $1, artist = $2, year_of_release = $3::int, genre = $4, quantity = $5::int
            WHERE id = $6
            RETURNING id;
            """
        args = (disc.name, disc.artist, disc.year_of_release, disc.genre, disc.quantity, disc.id)

        result = await self._connection.fetch(query, *args)

        return len(result) > 0

    async def delete(self, _id: str) -> bool:
        query = """
            DELETE FROM discs WHERE id = $1
            RETURNING id;
        """
        args = (_id,)

        result = await self._connection.fetch(query, *args)
        return len(result) > 0
