from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from PIL import Image

import numpy
import os

class App:
    def load_texture(self, path: str):
        # absolute path
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, path)
        # open the image
        img = Image.open(filename).convert('RGBA')
        # extract dimensions
        width, height = img.size
        # extract pixel data
        pixels = numpy.array(list(img.getdata()), numpy.uint8)

        tex = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, tex)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
        
        return tex

    def resize(self, width: int, height: int):
        """Resize the application window and set the projection
        matrix appropriately"""
        glutReshapeWindow(width, height)

        glLoadIdentity()
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()
    def fill_col(self, r: float, g: float, b: float):
        """Sets the fill colour of vertices for subsequent
        draw calls"""
        glDisable(GL_TEXTURE_2D)
        glColor3f(r, g, b)
    def fill_tex(self, tex):
        """Sets the fill texture of vertices for subsequent
        draw calls"""
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBindTexture(GL_TEXTURE_2D, tex)
    def rect(self, x: float, y: float, w: float, h: float = None):
        """Draws a rectangle, or a square if height isn't provided"""
        h = h if h != None else w

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

class Sketch:
    def run(self):
        """Takes over the main thread and triggers the game
        loop for this application, returning whenever the window
        is closed."""
        app = App()

        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutCreateWindow(self.name())

        def on_draw():
            # clear swap buffer...
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # ...perform draw logic...
            self.on_draw(app)
            # ...then swap buffers
            glutSwapBuffers()
        def on_tick():
            # this could be done using a lambda but eh.
            self.on_tick(app)

        glutDisplayFunc(on_draw)
        glutIdleFunc(on_tick)

        app.resize(1000, 800)
        self.on_start(app)

        glutMainLoop()

    def name(self) -> str:
        """Get the name of this sketch"""
        return ""
    def on_start(self, app: App):
        """Called on app startup"""
        pass
    def on_tick(self, app: App):
        """Called once a frame before rendering"""
        pass
    def on_draw(self, app: App):
        """Called when render calls should be made"""
        pass        