#!/usr/bin/env python2

from __future__ import division, print_function

from headers import *
from visual import vector
from constants import MASS_OF_MARS, RADIUS_OF_MARS, G
from matplotlib import pyplot as plt

rocket_pos = vector(1.30553e11, 1.86886e11, 0)
rocket_vel = vector(-14085.8, 9481.05, 0)
mars_pos = vector(1.30483e11, 1.86794e11, 0)
mars_vel = vector(-19791, 13813.6, 0)

# translate mars' pos and vel to 0
rocket_pos -= mars_pos
rocket_vel -= mars_vel

dt = 0.1

mass_of_rocket = 1

time = 0

plt.ion()
while True:
    force = - G * MASS_OF_MARS * mass_of_rocket * rocket_pos/ rocket_pos.mag**3

    rocket_vel += (force / mass_of_rocket) * dt

    rocket_pos += rocket_vel * dt

    print(rocket_pos)

    time += dt

    plt.scatter(time, rocket_pos.mag)

    plt.pause(0.1)
