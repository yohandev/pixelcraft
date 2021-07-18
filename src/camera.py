from engine import *

from world import Chunk


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def render(self, chunk: Chunk):
        dx, dy = chunk.x * Chunk.size, chunk.y * Chunk.size
        cx, cy = width() / 2, height() / 2

        for x, y, block in chunk:
            # TODO frustrum culling
            image(block.texture(), cx + (dx + x) * 80, cy + (dy + y) * 80)