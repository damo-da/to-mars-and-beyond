from __future__ import print_function, division
from math import isnan
from constants import *
from constants_game import *
from visual import vector, color, sphere
from utils import __

class PhysicalObject(object):
    """Physical Objects in the solar system."""
    __all__ = []
    __total_time = 0

    def __init__(self, mass, radius, pos):
        self.mass = float(mass)
        self.radius = float(radius)
        self.object = None
        self.last_trail_at = 0

        if len(pos) == 1:
            self.pos = vector(pos[0], 0, 0)
        elif len(pos) == 2:
            self.pos = vector(pos[0], pos[1], 0)
        else:
            self.pos = vector(pos[0], pos[1], pos[2])

        self.vel = vector(0, 0, 0)

    def print_debug(self):
        self.print_debug_movement(newline=False)
        print(",\t", end='')
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
        return self.get_net_force()/self.mass

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

        PhysicalObject.__total_time += DELTA_TIME

    @staticmethod
    def get_total_time():
        return PhysicalObject.__total_time

    def get_net_force(self):
        net = vector(0, 0, 0)

        for body in PhysicalObject.__all__:
            if body == self:
                continue
            else:
                this_direction = self.direction_with(body)
                this_force_magnitude = self.gravitational_force_magnitude_with(body)
                this_force = this_force_magnitude * this_direction

                # print("Magnitude is {}".format(this_force_magnitude))
                # print("Direction is {}".format(this_direction))
                # print("This force is {}".format(this_force))
                net += this_force

        if isnan(net.mag):
            net = 0

        return net

    def surface_gravity(self):
        return G * self.mass / (self.radius * self.radius)

    def gravitational_force_magnitude_with(self, body):
        return G * self.mass * body.mass / pow(self.distance_with(body), 2)

    def distance_with(self, body):
        return (body.pos - self.pos).mag

    def direction_with(self, body):
        m_vector = (body.pos - self.pos)
        return m_vector/m_vector.mag

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

        if abs(self.last_trail_at - PhysicalObject.get_total_time()) > TRAIL_AFTER_TIME:
            sphere(pos=self.object.pos, radius=RADIUS_TRAIL, color=self.object.color)
            print("Trail created")
            self.last_trail_at = PhysicalObject.get_total_time()

        self.object.pos = self.get_scaled_pos()


earth = PhysicalObject(MASS_OF_EARTH, RADIUS_OF_EARTH, (DISTANCE_BETWEEN_SUN_AND_EARTH, 0, 0))
earth.vel = vector(0, REVOLUTION_SPEED_OF_EARTH, 0)

sun = PhysicalObject(MASS_OF_SUN, RADIUS_OF_SUN, (0, 0, 0))

mars = PhysicalObject(MASS_OF_MARS, RADIUS_OF_MARS, (DISTANCE_BETWEEN_SUN_AND_MARS, 0, 0))
mars.vel = vector(0, REVOLUTION_SPEED_OF_MARS, 0)

moon = PhysicalObject(MASS_OF_MOON, RADIUS_OF_MOON, (DISTANCE_BETWEEN_EARTH_AND_MOON + DISTANCE_BETWEEN_SUN_AND_EARTH, 0, 0))
moon.vel = vector(0, REVOLUTION_SPEED_OF_MOON + REVOLUTION_SPEED_OF_EARTH, 0)
