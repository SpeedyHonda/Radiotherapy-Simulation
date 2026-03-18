# Imports
import numpy as np
import random
import matplotlib.pyplot as plt

# Classes
class Vector3(): # Essentially just a tuple of 3 floats but also has some specialised functionality
    # This is just for ease of use, being able to initialise a vector as Vector3(x, y, z)
    def __init__(self, x_input, y_input, z_input):
        self.x = x_input
        self.y = y_input
        self.z = z_input

    # Converts the vector into a unit vector (meaning the magnitude of the vector is 1 unit)
    def normalise(self):
        sum = (self.x**2 + self.y**2 + self.z**2)**(1/2)
        self.x /= sum
        self.y /= sum
        self.z /= sum
        return self
    
    # This is entirely for the sake of debugging so I can more easily understand how the particles are moving as we can print their exact positions and directions more easily
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    # Adds a bit to each of the x, y and z. Quite poorly written to be honest, but let's just call it specialised
    def move(self, direction, step):
        self.x += direction.x * step
        self.y += direction.y * step
        self.z += direction.z * step

# The Simulation Space
length, width, height = float(input()), float(input()), float(input())
voxelSize = float(input())
nx, ny, nz = int(length / voxelSize), int(width / voxelSize), int(height / voxelSize)

dosages = np.zeros((nx, ny, nz), np.int64)
energy = float(input())

x = (np.arange(nx) + 0.5) * voxelSize - length / 2
y = (np.arange(ny) + 0.5) * voxelSize - width / 2
# z = np.arange(nz) * voxelSize
z = (np.arange(nz) + 0.5) * voxelSize - height / 2

start_position = Vector3(0, 0, 0)
end_position = Vector3(0, 0, 0)

# Functions
def get_voxel_index(pos, voxelSize): # Given the position, finds the nearest voxel to access
    ix = int((pos.x + length/2) / voxelSize)
    iy = int((pos.y + width/2) / voxelSize)
    #iz = int(pos.z / voxelSize)
    iz = int((pos.z + height/2) / voxelSize)
    return ix, iy, iz

def get_beam_position(beam_shape, length, width): # Gets the particles position accounting for a bit of randomness
    if beam_shape == "circle":
        diameter = min(length, width) 
        radius = diameter / 2
        distance = random.random() * radius
        theta = random.random() * 2 * np.pi
        y = start_position.y + np.sin(theta) * distance
        x = start_position.x + np.cos(theta) * distance
    else:
        raise ValueError("Beam Shape is invalid")

    return x, y

def get_beam_direction(x, y, z): # Gets the direction of the particle as a unit vector
    dir = Vector3(end_position.x - x, end_position.y - y, end_position.z - z)
    dir = dir.normalise()
    return dir

def initialise_particles(number_of_particles, beam_type): # Creating a dictionary of particles. It has the ID number, attached with another dictionary with position, rotation and energy level
    particles = {}

    for i in range(number_of_particles):
        x0, y0 = get_beam_position(beam_type, length, width)
        z0 = start_position.z 

        particles[i] = {"Position": Vector3(x0, y0, z0), "Rotation": get_beam_direction(x0, y0, z0), "Energy Level": energy}

    return particles

def move_particles(p, dosages, voxelSize): # While we still have particles that have energy and are within the bounds of the simulation space, we move them according to their movement vector, then decrease its energy and add some to the voxel
    step = voxelSize / 5
    energy_loss = 0.05

    nx, ny, nz = dosages.shape

    for i in p:
        pos = p[i]["Position"]
        dir = p[i]["Rotation"]
        E = p[i]["Energy Level"]

        while E > 0:
            pos.move(dir, step)
            ix, iy, iz = get_voxel_index(pos, voxelSize)

            if 0 <= ix < nx and 0 <= iy < ny and 0 <= iz < nz:
                dosages[ix, iy, iz] += 1
            else:
                break

            E -= energy_loss

        p[i]["Energy Level"] = E

def show_dose_slice(dosages, axis="z", index=0): # This displays a *basic* heatmap describing the dose distribution. Please consider that the x and y heatmaps are vertically flipped
    if axis == "z":
        slice2d = dosages[:, :, index]
    elif axis == "y":
        slice2d = dosages[:, index, :]
    elif axis == "x":
        slice2d = dosages[index, :, :]

    plt.imshow(slice2d.T, cmap="inferno", origin="lower")
    plt.colorbar(label="Dose (a.u.)")
    plt.title(f"Dose slice along {axis}-axis at index {index}")
    plt.xlabel("Voxel index")
    plt.ylabel("Voxel index")
    plt.show()

# Running
beams = int(input("Enter how many beams you want: "))
for i in range(beams):
    start_position = Vector3(float(input()), float(input()), float(input()))
    end_position = Vector3(float(input()), float(input()), float(input()))
    particles = initialise_particles(100, "circle")
    move_particles(particles, dosages, voxelSize)

slice = int(input("What index of slice do you want? "))
axis = input("What axis do you want it taken from? ")

show_dose_slice(dosages, axis, slice)

# REMEMBER VOXEL SIZES MUST BE INTEGERS
# 10 10 10 1 10 0 0 0 0 0 10 5 x
# 50 50 50 1 6 0 0 0 0 0 50 25 x
# 50 50 50 1 6 0 0 0 0 0 50 25 z

