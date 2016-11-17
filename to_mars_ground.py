#!/usr/bin/env python2

from __future__ import division, print_function

from headers import *
from time import sleep
from visual import vector, dot
from math import cos, pi, sin, tan, acos
from constants import MASS_OF_MARS, RADIUS_OF_MARS, G
from matplotlib import pyplot as plt
from utils import get_total_energy, add_energy

from sys import stderr

rocket_pos = vector(-5.47454e+10, -2.21231e+11, 0)
rocket_vel = vector(21512, -8339.19, 0)
mars_pos = vector(-5.46831e+10, -2.21027e+11, 0)
mars_vel = vector(23445.7, -5800.21, 0)

# translate mars' pos and vel to 0
rocket_pos -= mars_pos
rocket_vel -= mars_vel

VELOCITY_RELATED = "vel-related"
ABSOLUTE = "absolute"
HORIZONTAL = "horizontal"

dt = 4
GRAPH = True
ZOOM = 0.015
SKIPS = 2000
zooms = [
    {"zoom": 2, "after": 500000, "skips": 2000, "dt": 1},
    {"zoom": 6, "after": 550000, "skips": 500, "dt": 1},
    {"zoom": 10, "after": 600000, "skips": 500, "dt": 1},
    {"zoom": 14, "after": 610000, "skips": 400, "dt": 1},
    {"zoom": 22, "after": 620000, "skips": 100, "dt": 1},
]

TIME_SKIP = 0
mass_of_rocket = 1

reached_orbit = False
reaches_orbit_in = 550000

perigee_force_until = 610242

last_perigee = 10e10  # initialized with a large value

propulsions_done = []

propulsions = [
    # {"type": ABSOLUTE, "magnitude": 10.0, "from":0, "duration": 7000, "color": "red"},
    {"type": VELOCITY_RELATED, "magnitude": -2, "from": 0, "duration": 2000, "color": "black"},
    # {"type": ABSOLUTE, "magnitude": -2.0, "from":800000, "duration": 1000, "color": "green"},
    # {"type": VELOCITY_RELATED, "magnitude": -1, "from": 400000, "duration": 3000, "color": "aqua"},
    {"type": HORIZONTAL, "magnitude": 0.4, "from": 501000, "duration": 800, "color": "red"},
    {"type": VELOCITY_RELATED, "magnitude": -1, "from": 540000, "duration": 1000, "color": "green"},
    # {"type": VELOCITY_RELATED, "magnitude": -0.3, "from": 9200, "duration": 600, "color": "black"},
    # {"type": VELOCITY_RELATED, "magnitude": -3.7, "from": 9100, "duration": 150, "color": "blue"},
    # {"type": VELOCITY_RELATED, "magnitude": -0.3, "from": 600000, "duration": 3000, "color": "gray"},
    # {"type": ABSOLUTE, "magnitude": -0.7, "from": 601000, "duration": 5000000000, "color": "pink"},
    {"type": HORIZONTAL, "magnitude": 2, "from": 400000, "duration": 50, "color": "skyblue"},

    {"type": HORIZONTAL, "magnitude": -1.5, "from": 620000, "duration": 2000, "color": "pink"},
    {"type": ABSOLUTE, "magnitude": -2.5, "from": 620500, "duration": 400000, "color": "red"},
    {"type": ABSOLUTE, "magnitude": -1.8, "from": 622000, "duration": 10000, "color": "blue"},
    {"type": VELOCITY_RELATED, "magnitude": -0.2, "from": 621500, "duration": 1000, "color": "blue"},
    {"type": HORIZONTAL, "magnitude": -0.3, "from": 622000, "duration": 444, "color": "blue"},
]


def draw_mars_on_graph():
    if not GRAPH: return;

    plt.axes()

    val = RADIUS_OF_MARS / ZOOM
    plt.axis([-val, val, -val, val])

    circle = plt.Circle((0, 0), radius=RADIUS_OF_MARS, fc='y', fill=False)
    plt.gca().add_patch(circle)

    plt.scatter(0, 0, color="red")
    # plt.axis('scaled')
    # plt.show()


time = 0

draw_mars_on_graph()

plt.ion()

notified = False

last_height = 1e100
zoomed = False

frame = 0

color = "black"

while True:
    f_gravity = - G * MASS_OF_MARS * mass_of_rocket * rocket_pos / (rocket_pos.mag ** 3)
    f_propulsion = vector()

    if len(zooms) > 0 and time > zooms[0]['after']:
        val = RADIUS_OF_MARS / (ZOOM * zooms[0]['zoom'])
        plt.axis([-val, val, -val, val])
        if 'skips' in zooms[0]:
            SKIPS = zooms[0]['skips']

        if 'dt' in zooms[0]:
            dt = zooms[0]['dt']

        zooms = zooms[1:]
        pass

    f_lander = vector()
    if not reached_orbit and time > reaches_orbit_in:
        reached_orbit = True
        reaches_orbit_in = time
        orbital_distance = rocket_pos.mag

        print("Reached orbit at {}".format(time))
        print(rocket_pos.diff_angle(vector(1, 0, 0)))

        # sleep(1)

    if reached_orbit and time < perigee_force_until:

        if rocket_pos.mag < last_perigee:
            last_perigee = rocket_pos.mag

        if 0 < rocket_pos.mag - last_perigee < 10e2:
            f_lander = rocket_vel / rocket_vel.mag
            f_lander *= -2.0



    for propulsion in propulsions:
        if propulsion['from'] < time < propulsion['from'] + propulsion['duration']:
            if propulsion not in propulsions_done:
                propulsions_done.append(propulsion)
                if "color" in propulsion:
                    color = propulsion["color"]
                print("Applying propulsion {}".format(propulsion))

            direction = vector(1, 0, 0)

            if 'type' in propulsion and propulsion['type'] == ABSOLUTE:
                # print("ABSOLUTE")
                direction = - rocket_pos / rocket_pos.mag
            elif propulsion['type'] == VELOCITY_RELATED:
                direction = rocket_vel / rocket_vel.mag
            elif propulsion['type'] == HORIZONTAL:
                ortho_vector = rocket_pos / rocket_pos.mag
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
        theta = acos(dot(rocket_vel, rocket_pos) / rocket_vel.mag / rocket_pos.mag) / pi
    except:
        pass

    if time > TIME_SKIP:
        print(
            "t= {0}, v={1:.0f}, h={2:.2f}, theta={3:.2f}, g={4:.2f}".format(time, rocket_vel.mag-241, rocket_pos.mag - RADIUS_OF_MARS,
                                                                 theta, f_gravity.mag))

    if rocket_pos.mag < RADIUS_OF_MARS:
        print("Rocket landed on ground with velocity: {0:.0f}".format(rocket_vel.mag))
        print("Total energy used: {}".format(get_total_energy()))
        with open("energy-used.tmp", "a") as f:
            f.write(str(get_total_energy()) + "\n")
        raw_input()
        exit(0)

    if rocket_pos.mag - RADIUS_OF_MARS > last_height:
        if time > TIME_SKIP and not reached_orbit:
            print("Warning, rocket going up", file=stderr)

    last_height = rocket_pos.mag - RADIUS_OF_MARS

    f_net = f_gravity + f_propulsion

    if reached_orbit:
        f_net += f_lander

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
