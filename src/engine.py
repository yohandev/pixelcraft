from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy
import os


def run(sketch):
    """Takes over the main thread and triggers the game
    loop for this application, returning whenever the window
    is closed."""

    # initialize GL(UT)
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow(sketch.name())

    # default size
    resize(1000, 800)

    # wrap over sketch's draw function
    def sketch_draw():
        # clear swap buffer...
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # ...perform draw logic...
        sketch.draw()
        # ...then swap buffers
        glutSwapBuffers()

    # set callbacks
    glutDisplayFunc(sketch_draw)
    glutIdleFunc(sketch_draw)
    # start callback
    sketch.setup()

    # begin game loop
    glutMainLoop()

def resize(width: int, height: int):
    """Resize the application window and set the projection
    matrix appropriately"""
    # set window size
    glutReshapeWindow(width, height)

    # reset projection matrix
    glLoadIdentity()
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

class Image:
    """Wrapper over an OpenGL texture2D"""
    def __init__(self, path: str, args: tuple):
        """Loads the image at the given *absolute* path into
        GPU memory"""

        from PIL import Image

        # open the image
        img = Image.open(path).convert('RGBA')
        # extract dimensions
        width, height = img.size
        # extract pixel data
        pixels = numpy.array(list(img.getdata()), numpy.uint8)

        # create texture on GPU
        inner = glGenTextures(1)

        # assign texture parameters
        glBindTexture(GL_TEXTURE_2D, inner)

        # wrap
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # mag/min filters
        if 'linear' in args:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        else:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        # load pixels in
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
        
        # save metadata in self
        self.inner = inner
        self.width = width
        self.height = height

def load_image(path: str, *args) -> Image:
    """Loads an image given its path relative to the /res folder.
    Argument `args` accepts:
        - "linear"
        - "nearest"
    """
    # absolute path
    root = os.path.dirname(__file__)
    path = os.path.join(root, "../res", path)

    return Image(path, args)

def image(img: Image, x: float, y: float, w: float = None, h: float = None):
    """Draws the given image at the given position. If both width and
    height arguments are ommited, the image's original size is used.
    If only height is ommited, image aspect ratio is preserved to match
    the given width."""
    # optional arguments
    w = w if w != None else img.width
    h = h if h != None else (img.height / img.width) * w

    # enable textures
    if image.bound == None:
        glEnable(GL_TEXTURE_2D)
    # don't rebind unnecessarily
    if image.bound is not img:
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBindTexture(GL_TEXTURE_2D, img.inner)
        image.bound = img
    
    # draw a rectangle with texture
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(x, y)
    glTexCoord2f(1, 1)
    glVertex2f(x + w, y)
    glTexCoord2f(1, 0)
    glVertex2f(x + w, y + h)
    glTexCoord2f(0, 0)
    glVertex2f(x, y + h)
    glEnd()
image.bound = None