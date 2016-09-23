#!/usr/bin/env python2
from headers import *
from constants import *
from constants_game import *
from utils import show_arrow
from visual import color

from physical_object import PhysicalObject, earth, sun, mars


def show_graphics():
    show_arrow()

if __name__ == "__main__":
    show_graphics()

    earth.register(color.green)
    sun.register(color.yellow)

    while True:
        PhysicalObject.update_bodies()

        print(earth.vel)

        # rate(FRAME_RATE)
