from __future__ import print_function, division

from constants import *
from constants_game import *
from visual import vector, color, sphere
from utils import __

class PhysicalObject(object):
    """Physical Objects in the solar system."""
    __all__ = []

    def __init__(self, mass, radius, pos):
        self.mass = float(mass)
        self.radius = float(radius)
        self.object = None

        if len(pos) == 1:
            self.pos = vector(pos[0], 0, 0)
        elif len(pos) == 2:
            self.pos = vector(pos[0], pos[1], 0)
        else:
            self.pos = vector(pos[0], pos[1], pos[2])

        self.vel = vector(0, 0, 0)

    def print_debug(self):
        self.print_debug_movement(newline=False)

        self.print_debug_consts()

    def print_debug_movement(self, newline=True):
        text = "accln: {}, vel: {}, pos: {}".format(self.accln(), self.vel, self.pos)

        if newline:
            print(text)
        else:
            print(text, end='')

    def print_debug_consts(self, newline=True):
        text = "mass: {}, radius: {}, pos: {}".format(self.mass, self.radius, self.pos)

        if newline:
            print(text)
        else:
            print(text, end='')

    @staticmethod
    def count_objects():
        # print(len(PhysicalObject.__all__))
        return len(PhysicalObject.__all__)

    def accln(self):
        return self.get_net_force()/self.mass;

    @staticmethod
    def update_bodies():
        updates = []
        for item in PhysicalObject.__all__:
            net_force = item.get_net_force()
            accln = net_force / item.mass
            new_vel = item.vel + accln * DELTA_TIME
            new_pos = item.pos + item.vel * DELTA_TIME
            updates.append({"item": item, "vel": new_vel, "pos": new_pos})

        # print(updates[0]['item'].pos - updates[0]['pos'])

        for item in updates:
            item["item"].vel = item['vel']
            item["item"].pos = item['pos']
            item["item"].render_updates()

    def get_net_force(self):
        net = vector(0, 0, 0)

        for body in PhysicalObject.__all__:
            if body == self:
                continue
            else:
                this_direction = self.direction_with(body)
                this_force_magnitude = self.gravitational_force_magnitude_with(body)
                this_force = this_force_magnitude * this_direction

                net += this_force

        return net

    def surface_gravity(self):
        return G * self.mass / (self.radius * self.radius)

    def gravitational_force_magnitude_with(self, body):
        return G * self.mass * body.mass / pow(self.distance_with(body), 2)

    def distance_with(self, body):
        return (body.pos - self.pos).mag

    def direction_with(self, body):
        return body.pos - self.pos

    def get_scaled_pos(self):
        return __(self.pos[0]), __(self.pos[1]), __(self.pos[2])

    def register(self, color=color.orange):
        PhysicalObject.__all__.append(self)


        #initialize graphical stuffs
        if not SHOW_VISUAL: return

        scaled_pos = self.get_scaled_pos()

        # print("Scaled pos is {}".format(scaled_pos))
        self.object = sphere(pos=scaled_pos, radius=RADIUS_1, color=color)

    def render_updates(self):
        if self.object is None:
            return

        self.object.pos = self.get_scaled_pos()


earth = PhysicalObject(MASS_OF_EARTH, RADIUS_OF_EARTH, (DISTANCE_BETWEEN_SUN_AND_EARTH, 0, 0))
earth.vel = vector(0, 30556, 0)

sun = PhysicalObject(MASS_OF_SUN, RADIUS_OF_SUN, (0, 0, 0))
mars = PhysicalObject(MASS_OF_MARS, RADIUS_OF_MARS, (DISTANCE_BETWEEN_SUN_AND_MARS, 0, 0))
