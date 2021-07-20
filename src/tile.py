from engine import *

from enum import Enum

class Tile:
    """Data about a type of tile"""

    class Registry:
        """A registry of tile data"""
        def __init__(self, tiledata: str):
            """Load a tile registry given the path to a TOML tile data file"""
            self.tiles = [Tile(data, id) for id, data in enumerate(load_toml(tiledata)['tile'])]
            self.tiles_rev = {tile.name.replace(' ', '_').lower(): tile for tile in self.tiles}

        def __getitem__(self, key):
            # get by string ID
            if isinstance(key, str): return self.tiles_rev[key.replace(' ', '_').lower()]
            # get by numeric ID
            else: return self.tiles[key]

    class Collider(Enum):
        """Collision behaviours for a tile"""
        VOID = 0
        FULL = 1
        HALF_TOP = 2
        HALF_BTM = 3

    def __init__(self, toml: dict, id: int):
        # -- required fields --
        name    = toml['name']
        texture = toml['texture']
        collide = toml['collide']
        
        # -- field validation --
        name    = str(name)
        texture = load_image('textures/tiles/' + texture)
        collide = Tile.Collider[str(collide).upper()]

        # -- save fields --
        self.name    = name
        self.texture = texture
        self.collide = collide
        self.id      = id
