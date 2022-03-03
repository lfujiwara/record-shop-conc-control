class DiscDto:
    """Disc value object."""
    id: str
    name: str
    artist: str
    year_of_release: int
    genre: str
    quantity: int

    def __init__(self, _id: str, name: str, artist: str, year_of_release: int, genre: str, quantity: int):
        self.id = _id
        self.name = name
        self.artist = artist
        self.year_of_release = year_of_release
        self.genre = genre
        self.quantity = quantity
