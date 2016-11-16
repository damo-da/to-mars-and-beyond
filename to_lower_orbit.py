from __future__ import print_function, division

from headers import *
from math import pi, sin, cos, tan, sqrt, atan as arctan
from constants import RADIUS_OF_EARTH, MASS_OF_EARTH, G, GROUND_SPEED_AT_EARTH
from visual import vector, dot as dot_product
from matplotlib import pyplot as plt
import sys
from utils import add_energy, get_total_energy


FRAME_SKIPS = 800
dt = 0.1
mass = 1
GRAPH = True
ZOOM = 0.5

time_to_exit = 20000

# perigee: the lowest altitude
# apogee: the hightest altitude

colors = ["red","blue","aqua","green", "brown", "pink"]


def print_err(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def draw_earth_on_graph():
    if not GRAPH: return;

    plt.axes()

    val = RADIUS_OF_EARTH / ZOOM
    plt.axis([-val, val, -val, val])

    circle = plt.Circle((0, 0), radius=RADIUS_OF_EARTH, fc='y', fill=False)
    plt.gca().add_patch(circle)

    plt.scatter(0, 0, color="black")
    # plt.axis('scaled')
    # plt.show()


def check_conditions():
    global r_vec, v_vec

    COSINE_LIMIT_CHECK = 0.002
    ORBITAL_SPEED_LIMIT_CHECK = 20

    # print(r_vec)
    # print(v_vec)

    cosine_check_passed = False
    cosine_value = dot_product(r_vec, v_vec) / (r_vec.mag * v_vec.mag)

    # print(cosine_value)
    if abs(cosine_value) < COSINE_LIMIT_CHECK:
        # print("Direction match")
        cosine_check_passed = True

    orbital_speed_check_passed = False

    orbital_speed_required = sqrt(G * MASS_OF_EARTH / r_vec.mag)
    orbital_speed_diff = v_vec.mag - orbital_speed_required
    if abs(orbital_speed_diff) < ORBITAL_SPEED_LIMIT_CHECK:
        # print("Orbital speed pass with distance {}".format(orbital_speed_diff))
        orbital_speed_check_passed = True

    cost = cosine_check_passed / 1.0 + abs(orbital_speed_check_passed)/7000.

    return (cosine_check_passed and orbital_speed_check_passed), cost, \
           cosine_check_passed, orbital_speed_check_passed, \
           cosine_value, orbital_speed_diff


def apply_force(f_net):
    global v_vec, r_vec, time
    accln = f_net / mass
    v_vec += accln * dt
    r_vec += v_vec * dt

    time += dt


rocket_thrusts = vector(18, 18)
propeller_until = 182

apogee_thrusts = vector(7, 0.0) # direction with respect to the velocity of the rocket
apogee_active = False
apogee_after = 340
apogee_upto = 700
apogee_message_shown = False

capuche_thrusts = vector(3.35, 0.0)
capuche_active = False
capuche_after = 3900
capuche_upto = 4700
capuche_message_shown = False

time_render_threshold = 1

propeller_on = True
current_frame = 0
r_vec = vector(0, RADIUS_OF_EARTH)
v_vec = vector(GROUND_SPEED_AT_EARTH, 0)
time = 0

draw_earth_on_graph()


def simulate(exit_time=400, exit_after_success=True, return_state=False):
    global propeller_on, current_frame, r_vec, v_vec, time, apogee_active, apogee_thrusts, apogee_message_shown
    global capuche_active, capuche_thrusts, capuche_message_shown

    propeller_on = True
    current_frame = 0
    r_vec = vector(0, RADIUS_OF_EARTH)
    v_vec = vector(GROUND_SPEED_AT_EARTH, 0)
    time = 0

    cost_sum = 0
    iters = 0

    max_height = r_vec.mag

    while True:
        f_gravity = r_vec * (- G * MASS_OF_EARTH * mass / r_vec.mag ** 3)

        f_propulsion = vector()
        if propeller_on:
            # direction_diff = 0
            f_propulsion += rocket_thrusts

        if apogee_active:
            base_dir = v_vec/v_vec.mag
            apogee_thrust_dir = apogee_thrusts / apogee_thrusts.mag
            apogee_force = apogee_thrusts.mag * (base_dir + apogee_thrust_dir)

            # print("Apogee force: {}".format(apogee_force))
            #
            f_propulsion += apogee_force

        if capuche_active:
            base_dir = v_vec / v_vec.mag

            capuche_thrust_dir = capuche_thrusts / capuche_thrusts.mag
            capuche_force = capuche_thrusts.mag * (base_dir + capuche_thrust_dir)

            f_propulsion += base_dir * capuche_force.mag

        if propeller_on and time > propeller_until:
            print("Turning propellers off at t = {:.1F}, h= {:.1F}".format(time, r_vec.mag - RADIUS_OF_EARTH))
            propeller_on = False
            continue
        current_frame += 1

        f_net = f_propulsion + f_gravity

        add_energy(f_propulsion, v_vec, dt)

        apply_force(f_net)

        if r_vec.mag > max_height:
            max_height = r_vec.mag
        elif r_vec.mag < max_height:
            # print_err("WARNING: ROCKET losing altitude. currently lost altitude of {}m from max_height".format(abs(r_vec.mag-max_height)))
            pass

        # print(r_vec.mag - max_height)

        condition_results = check_conditions()
        condition = condition_results[0]

        cost = condition_results[1]
        cost_sum += cost
        iters += 1.

        # print("CHECK: {0}, max_height={1:.1E}, time = {3}, {2}, apogee: {4}".format(f_net, max_height - RADIUS_OF_EARTH, condition_results, time, apogee_active))


        if condition == True and exit_after_success:
            print("Successful")
            if return_state:
                return [True, cost_sum/iters]
            return True
        elif condition == True and apogee_active and not apogee_message_shown:
            apogee_active = False
            apogee_message_shown = True
            print("APOGEE REACHED")
            print(condition_results)
            print("")
            # plt.pause(1)
        else:
            if not apogee_active and (apogee_after < time < apogee_upto):
                apogee_active = True
            elif apogee_active and time > apogee_upto:
                apogee_active = False

        if time > exit_time:
            print("Can not achieve stable orbit till exit time.")
            if return_state:
                return [False, cost_sum/iters]
            return False

        if GRAPH and (current_frame > FRAME_SKIPS) and time > time_render_threshold:
            # graphing
            plt.scatter(r_vec[0], r_vec[1], color=colors[ int(time/4000.)%len(colors)])
            plt.pause(0.01)
            # plt.scatter(time, r_vec.mag)
            current_frame = 0

        if not capuche_active and not capuche_message_shown and (capuche_after < time < capuche_upto) :
            capuche_active = True
            capuche_message_shown = True
            print("Activating capuche")
            plt.pause(0.4)
        elif capuche_active and time > capuche_upto:
            print("Deactivating capuche")
            capuche_active = False

        if time > 8000 and (apogee_active or propeller_on):
            print("Apogee or propeller active after a long time :\\")
            plt.pause(10)
            print(apogee_active)
            print(propeller_on)

        if time > time_to_exit:
            print("It's time to leave")
            with open("energy-used.tmp", "w") as f:
                f.write(str(get_total_energy())+"\n")
            print("time={}, speed={}, r.mag={}".format(time, v_vec.mag, r_vec.mag))

            raw_input("Press any key to exit")
            break

        # print(v_vec.mag, r_vec.mag)
        # print("a: {},   v: {},   r: {},   t:{},   rocket_thrust: {}".format(accln, v_vec, r_vec, time, "on" if propeller_on else "off"))

        # print ("loop complete")

        print("ENERGY per kg: {}".format(get_total_energy()))

        if r_vec.mag < RADIUS_OF_EARTH:
            print_err("Warning: rocket inside earth's surface")
            if return_state:
                return [False, cost_sum/iters]

            return False


def simulate_everything():
    global propeller_until, rocket_thrusts

    loop_counter = 0

    successful_results = []

    for i in range(73, 85):
        for j in range(10, 30):
            for t in range(50, 120):
                loop_counter += 1
                # print("loop_counter: {}, i={}, j={}, t={}".format(loop_counter, i, j, t))

                rocket_thrusts = vector(i, j)
                propeller_until = t

                # print("Simulating for thrust=({}, {}), t = {}".format(i, j, t))
                result = simulate()

                if result == True:
                    print("Result achieved at: ")
                    print("Simulating for thrust=({}, {}), t = {}".format(i, j, t))
                    successful_results.append((i, j, t))

                    # import sys
                    # sys.exit()

    print(successful_results)


if __name__ == "__main__":
    if GRAPH:
        print(simulate(100000, exit_after_success=False))
    else:
        for i in range(200, 250):
            rocket_thrusts = vector(i, 80)
            time = 200
            result = simulate(exit_time=4000, return_state=True)

            print_err(result[1])

            plt.scatter(i, result[1] * 10**5)
            plt.pause(0.01)

        print(check_conditions())
        # use_simulation_input()
