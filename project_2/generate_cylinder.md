################################################################################ 3d Lennard-Jones gas
units lj
dimension 3
################################################################################ Periodic boundiaries
boundary p p p
atom_style atomic

variable b equal 5.72
variable sigma equal 3.405
variable rho_prime equal 4/((${b}/${sigma})^3)
variable temperature equal 0.851

################################################################################ Set fcc lattice with specified density
lattice fcc ${rho_prime}
#lattice fcc 0.01
region simbox block 0 20 0 20 0 20
create_box 2 simbox
create_atoms 1 box

################################################################################ Use a radius of 2 nm (equal to 20 Å)
variable radius equal 20/${b}
variable center_y equal ly/2
variable center_z equal lz/2
region cylinder cylinder x ${center_y} ${center_z} ${radius} EDGE EDGE units box

mass * 1.0
velocity all create ${temperature} 87287

pair_style lj/cut 3.0
pair_coeff * * 1.0 1.0

fix 1 all nvt temp ${temperature} ${temperature} 0.5
#fix 1 all nve

thermo 100
# Thermalize for 3000 steps
run 3000

################################################################################ Group all atoms in the cylinder
group cylinder_group region cylinder
set group cylinder_group type 2

################################################################################ Create another group from all the remaining atoms except for the ones in the cylinder

group frozen subtract all cylinder_group

# Set the velocity of the atoms outside the cylinder to zero
velocity frozen set 0 0 0

# Avoid integrating all the particles
unfix 1

# Run cylinder using nve
fix 1 cylinder_group nve

#fix 1 all nvt temp ${temperature} ${temperature} 0.5

dump 1 all custom 10 data/argon_cylinder.lammpstrj id type x y z vx vy vz

log data/argon_cylinder.log

run 5000
