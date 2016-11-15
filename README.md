# Simulation of Rocket Flight

This is a simple simulation of rocket flight from earth's surface to Mars. 

## Dependencies:
1. Python2
2. VPython
3. `matplotlib` 

## Problem
This project aims to simulate a rocket flight from Earth's surface to Mars.

## Solution
The solution has been divided into three parts: the flight to earth's lower orbit, inter-planetary flight and the landing.  
It takes into account the following things:

1. Gravity from sun, earth and mars
2. Rocket's thrust in 2 

However, to keep the project simple and limited to basic physics knowledge, a lot of assumptions have been made, notably the following:
### Everything in the universe is 2-dimensional.
To a certain degree, [this is a truth](https://www.youtube.com/watch?v=MTUsOWtxKKA). This assumption makes things so much simpler. The assumption that the Earth is a circle is made to reduce all sorts of compications including axial rotations, rotational speed variation at different latitudes, etc.

### No atmosphere in Earth or Mars
When there is atmosphere, there is drag. When drag is incorporated, there is a need of differential equations to be solved. So, to avoid all sorts of complications and also to keep the project simple for a basic physics class, the idea of atmosphere has been completely removed.

### Rocket's mass loss is concentrated at two fixed points.
Real rockets have various stages of flight when they drop off fuel containers when emptied. In ths project, the first "dropping" is done when escaping earth's lower orbit and after reaching Mars's orbit.
