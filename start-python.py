from autosolenoid import *

# - - - DESIGN INPUTS - - -
N_coil = # number of turns
L_coil = # mm, coil length
I_coil = # A, current
r_in_coil = # mm, winding radius
D_wire = # mm, wire diameter

r_plunger = # mm, plunger radius
L_plunger = # mm, plunger length
r_spring = # mm, spring housing radius
L_spring = # mm, spring housing length
mtl_plunger = "1020 Steel" # A FEMM material
L_stroke = # mm, max. stroke

r_minor_core = # mm, core inner radius
L_in_core = # mm, core inner length
t_r_core = # mm, shell outer thickness
t_a1_core = # mm, shell closed side thickness
t_a2_core = # mm, shell action side thickness
mtl_core = "1020 Steel" # A FEMM material

d_stroke = 1 # how many mm per analysis the plunger will move
view_padding = 30 # how many mm of padding from the edges of the solenoid the bitmap images will have
filename_main = "autocoil"
export_video = True # requires moviepy
# - - - - -

inputs = [N_coil, L_coil, I_coil, r_in_coil, D_wire, r_plunger, L_plunger, r_spring, L_spring,
          mtl_plunger, L_stroke, r_minor_core, L_in_core, t_r_core, t_a1_core, t_a2_core, mtl_core,
          d_stroke, view_padding, filename_main, export_video]
autoAnalyze(inputs)
