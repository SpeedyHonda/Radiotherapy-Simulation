# Imports
import numpy as np
import random
import matplotlib.pyplot as plt

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
        return self
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def move(self, direction, step):
        self.x += direction.x * step
        self.y += direction.y * step
        self.z += direction.z * step

    

# Water Phantom
length, width, height = float(input()), float(input()), float(input())
voxelSize = float(input())
nx, ny, nz = int(length / voxelSize), int(width / voxelSize), int(height / voxelSize)

dosages = np.zeros((nx, ny, nz), np.int64)
energy = float(input())

x = (np.arange(nx) + 0.5) * voxelSize - length / 2
y = (np.arange(ny) + 0.5) * voxelSize - width / 2
z = np.arange(nz) * voxelSize

start_position = Vector3(float(input()), float(input()), float(input()))
end_position = Vector3(float(input()), float(input()), float(input()))

print(dosages)
print(x)
print(y)
print(z)

def get_voxel_index(pos, x, y, z, voxelSize):
    ix = int((pos.x + length/2) / voxelSize)
    iy = int((pos.y + width/2) / voxelSize)
    iz = int(pos.z / voxelSize)
    return ix, iy, iz

def get_beam_position(beam_shape, length, width):
    if beam_shape == "circle":
        diameter = min(length, width) / 2
        radius = diameter / 2
        distance = random.random() * radius
        theta = random.random() * 2 * np.pi
        y = start_position.y + np.sin(theta) * distance
        x = start_position.x + np.cos(theta) * distance
    else:
        raise ValueError("Beam Shape is invalid")

    return x, y

def get_beam_direction(x, y, z):
    dir = Vector3(end_position.x - x, end_position.y - y, end_position.z - z)
    dir = dir.normalise()
    print(dir)
    return dir

def initialise_particles(number_of_particles, beam_type):
    particles = {}

    for i in range(number_of_particles):
        x0, y0 = get_beam_position(beam_type, length, width)
        z0 = start_position.z 

        particles[i] = {"Position": Vector3(x0, y0, z0), "Rotation": get_beam_direction(x0, y0, z0), "Energy Level": energy}

    return particles

def move_particles(p, dosages, x, y, z, voxelSize):
    step = voxelSize / 5
    energy_loss = 0.05

    nx, ny, nz = dosages.shape

    for i in p:
        pos = p[i]["Position"]
        dir = p[i]["Rotation"]
        E = p[i]["Energy Level"]

        while E > 0:
            pos.move(dir, step)
            ix, iy, iz = get_voxel_index(pos, length, width, height, voxelSize)

            if 0 <= ix < nx and 0 <= iy < ny and 0 <= iz < nz:
                dosages[ix, iy, iz] += 1
            else:
                break

            if 0 <= ix < nx and 0 <= iy < ny and 0 <= iz < nz:
                dosages[ix, iy, iz] += 1
            else:
                break

            E -= energy_loss

        p[i]["Energy Level"] = E

def show_dose_slice(dosages, axis="z", index=0):
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



particles = initialise_particles(100, "circle")
move_particles(particles, dosages, x, y, z, voxelSize)
slice = int(input("What index of slice do you want? "))
axis = input("What axis do you want it taken from? ")

show_dose_slice(dosages, axis, slice)



