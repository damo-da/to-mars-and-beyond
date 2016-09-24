#!/usr/bin/env python2

from  __future__ import print_function, division
from headers import *
from constants import *
from constants_game import *
from utils import show_arrow
from visual import color, rate

from physical_object import PhysicalObject, earth, sun, mars

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

    while True:
        PhysicalObject.update_bodies()

        print_debug()

        rate(FRAME_RATE)

        # break
