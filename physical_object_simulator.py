#!/usr/bin/env python2

from  __future__ import print_function, division
from headers import *
from constants import *
from constants_game import *
from utils import show_arrow, add_energy, get_total_energy
import matplotlib.pyplot as plt

from visual import color, rate

from physical_object import PhysicalObject, earth, sun, mars, moon, rocket, unit_mass, DELTA_TIME as dt

import numpy as np
import pylab


def show_graphics():
    # show_arrow()
    pass


def print_debug():

    print("time: {0:.2E}  ".format(PhysicalObject.get_total_time()), end='')
    print("distance to mars: {0:.2E}\t".format(mars.distance_with(rocket)), end='')
    print("distance to earth: {0:.2E}   ".format(earth.distance_with(rocket)), end='')
    print("energy used: {0:.2E}\t".format(get_total_energy()), end='')

    # print("Net force on earth: {0:.2E} ".format(earth.get_net_force().mag))
    # print("Accln: {0:.2E} ".format(earth.accln().mag))

    print()

if __name__ == "__main__":
    show_graphics()

    earth.register(color.green)
    sun.register(color.yellow)
    mars.register(color.red)
    # moon.register(color.white)
    rocket.register(color.cyan)

    frame = 0

    lastdiff = 1e1000
    while True:
        # print(PhysicalObject.get_total_time())

        render = frame > MAIN_SKIPS

        PhysicalObject.update_bodies(render)
        add_energy(rocket.get_net_propulsion(), rocket.vel, dt)

        frame += 1

        # print((rocket.pos - mars.pos).mag)
        # print(render)
        # print(FRAME_RATE)
        print_debug()
        # print(abs((DISTANCE_BETWEEN_SUN_AND_MARS-RADIUS_OF_MARS) - rocket.pos.mag), PhysicalObject.get_total_time())
        diff = abs(rocket.pos.mag - DISTANCE_BETWEEN_SUN_AND_MARS-RADIUS_OF_MARS)
        if diff > lastdiff and PhysicalObject.get_total_time() > 8000000:
            print("Difference in distance started to increase")
            print(rocket.pos, rocket.vel)
            print(mars.pos, mars.vel)
            print(mars.pos.diff_angle(rocket.pos))
            print("distance from mars: {}, total energy: {}, total time: {}".format(diff, get_total_energy(), PhysicalObject.get_total_time()))
            print("DISTANCE FROM MARS orbit: {}".format(diff))

            with open("energy-used.tmp", "a") as f:
                f.write(str(get_total_energy())+"\n")

            break
        else:
            lastdiff = diff


        if render:
            rate(FRAME_RATE)
            frame = 0

        # break

    print("Rocket reached mars")
