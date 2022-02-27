from typing import Awaitable, List

from aiopg import connection as pg_connection

from lea_record_shop.entities import Disc
from lea_record_shop.services.disc_crud import GetDiscsRequestDto
from lea_record_shop.services.disc_crud.disc_crud_repository import IDiscCrudRepository


class DiscCrudRepositoryPostgresql(IDiscCrudRepository):
    _connection: pg_connection

    def __init__(self, _connection: pg_connection):
        self._connection = _connection

    async def save(self, disc: Disc) -> Awaitable[None]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute("""
            INSERT INTO discs (id, name, artist, year_of_release, genre, quantity)
            VALUES (%s, %s, %s, %s, %s, %s);
            """, (disc.id, disc.name, disc.artist, disc.year_of_release, disc.genre, disc.quantity))

    async def get_by_id(self, _id: str) -> Awaitable[Disc]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute("""
            SELECT id, name, artist, year_of_release, genre, quantity FROM discs WHERE id = %s;
            """, (_id,))
            data = await _cursor.fetchone()

        if not data:
            return None
        return Disc(id=data[0], name=data[1], artist=data[2], year_of_release=data[3], genre=data[4], quantity=data[5])

    async def get(self, params: GetDiscsRequestDto) -> Awaitable[List[Disc]]:

        _where_args = []
        _where_clauses = []

        if params.name_exact:
            _where_clauses.append("name = %s")
            _where_args.append(params.name)
        if params.name:
            _where_clauses.append("name LIKE %s")
            _where_args.append(f"%{params.name}%")
        if params.artist:
            _where_clauses.append("artist LIKE %s")
            _where_args.append(f"%{params.artist}%")
        if params.artist_exact:
            _where_clauses.append("artist = %s")
            _where_args.append(params.artist)
        if params.genre:
            _where_clauses.append("genre LIKE %s")
            _where_args.append(f"%{params.genre}%")
        if params.genre_exact:
            _where_clauses.append("genre = %s")
            _where_args.append(params.genre)
        if params.year_of_release_min:
            _where_clauses.append("year_of_release >= %s")
            _where_args.append(params.year_of_release_min)
        if params.year_of_release_max:
            _where_clauses.append("year_of_release <= %s")
            _where_args.append(params.year_of_release_max)

        _where = ''
        if len(_where_clauses):
            _where = f'WHERE {" AND ".join(_where_clauses)}'

        async with self._connection.cursor() as _cursor:
            await _cursor.execute(f'''
            SELECT id, name, artist, year_of_release, genre, quantity FROM discs
            {_where} LIMIT %s OFFSET %s;
            ''', (*_where_args, params.limit, params.offset))

            results = await _cursor.fetchall()

        return [Disc(id=result[0], name=result[1], artist=result[2], year_of_release=result[3], genre=result[4],
                     quantity=result[5]) for result in results]

    async def update(self, disc: Disc) -> Awaitable[bool]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute("""
            UPDATE discs 
                SET name = %s, artist = %s, year_of_release = %s, genre = %s, quantity = %s
            WHERE id = %s
            RETURNING id;
            """, (disc.name, disc.artist, disc.year_of_release, disc.genre, disc.quantity, disc.id))
            row_count = _cursor.rowcount

        return row_count > 0

    async def delete(self, _id: str) -> Awaitable[bool]:
        async with self._connection.cursor() as _cursor:
            await _cursor.execute("""
            DELETE FROM discs WHERE id = %s;
            """, (_id,))
            row_count = _cursor.rowcount

        return row_count > 0
