class Disc:
    """Represents a disc in stock."""

    id: str
    name: str
    artist: str
    year_of_release: int
    genre: str
    quantity: int

    def __init__(self, id: str, name: str, artist: str, year_of_release: int, genre: str, quantity: int):
        self.id = id
        self.name = name
        self.artist = artist
        self.year_of_release = year_of_release
        self.genre = genre
        self.quantity = quantity
