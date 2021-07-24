from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy
import enum
import math
import toml
import os


def run(sketch):
    """Takes over the main thread and triggers the game
    loop for this application, returning whenever the window
    is closed."""

    # initialize GL(UT)
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutCreateWindow("")

    # default size
    resize(1000, 800)
    # enable alpha blending
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # wrap over sketch's draw function
    def sketch_draw():
        # perform draw logic...
        sketch.draw()
        # ...then swap buffers
        glutSwapBuffers()
    def sketch_keydown(k, _x, _y):
        sketch.keydown(k)
    def sketch_keyup(k, _x, _y):
        sketch.keyup(k)
    def sketch_mousemove(x, y):
        sketch.mousemove(x, height() - y)

    # set callbacks
    glutDisplayFunc(sketch_draw)
    glutIdleFunc(sketch_draw)
    glutSpecialFunc(sketch_keydown)
    glutSpecialUpFunc(sketch_keyup)
    glutPassiveMotionFunc(sketch_mousemove)
    # start callback
    sketch.setup()

    # begin game loop
    glutMainLoop()

def resize(w: int, h: int):
    """Resize the application window and set the projection
    matrix appropriately"""
    # set window size
    glutReshapeWindow(w, h)

    # reset projection matrix
    glLoadIdentity()
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, w, 0.0, h, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

    # store wize
    width.value = w
    height.value = h

def rename(title: str):
    """Rename the window with the given title"""
    glutSetWindowTitle(title)

def width() -> int: return width.value
def height() -> int: return height.value

def load_toml(path):
    """Loads a TOML file given its path relative to /res"""
    # absolute path
    root = os.path.dirname(__file__)
    path = os.path.join(root, "../res", path)

    return toml.load(path)


def background(r: float, g: float, b: float, a: float = 1.0):
    """Clears the screen using the given colour"""
    glClearColor(r, g, b, a)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

def pushMatrix(): glPushMatrix()
def popMatrix(): glPopMatrix()
def translate(x: float, y: float): glTranslatef(x, y, 0)
def rotate(deg: float): glRotatef(deg, 0, 0, 1)
def scale(x: float, y: float): glScalef(x, y, 1)

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
        # unbind
        glBindTexture(GL_TEXTURE_2D, 0)

        # save metadata in self
        self.inner = inner
        self.width = width
        self.height = height
        self.path = path

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
        glColor3f(1.0, 1.0, 1.0)
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

def fill(r: float, g: float, b: float):
    """Sets the fill colour for subsequent calls"""
    if image.bound != None:
        # disable texturing
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
        image.bound = None
    # set vertex colour
    glColor3f(r, g, b)

def rect(x: float, y: float, w: float, h: float = None):
    """Draws a rectangle, or square(if argument h is omitted)
    at the given x, y position"""
    # optional arguments
    h = h if h != None else w

    # draw a rectangle without texture
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()