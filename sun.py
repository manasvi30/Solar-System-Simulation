from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np

class Sun:
    def __init__(self, texture_file=None):
        self.texture = self.load_texture(texture_file)
    
    def load_texture(self, texture_file):
        img = Image.open(texture_file)
        img_data = np.array(list(img.getdata()), np.uint8)
        texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture

    def shape(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluSphere(quadric, 1.0, 50, 50)  # Radius 1.0 for Sun
        gluDeleteQuadric(quadric)
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_TEXTURE_2D)
