from engine import *

from world import World


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def render(self, world: World):
        px = 40

        min = self.x - width() // (2 * px), self.y - height() // (2 * px)
        max = self.x + width() // (2 * px), self.y + height() // (2 * px)

        cx, cy = width() / 2 - (px / 2), height() / 2 - (px / 2)

        for x in range(int(min[0] - 2), int(max[0]) + 2):
            for y in range(int(min[1] - 2), int(max[1]) + 2):
                image(world[x, y].texture, (x - self.x) * px + cx, (y - self.y) * px + cy, px)


