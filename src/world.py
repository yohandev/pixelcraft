from tile import *

import numpy as np


class World:
    """A container of tile data and entites for a single dimension
    
    Attributes:
        size    The numer of tiles in the x, y dimensions of the world
    """
    size = 6000, 800

    def __init__(self, registry: Tile.Registry):
        """Creates an empty world with default tile(id#0)"""
        self.tiles      = np.ones(World.size, dtype=np.uint16)
        self.registry   = registry

    def __getitem__(self, pos):
        """Get the tile at the given position: x, y"""
        x, y = pos[0] + World.size[0] // 2, pos[1] + World.size[1] // 2
        return self.registry[self.tiles[x, y]]

    def __setitem__(self, pos, item):
        """Set the tile at the given position: x, y"""
        x, y = pos[0] + World.size[0] // 2, pos[1] + World.size[1] // 2
        self.tiles[x, y] =  np.uint16(self.registry[item].id)
