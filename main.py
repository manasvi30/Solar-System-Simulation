import math
import numpy as np
import pygame, sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from planet import Planet

magnification_big = 20
magnification_small = 5

# Planets Definitions

# Definition of Sun
sun_radius = 2
sun_texture = "D:/Solar/Textures/Sun.jpg"
sun_position = (0, 0, 0)

# Definition of mercury
mercury_radius = 0.015 * magnification_big
mercury_texture = "D:/Solar/Textures/mercury.jpg"
mercury_distance = 5
mercury_position = (mercury_distance, 0, 0)
mercury_speed = 1.0

# Definition of venus
venus_radius = 0.024 * magnification_big
venus_texture = "D:/Solar/Textures/y.jpg"
venus_distance = 6
venus_position = (venus_distance, 0, 0)
venus_speed = 0.8

# Definition of earth
earth_radius = 0.05 * magnification_big
earth_texture = "D:/Solar/Textures/earth.jpg"
earth_distance = 7
earth_position = (earth_distance, 0, 0)
earth_speed = 0.7

# Definition of mars
mars_radius = 0.029 * magnification_big
mars_texture = "D:/Solar/Textures/mars.jpg"
mars_distance = 8
mars_position = (mars_distance, 0, 0)
mars_speed = 0.6

# Definition of jupiter
jupiter_radius = 0.290 * magnification_small
jupiter_texture = "D:/Solar/Textures/jupiter.jpg"
jupiter_distance = 11.5
jupiter_position = (jupiter_distance, 0, 0)
jupiter_speed = 0.48

# Definition of saturn
saturn_radius = 0.190 * magnification_small
saturn_ring_texture = "D:/Solar/Textures/saturn_ring.png"
saturn_texture = "D:/Solar/Textures/saturn.jpg"
saturn_distance = 12.5
saturn_position = (saturn_distance, 0, 0)
saturn_speed = 0.4
saturn_ring_inner_radius = saturn_radius * 1.2
saturn_ring_outer_radius = saturn_radius * 1.8

# Definition of uranus
uranus_radius = 0.110 * magnification_small
uranus_texture = "D:/Solar/Textures/uranus.jpg"
uranus_distance = 13.5
uranus_position = (uranus_distance, 0, 0)
uranus_speed = 0.36

# Definition of neptune
neptune_radius = 0.110 * magnification_small
neptune_texture = "D:/Solar/Textures/neptune.jpg"
neptune_distance = 14.5
neptune_position = (neptune_distance, 0, 0)
neptune_speed = 0.33

def set_projection(display):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.0, 15.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    camera_distance = 15
    camera_pos = np.array([0, 10, camera_distance])
    target_point = np.array([0.0, 0.0, 0.0])
    up_vector = np.array([0.0, 1.0, 0.0])

    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], target_point[0], target_point[1], target_point[2], up_vector[0], up_vector[1], up_vector[2])

def milky_way():
    glPointSize(2.0)
    glBegin(GL_POINTS)
    num_stars = 50
    for _ in range(num_stars):
        brightness = np.random.uniform(0.5, 1.0)
        glColor3f(brightness, brightness, brightness)
        x = np.random.uniform(-20.0, 20.0)
        y = np.random.uniform(-20.0, 20.0)
        z = np.random.uniform(-20.0, 20.0)
        glVertex3f(x, y, z)
    glEnd()

def main():
    pygame.init()
    display = (1250, 650)
    pygame.display.set_caption('3D Solar System Simulation')
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    set_projection(display)

    sun = Planet(sun_radius, sun_texture, 0, position=sun_position)
    mercury = Planet(mercury_radius, mercury_texture, mercury_speed, position=mercury_position, orbital_distance=mercury_distance)
    venus = Planet(venus_radius, venus_texture, venus_speed, position=venus_position, orbital_distance=venus_distance)
    earth = Planet(earth_radius, earth_texture, earth_speed, position=earth_position, orbital_distance=earth_distance)
    mars = Planet(mars_radius, mars_texture, mars_speed, position=mars_position, orbital_distance=mars_distance)
    jupiter = Planet(jupiter_radius, jupiter_texture, jupiter_speed, position=jupiter_position, orbital_distance=jupiter_distance)
    saturn = Planet(saturn_radius, saturn_texture, saturn_speed, position=saturn_position, orbital_distance=saturn_distance, ring_texture_file=saturn_ring_texture, ring_inner_radius=saturn_ring_inner_radius, ring_outer_radius=saturn_ring_outer_radius)
    uranus = Planet(uranus_radius, uranus_texture, uranus_speed, position=uranus_position, orbital_distance=uranus_distance)
    neptune = Planet(neptune_radius, neptune_texture, neptune_speed, position=neptune_position, orbital_distance=neptune_distance)

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        milky_way()

        for planet in planets:
            planet.update_rotation()
            planet.position = planet.calculate_orbital_position()

        for planet in planets:
            glPushMatrix()
            glTranslatef(*planet.position)
            planet.apply_rotation()
            planet.shape()
            if planet == saturn:
                planet.draw_ring()
            glPopMatrix()

        error = glGetError()
        if error != GL_NO_ERROR:
            print(f"OpenGL Error: {error}")

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == '__main__':
    main()
