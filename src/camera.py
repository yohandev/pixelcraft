from engine import *

from world import World


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def render(self, world: World):
        min = self.x - width() // (2 * 80), self.y - height() // (2 * 80)
        max = self.x + width() // (2 * 80), self.y + height() // (2 * 80)

        cx, cy = width() / 2 - 40, height() / 2 - 40

        for x in range(int(min[0] - 2), int(max[0]) + 2):
            for y in range(int(min[1] - 2), int(max[1]) + 2):
                image(world[x, y].texture, (x - self.x) * 80 + cx, (y - self.y) * 80 + cy, 80)


