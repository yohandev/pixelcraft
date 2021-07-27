from engine import *
from physics import Aabb


class Tile:
    """Data about a type of tile"""

    # The size, in pixels, of a single tile. Size in world units is 1x1
    SIZE = 40

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

    class Collider(enum.Enum):
        """Collision behaviours for a tile"""
        VOID = 0
        FULL = 1
        HALF_TOP = 2
        HALF_BTM = 3

    class Ref:
        """A reference to a specific tile, containing its metadata and position"""
        def __init__(self, tile, x: int, y: int):
            self.tile = tile
            self.x = x
            self.y = y
        
        def draw(self):
            """Renders self in global screen coordinates"""
            image(self.tile.texture, self.x, self.y, 1)

        def aabb(self):
            """Get this block's bounding box"""
            if self.tile.collide == Tile.Collider.FULL:
                return Aabb(self.x + 0.5, self.y + 0.5, 1, 1)
            elif self.tile.collide == Tile.Collider.VOID:
                return Aabb(self.x + 0.5, self.y + 0.5, 0, 0)
            elif self.tile.collide == Tile.Collider.HALF_BTM:
                return Aabb(self.x + 0.5, self.y + 0.25, 1, 0.5)
            elif self.tile.collide == Tile.Collider.HALF_TOP:
                return Aabb(self.x + 0.5, self.y + 0.75, 1, 0.5)

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
