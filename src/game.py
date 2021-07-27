from engine import *

from camera import Camera
from entity import Player
# from player import Player
from world import World
from tile import Tile


camera = None
player = None
world = None

input = [0, 0]
mouse = [0, 0]


def setup():
    global camera, player, world

    rename('pixelcraft')
    resize(1000, 800)

    camera = Camera()
    player = Player()
    world = World(Tile.Registry('data/tiles.toml'))

    world.generate()

def draw():
    player.x += input[0] * 0.1
    player.y += input[1] * 0.1
    player.walking = input[0] != 0

    background(0.5, 0.6, 0.8)

    # gravity
    # player.y -= 0.5
    # below = round(player.x), math.floor(player.y) - 1
    # if player.aabb().intersects(world[below].aabb(below[0], below[1])):
    #     player.y = below[1] + 2

    # if input[0] == 0:
    #     player.state &= ~Player.State.WALKING
    #     player.state |= Player.State.IDLE
    # else:
    #     player.state &= ~Player.State.IDLE
    #     player.state |= Player.State.WALKING

    camera.x, camera.y = player.x, player.y

    # -- begin render --
    camera.push_view()

    for block in camera.visible(world):
        block.draw()
    
    player.draw()
    
    camera.pop_view()
    # -- end render --

    # player.render(width() / 2, height() / 2, look[0], look[1])
    player.facing = camera.screen_to_world(mouse[0], mouse[1])

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
    mouse[0], mouse[1] = x, y
    player.swinging = True

def mouseup(x, y):
    mouse[0], mouse[1] = x, y
    player.swinging = False

def mousemove(x, y):
    mouse[0], mouse[1] = x, y

def mousedrag(x, y):
    mouse[0], mouse[1] = x, y