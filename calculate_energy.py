#!/usr/bin/env python

from __future__ import print_function, division

with open("energy-used.tmp") as f:
    file_contents = f.read()


values = [0 if not x else float(x.replace("\n", "")) for x in file_contents.split("\n")][0:3]

final_payload_mass = 1000
mass_loss_on_mars_space = 0.1
mass_loss_on_lower_orbit_ratio = 0.1
fuel_percentage = 0.95

initial_payload_mass = ((final_payload_mass / mass_loss_on_mars_space) / mass_loss_on_lower_orbit_ratio)
fuel_mass = initial_payload_mass * fuel_percentage

first_energy_total = initial_payload_mass * values[0]
second_energy_total = initial_payload_mass * mass_loss_on_lower_orbit_ratio * values[1]
third_energy_total = initial_payload_mass * mass_loss_on_lower_orbit_ratio * mass_loss_on_mars_space * values[2]

total_energy = first_energy_total + second_energy_total + third_energy_total

print("Total energy for a payload of {0} kg: {1:1.1e} Joules".format(final_payload_mass, total_energy))
print("Total fuel carried: {} kg".format(fuel_mass))

print("Energy provided per kg of fuel: {0:.2e} Joules".format(total_energy/fuel_mass))

