from engine import *

from camera import Camera
from player import Player
from world import World
from tile import Tile


camera = None
player = None
world = None

input = [0, 0]
look = [0, 0]

def setup():
    global camera, player, world

    rename('pixelcraft')
    resize(1000, 800)

    camera = Camera()
    player = Player()
    world = World(Tile.Registry('data/tiles.toml'))

    world.generate()
    world[0, 0] = 'grass'

def draw():
    camera.x += input[0] * 0.1
    camera.y += input[1] * 0.1

    background(0.5, 0.6, 0.8)

    if input[0] == 0:
        player.state &= ~Player.State.WALKING
        player.state |= Player.State.IDLE
    else:
        player.state &= ~Player.State.IDLE
        player.state |= Player.State.WALKING

    camera.render(world)
    player.render(look)


def keydown(key):
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
    # arrow Keys
    if key == 100:   # right
        input[0] = max(0, input[0])
    elif key == 101: # up
        input[1] = min(0, input[1])
    elif key == 102: # left
        input[0] = min(0, input[0])
    elif key == 103: # down
        input[1] = max(0, input[1])

def mousedown(x, y):
    look[0], look[1] = x, y
    player.state |= Player.State.ATTACKING

def mouseup(x, y):
    look[0], look[1] = x, y
    player.state &= ~Player.State.ATTACKING

def mousemove(x, y):
    look[0], look[1] = x, y

def mousedrag(x, y):
    look[0], look[1] = x, y