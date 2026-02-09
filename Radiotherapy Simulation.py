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
        pass
    
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

def initialise_particles(number_of_particles):
    return {i : {"Position" : Vector3(0,0,0), "Rotation" : Vector3(0,0,0), "Energy Level" : energy} for i in range(number_of_particles)}

particles = initialise_particles(100)
print(particles[0]["Position"])

diameter = min(length,width,height)/2
centre = (nx/2, ny/2)