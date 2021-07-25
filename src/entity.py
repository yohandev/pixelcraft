from engine import *
from util import *

from tile import Tile


class Entity:
    """Base class for all entities"""
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self, frame: float):
        """Draws this entity at its position, given its frame in the walk cycle"""
        pass

class Player(Entity):
    def __init__(self):
        super().__init__()

        # block to look at
        self.facing = 0, 0
    
    @lazy
    def textures(): return {
        'head': load_image('textures/player/head.png'),
        'body': load_image('textures/player/body.png'),
        'arm':  load_image('textures/player/arm.png'),
        'leg':  load_image('textures/player/leg.png'),
    }

    def draw(self, frame: float):
        # get body part textures
        img = Player.textures()

        # head x, y
        hx, hy = self.x, self.y + 0.75
        # mouse x, y
        mx, my = self.facing
        # head rotation
        facing = math.degrees(math.atan2(my - hy, mx - hx))
        flip = 1
        if abs(facing) > 90:
            facing = -facing + 180
            flip = -1
        # limbs rotation
        swing = 45 * math.sin(frame)

        print(facing)

        push_matrix()

        # move to position
        translate(self.x, self.y)
        # undo the world->screen scaling
        scale(1 / Tile.SIZE, 1 / Tile.SIZE)

        image(img['leg'], pivot = (0.5, 1), angle = +swing)
        image(img['leg'], pivot = (0.5, 1), angle = -swing)
        image(img['arm'], y = img['body'].h, pivot = (0.5, 1), angle = -swing)
        image(img['body'], pivot = (0.5, 0))
        image(img['head'], y = img['body'].h, pivot = (0.5, 0), angle = facing, scaling = (flip, 1))
        image(img['arm'], y = img['body'].h, pivot = (0.5, 1), angle = +swing)

        pop_matrix()