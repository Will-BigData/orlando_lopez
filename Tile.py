class Tile:
    type: str
    prev = []
    next = []
    def __init__(self, type):
        self.type = type
        self.next = []
        self.prev = []


