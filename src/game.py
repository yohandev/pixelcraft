from engine import *

from camera import Camera
from entity import Player
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
    player.walking = input[0] != 0
    player.facing = camera.screen_to_world(mouse[0], mouse[1])

    # damped follow player
    camera.x += (player.x - camera.x) * 0.10
    camera.y += (player.y - camera.y) * 0.05

    # physics
    player.y += player.vel

    # blocks to left and right of player
    left = [
        world[math.floor(player.x - 1), math.floor(player.y)],
        world[math.floor(player.x - 1), math.floor(player.y + 1)]
    ]
    right = [
        world[math.floor(player.x + 1), math.floor(player.y)],
        world[math.floor(player.x + 1), math.floor(player.y + 1)]
    ]
    # hit blocks?
    if True in (block.aabb().intersects(player.aabb()) for block in left):
        # snap
        player.x = math.floor(player.x - 1) + 1.2
        if input[0] > 0:
            player.x += input[0] * 0.1
    elif True in (block.aabb().intersects(player.aabb()) for block in right):
        # snap
        player.x = math.floor(player.x + 1) - 0.2
        if input[0] < 0:
            player.x += input[0] * 0.1
    else:
        player.x += input[0] * 0.1

    # block below player
    below = world[math.floor(player.x), math.floor(player.y - 0.75)]
    # is grounded?
    if below.aabb().intersects(player.aabb()):
        # snap to ground
        player.y = below.y + 1 + 0.65
        player.vel = 0
        # jump
        if input[1] == 1:
            player.vel = 0.325
    else:
        # gravity
        player.vel -= 0.025

    # -- begin render --
    background(0.5, 0.6, 0.8)
    camera.push_view()

    for block in camera.visible(world):
        block.draw()
    
    player.draw()
    
    camera.pop_view()
    # -- end render --

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

    # building
    mx, my = (math.floor(n) for n in camera.screen_to_world(mouse[0], mouse[1]))
    if world[mx, my] == 'air':
        world[mx, my] = 'stone'
    else:
        world[mx, my] = 'air'

def mouseup(x, y):
    mouse[0], mouse[1] = x, y
    player.swinging = False

def mousemove(x, y):
    mouse[0], mouse[1] = x, y

def mousedrag(x, y):
    mouse[0], mouse[1] = x, y