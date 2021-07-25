from typing import Tuple
from engine import *

from world import World
from tile import Tile


class Camera:
    """A conversion layer between world coordinates and screen coordinates"""
    def __init__(self):
        """Initialize a camera with position (0, 0), in world coordinates"""
        self.x = 0
        self.y = 0

    def world_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """Converts a world coordinate to its window-relative pixel coordinate"""
        # offset from origin to center of screen
        cx, cy = width() / 2, height() / 2
        # world coordinate relative to the camera
        dx, dy = x - self.x, y - self.y

        return dx * Tile.SIZE + cx, dy * Tile.SIZE + cy

    def screen_to_world(self, x: float, y: float) -> Tuple[float, float]:
        """Converts a window-relative pixel coordinate to its world coordinate"""
        # offset from origin to center of screen
        cx, cy = width() / 2, height() / 2
        # world coordinate relative to the camera
        dx, dy = (x - cx) / Tile.SIZE, (y - cy) / Tile.SIZE

        return dx + self.x, dy + self.y

    def visible(self, world: World):
        """Yields all the blocks within `world` that are visible to this camera"""
        # world coordinate for what *shouldn't* be culled
        min, max = self.screen_to_world(0, 0), self.screen_to_world(width(), height())

        # yield cartesian product
        for x in range(math.floor(min[0]), math.ceil(max[0])):
            for y  in range(math.floor(min[1]), math.ceil(max[1])):
                yield world[x, y]

    def push_view(self):
        """Push the view matrix for this camera"""
        push_matrix()
        # new position of origin
        dx, dy = self.world_to_screen(0, 0)
        # translate very successive draw calls
        translate(dx, dy)

    def pop_view(self):
        """Pop the view matrix for this camera"""
        pop_matrix()