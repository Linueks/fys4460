# 3d Lennard-Jones gas
units lj
dimension 3
# Periodic boundiaries
boundary p p p
atom_style atomic

variable seed equal 87287
variable sigma equal 3.405
variable b equal 5.72
variable reduced_density equal 4/((${b}/${sigma})^3)
variable temperature equal 1.5
variable num_box equal 20
variable radius_min equal 20/${b}
variable radius_max equal 30/${b}

# Set fcc lattice with specified density
lattice fcc ${reduced_density}
region simbox block 0 ${num_box} 0 ${num_box} 0 ${num_box}
create_box 2 simbox
create_atoms 1 box

variable box_len equal lx

mass * 1.0
velocity all create ${temperature} ${seed}

pair_style lj/cut 3.0
pair_coeff * * 1.0 1.0

fix 1 all nvt temp ${temperature} ${temperature} 0.5

thermo 100
run 1000

# Use a radius of 2 nm (equal to 20 Å)
variable radius equal 20/${b}
variable centre_x equal lx/2
variable centre_y equal ly/2
variable centre_z equal lz/2
region cylinder_reg cylinder x ${centre_y} ${centre_z} ${radius} EDGE EDGE units box

# Delete half of the atoms in the region
delete_atoms porosity cylinder_reg 0.5 ${seed}

group pore_group region cylinder_reg
set group pore_group type 2

# Create another group from all the remaining atoms except for the ones in the cylinder
group frozen subtract all pore_group
# Set the velocity of the atoms outside the cylinder to zero
velocity frozen set 0 0 0
# Avoid integrating all the particles
unfix 1

# Run pore_group using NVE
fix 1 pore_group nve

dump 1 all custom 10 data/cylinder_flow_profile.lammpstrj id type x y z vx vy vz

# Compute the porosity
variable porosity equal count(pore_group)/count(all)
print ${porosity} file data/flow_profile_porosity.dat

reset_timestep 0
compute pore_temp pore_group temp
compute msd pore_group msd
variable time equal dt*step

thermo_style custom step v_time c_pore_temp etotal press c_msd[4]

#Adding the force to generate the flow in the nanotube
fix force pore_group addforce 0.1 0.0 0.0

thermo 10
log data/cylinder_flow_profile.log

run 2000
