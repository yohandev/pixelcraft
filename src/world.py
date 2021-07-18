from blocks import *

class Chunk:
    size = 32
    area = 32 ** 2

    def __init__(self, x: int, y: int):
        self.tiles = [BlockAir()] * Chunk.area
        self.x = x
        self.y = y

    def __getitem__(self, pos):
        return self.tiles[pos[1] * Chunk.size + pos[0]]

    def __iter__(self):
        for i, block in enumerate(self.tiles):
            x = i % Chunk.size
            y = i // Chunk.size

            yield x, y, block