# Imports
import numpy as np
import random

# Classes
class Vector3():
    def __init__(self, x_input, y_input, z_input):
        self.x = x_input
        self.y = y_input
        self.z = z_input

    def normalise(self):
        sum = (self.x**2 + self.y**2 + self.z**2)**(1/2)
        self.x /= sum
        self.y /= sum
        self.z /= sum
    
    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"
    
# Water Phantom
length, width, height = float(input()), float(input()), float(input())
voxelSize = float(input())
nx, ny, nz = int(length / voxelSize), int(width / voxelSize), int(height / voxelSize)

dosages = np.zeros((nx, ny, nz), np.int64)
energy = float(input())

x = (np.arange(nx) + 0.5) * voxelSize - length / 2
y = (np.arange(ny) + 0.5) * voxelSize - width / 2
z = (np.arange(nz) + 0.5) * voxelSize

# We are taking the 3D space to be comprised of many small cubes of size voxelSize

print(dosages)
print(x)
print(y)
print(z)

def get_beam_position(beam_shape, length, width):
    if beam_shape == "circle":
        diameter = min(length, width) / 2
        radius = diameter / 2
        distance = random.random() * radius
        theta = random.random() * 2 * np.pi
        y = np.sin(theta) * distance
        x = np.cos(theta) * distance
    else:
        raise ValueError("Beam Shape is invalid")

    return x, y

def initialise_particles(number_of_particles, beam_type):
    particles = {}

    for i in range(number_of_particles):
        x0, y0 = get_beam_position(beam_type, length, width)
        z0 = 0 

        particles[i] = {"Position": Vector3(x0, y0, z0), "Rotation": Vector3(0, 0, 1), "Energy Level": energy}

    return particles


particles = initialise_particles(100, "circle")
print(particles[0]["Position"])

# I am defining rotation in a Vector3 as x degrees about the x axis, y degrees about the y axis and z degrees about the z axis