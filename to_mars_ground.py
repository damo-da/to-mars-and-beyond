#!/usr/bin/env python2

from __future__ import division, print_function

from headers import *
from visual import vector, dot
from math import cos, pi, sin, tan, acos
from constants import MASS_OF_MARS, RADIUS_OF_MARS, G
from matplotlib import pyplot as plt
from utils import get_total_energy, add_energy

from sys import stderr

rocket_pos = vector(1.30553e11, 1.86886e11, 0)
rocket_vel = vector(-14085.8, 9481.05, 0)
mars_pos = vector(1.30483e11, 1.86794e11, 0)
mars_vel = vector(-19791, 13813.6, 0)

# translate mars' pos and vel to 0
rocket_pos -= mars_pos
rocket_vel -= mars_vel

VELOCITY_RELATED = "vel-related"
ABSOLUTE = "absolute"
HORIZONTAL = "horizontal"

dt = 1
GRAPH = True
ZOOM = 0.027
SKIPS = 40

TIME_SKIP = 0
mass_of_rocket = 1

propulsions_done = []

propulsions = [
    {"type": ABSOLUTE, "magnitude": 10.0, "from":0, "duration": 7000, "color": "red"},
    {"type": VELOCITY_RELATED, "magnitude": -9.0, "from":2000, "duration":5000, "color": "black"},
    {"type": ABSOLUTE, "magnitude": 15.0, "from":6500, "duration": 1000, "color": "green"},
    {"type": VELOCITY_RELATED, "magnitude": -11.0, "from": 6000, "duration": 1800, "color": "aqua"},
    {"type": VELOCITY_RELATED, "magnitude": -2.1, "from": 7200, "duration": 1200, "color": "red"},
    {"type": ABSOLUTE, "magnitude": -3.0, "from": 8400, "duration": 900, "color": "pink"},
    {"type": VELOCITY_RELATED, "magnitude": -1.4, "from": 8400, "duration": 1000, "color": "brown"},
    {"type": VELOCITY_RELATED, "magnitude": -0.3, "from": 9200, "duration": 600, "color": "black"},
    {"type": VELOCITY_RELATED, "magnitude": -3.7, "from": 9100, "duration": 150, "color": "blue"},
    {"type": ABSOLUTE, "magnitude": -0.1, "from": 9150, "duration": 95, "color": "gray"},
    {"type": HORIZONTAL, "magnitude": -0.4, "from": 9150, "duration": 50, "color": "skyblue"}
]

def draw_mars_on_graph():
    if not GRAPH: return;

    plt.axes()

    val = RADIUS_OF_MARS / ZOOM
    plt.axis([-val, val, -val, val])

    circle = plt.Circle((0, 0), radius=RADIUS_OF_MARS, fc='y', fill=False)
    plt.gca().add_patch(circle)

    plt.scatter(0, 0, color="black")
    # plt.axis('scaled')
    # plt.show()

time = 0


draw_mars_on_graph()

plt.ion()

notified=False

last_height = 1e100
zoomed=False


frame = 0

color = "black"

while True:
    f_gravity = - G * MASS_OF_MARS * mass_of_rocket * rocket_pos/ rocket_pos.mag**3
    f_propulsion = vector()

    if not zoomed and time > 6500:
        val =  RADIUS_OF_MARS / (ZOOM * 17)
        plt.axis([-val, val, -val, val])
        SKIPS = 20

    for propulsion in propulsions:
        if propulsion['from'] < time < propulsion['from']+propulsion['duration']:
            if propulsion not in propulsions_done:
                propulsions_done.append(propulsion)
                if "color" in propulsion:
                    color = propulsion["color"]
                print("Applying propulsion {}".format(propulsion))

            direction = vector(1, 0, 0)

            if 'type' in propulsion and propulsion['type'] == ABSOLUTE:
                # print("ABSOLUTE")
                direction = - rocket_pos/rocket_pos.mag
            elif propulsion['type'] == VELOCITY_RELATED:
                direction = rocket_vel/rocket_vel.mag
            elif propulsion['type'] == HORIZONTAL:
                ortho_vector = rocket_pos /rocket_pos.mag
                direction = vector(ortho_vector.y, -ortho_vector.x)
            else:
                raise SystemError

            force = propulsion['magnitude'] * direction
            f_propulsion += force
        else:
            if not notified and time > propulsion['from']:
                print("PRopulsion stopped")
                notified = True
                # plt.pause(0.02)
    try:
        theta = acos(dot(rocket_vel, rocket_pos)/rocket_vel.mag / rocket_pos.mag )/pi
    except:
        pass

    # print("t= {0}, v={1:.0f}, h={2:.2f}, theta={3:.2f}".format(time, rocket_vel.mag, rocket_pos.mag-RADIUS_OF_MARS, theta))

    if rocket_pos.mag < RADIUS_OF_MARS:
        print("Rocket landed on ground with velocity: {0:.0f}".format(rocket_vel.mag))
        print("Total energy used: {}".format(get_total_energy()))
        with open("energy-used.tmp", "a") as f:
            f.write(str(get_total_energy()) + "\n")
        raw_input()
        exit(0)

    if rocket_pos.mag - RADIUS_OF_MARS > last_height:
        print("Warning, rocket going up", file=stderr)

    last_height = rocket_pos.mag - RADIUS_OF_MARS

    f_net = f_gravity + f_propulsion

    add_energy(f_net, rocket_vel, dt)

    rocket_vel += (f_net / mass_of_rocket) * dt

    rocket_pos += rocket_vel * dt

    # print(rocket_pos)

    time += dt

    frame += 1

    if time < TIME_SKIP: continue

    if frame > SKIPS:
        plt.scatter(rocket_pos.x, rocket_pos.y, color=color)

        plt.pause(0.01)

        frame = 0
