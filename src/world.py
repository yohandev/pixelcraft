from typing import Tuple
from tile import *

import numpy
import noise


class World:
    """A container of tile data and entites for a single dimension
    
    Attributes:
        size    The numer of tiles in the x, y dimensions of the world
    """
    size = 6000, 800

    def min(self): return -(self.size[0] // 2), -(self.size[1] // 2)
    def max(self): return +(self.size[0] // 2), +(self.size[1] // 2)

    def __init__(self, registry: Tile.Registry):
        """Creates an empty world with default tile(id#0)"""
        self.tiles      = numpy.zeros(World.size, dtype=numpy.uint16)
        self.registry   = registry

    def __getitem__(self, pos: Tuple[int, int]):
        """Get the tile at the given position: x, y"""
        # decompose position
        x, y = pos
        # offset such that (0, 0) is the center of the world
        cx, cy = World.size[0] // 2, World.size[1] // 2
        # find tile metadata at position
        out = self.registry[self.tiles[x + cx, y + cy]]

        return Tile.Ref(out, x, y)

    def __setitem__(self, pos, item):
        """Set the tile at the given position: x, y"""
        x, y = pos[0] + World.size[0] // 2, pos[1] + World.size[1] // 2
        self.tiles[x, y] = self.registry[item].id

    def generate(self):
        dirt = self.registry['dirt'].id
        grass = self.registry['grass'].id
        stone = self.registry['stone'].id

        for x in range(self.size[0]):
            h = 400 + int(20 * noise.pnoise1(x * 0.01) - 10)
            
            hs = int(h * 0.995 + (5 * noise.pnoise1(x * 0.05) - 2.5))
            hs = min(hs, h)

            for y in range(hs, h):
                self.tiles[x, y] = dirt
            for y in range(hs):
                self.tiles[x, y] = stone
            self.tiles[x, h] = grass
