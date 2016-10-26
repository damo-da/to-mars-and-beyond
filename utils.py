from visual import arrow, color
from constants_game import SCALE, SHOW_VISUAL


def get_scaled_distance(distance):
    """Converts distance in metres to virtual units."""
    return distance * SCALE


def __(distance):
    distance = get_scaled_distance(distance)
    # print("Distance is {}".format(distance))
    return distance


def show_arrow():
    if not SHOW_VISUAL:
        return

    arrow(pos=(0, 60, -1), axis=(5, 0, 0), length=100, shaftwidth=2, color=color.magenta)


__energy = 0


def add_energy(force, v_vec, dt):
    global __energy
    __energy += force.mag * v_vec.mag * dt


def get_total_energy():
    global __energy
    return __energy
