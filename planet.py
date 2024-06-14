import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math

class Planet:
    def __init__(self, radius, texture_file, rotation_speed, rotation_angle=45, position=(0.0, 0.0, 0.0), orbital_distance=0, rotation_angle_self=0.0, ring_texture_file=None, ring_inner_radius=0.0, ring_outer_radius=0.0):
        self.radius = radius 
        self.texture = self.load_texture(texture_file)
        self.rotation_speed = rotation_speed
        self.rotation_angle = rotation_angle   
        self.position = np.array(position)    
        self.orbital_distance = orbital_distance
        self.rotation_angle_self = rotation_angle_self
        self.ring_texture_file = ring_texture_file
        self.ring_texture = self.load_texture(ring_texture_file) if ring_texture_file else None
        self.ring_inner_radius = ring_inner_radius
        self.ring_outer_radius = ring_outer_radius

    def load_texture(self, texture_file):
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        img = Image.open(texture_file).transpose(Image.FLIP_TOP_BOTTOM)
        img_data = np.array(list(img.getdata()), np.uint8)      
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texture
    
    def shape(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor3f(1.0, 1.0, 1.0)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluSphere(quadric, self.radius, 32, 32)
        gluDeleteQuadric(quadric)
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_DEPTH_TEST)

    def draw_ring(self):
        if self.ring_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.ring_texture)
            glBegin(GL_QUAD_STRIP)
            for i in range(361):
                theta = math.radians(i)
                x = math.cos(theta)
                z = math.sin(theta)
                glTexCoord2f(0, 1)
                glVertex3f(self.ring_inner_radius * x, 0, self.ring_inner_radius * z)
                glTexCoord2f(1, 0)
                glVertex3f(self.ring_outer_radius * x, 0, self.ring_outer_radius * z)
            glEnd()
            glDisable(GL_TEXTURE_2D)

    def update_rotation(self):
        self.rotation_angle += abs(self.rotation_speed)
        self.rotation_angle_self += 0.5

    def apply_rotation(self):
        glRotatef(self.rotation_angle_self, 0, 1, 0)
        glRotatef(self.rotation_angle, 0, 1, 0)

    def calculate_orbital_position(self):
        y = 0.0
        z = self.orbital_distance * math.sin(math.radians(self.rotation_angle))
        x = self.orbital_distance * math.cos(math.radians(self.rotation_angle))
        return np.array([x, y, z])
    
    def combine_images(self, ring_image_path, planet_image_path, output_path):
        ring = Image.open(ring_image_path)
        planet = Image.open(planet_image_path)

        ring = ring.resize((int(planet.width * 1.5), int(planet.height * 1.5)), Image.ANTIALIAS)
        ring = ring.rotate(-10, expand=True)

        combined_image = Image.new('RGBA', ring.size, (0, 0, 0, 0))

        planet_position = ((ring.width - planet.width) // 2, (ring.height - planet.height) // 2)
        combined_image.paste(ring, (0, 0), ring)
        combined_image.paste(planet, planet_position, planet)

        combined_image.save(output_path)
        print(f"Combined image saved as '{output_path}'")
