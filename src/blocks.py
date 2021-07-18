from engine import *
from util import *

from typing import List
from enum import Enum


class Block:
    name = "Missing"
    texture = "tiles/missing.png"        

class BlockAir(Block):
    name = "Air"
    texture = "tiles/air.png"

class BlockDirt(Block):
    name = "Dirt"
    texture = "tiles/dirt.png"

class BlockGrass(Block):
    name = "Grass"
    texture = "tiles/grass.png"

# class BlockWoodenPlanks(Block):
#     name = lambda self: BlockWoodenPlanks.names[self.variant]
#     texture = lambda self: BlockWoodenPlanks.textures[self.variant]
    
#     names = [
#         "Oak Wood Planks",
#         "Spruce Wood Planks",
#         "Birch Wood Planks"
#     ]
#     textures = [
#         "tiles/oak_wooden_planks.png",
#         "tiles/spruce_wooden_planks.png",
#         "tiles/birch_wooden_planks.png",
#     ]

class WoodVariant(Enum):
    oak = 1
    spruce = 2
    birch = 3
    jungle = 4
    dark_oak = 5

def init_blocks():
    for id, block in enumerate(Block.__subclasses__()):
        if isinstance(block.name, str):
            block.name = lambda _self: block.name
        if isinstance(block.texture, str):
            texture = load_image(block.texture)
            block.texture = lambda _self: texture
        try:
            block.textures = [load_image(path) for path in block.textures]
        except AttributeError:
            pass

        block.id = id