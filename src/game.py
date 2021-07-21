from engine import *

from camera import Camera
from world import World
from tile import Tile


camera = None
world = None

input = [0, 0]

def setup():
    global camera, world

    rename('pixelcraft')
    resize(1000, 800)

    camera = Camera()
    world = World(Tile.Registry('data/tiles.toml'))

    world.generate()
    world[0, 0] = 'grass'

def draw():
    camera.x += input[0] * 0.1
    camera.y += input[1] * 0.1

    background(0.5, 0.6, 0.8)

    camera.render(world)


def keydown(key):
    global input

    # arrow Keys
    if key == 100:   # right
        input[0] = -1
    elif key == 101: # up
        input[1] = 1
    elif key == 102: # left
        input[0] = 1
    elif key == 103: # down
        input[1] = -1

def keyup(key):
    global input

    # arrow Keys
    if key == 100:   # right
        input[0] = max(0, input[0])
    elif key == 101: # up
        input[1] = min(0, input[1])
    elif key == 102: # left
        input[0] = min(0, input[0])
    elif key == 103: # down
        input[1] = max(0, input[1])