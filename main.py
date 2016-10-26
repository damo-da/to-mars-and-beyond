#!/usr/bin/env python2

from  __future__ import print_function, division
from headers import *
from constants import *
from constants_game import *
from utils import show_arrow
import matplotlib.pyplot as plt

from visual import color, rate

from physical_object import PhysicalObject, earth, sun, mars, moon, rocket, unit_mass

import numpy as np
import pylab

def show_graphics():
    show_arrow()

def print_debug():
    print("Earth: ", end='')
    earth.print_debug()

    print("Sun: ", end='')
    sun.print_debug()

    print("Total time: {0:.2E}".format(PhysicalObject.get_total_time()))
    print("Distance : {0:.2E}".format(earth.distance_with(sun)))

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
        frame += 1

        # print((rocket.pos - mars.pos).mag)
        # print(render)
        # print(FRAME_RATE)
        # print_debug()
        diff = (rocket.pos - mars.pos).mag
        if diff > lastdiff:
            print("DIff started to increase")
            print(rocket.pos, rocket.vel)
            print(mars.pos, mars.vel)
            print(diff)
            print(PhysicalObject.get_total_time())
            import sys;
            sys.exit()
        else:
            lastdiff = diff


        if render:
            rate(FRAME_RATE)
            frame = 0

        # break

