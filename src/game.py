from engine import *

from blocks import init_blocks
from camera import Camera
from world import Chunk


camera = Camera()
chunk = Chunk(0, 0)

def name(): return "pixelcraft"

def setup():
    resize(1000, 800)
    init_blocks()

def draw():
    camera.render(chunk)
