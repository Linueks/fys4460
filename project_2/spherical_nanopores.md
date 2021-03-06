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
variable temperature equal 0.851
variable num_box equal 20
variable radius_min equal 20/${b}
variable radius_max equal 30/${b}

# Set fcc lattice with specified density
lattice fcc ${reduced_density}
region simbox block 0 ${num_box} 0 ${num_box} 0 ${num_box}
create_box 2 simbox
create_atoms 1 box

variable box_len equal lx

variable a loop 20
label pore_loop

variable x_1 equal random(0,${box_len},${seed})
variable y_1 equal random(0,${box_len},${seed})
variable z_1 equal random(0,${box_len},${seed})
variable radius_1 equal random(${radius_min},${radius_max},${seed})
region $a sphere ${x_1} ${y_1} ${z_1} ${radius_1} units box

next a
jump random_argon.md pore_loop

mass * 1.0
velocity all create ${temperature} ${seed}

pair_style lj/cut 3.0
pair_coeff * * 1.0 1.0

fix 1 all nvt temp ${temperature} ${temperature} 0.5
#fix 1 all nve

thermo 100
# Thermalize for 3000 steps
run 300

group pore_group region 1

# Group all atoms in the cylinder
variable a loop 2 20
label group_loop

group pore_$a region $a
group pore_group union pore_group pore_$a

next a
jump random_argon.md group_loop

set group pore_group type 2
# Create another group from all the remaining atoms except for the ones in the cylinder
group frozen subtract all pore_group
# Set the velocity of the atoms outside the cylinder to zero
velocity frozen set 0 0 0
# Avoid integrating all the particles
unfix 1

# Run cylinder using nve
fix 1 pore_group nve

dump 1 all custom 10 data/spherical_nanopores_argon.lammpstrj id type x y z vx vy vz

# Compute the porosity
variable porosity equal count(pore_group)/count(all)
print ${porosity} file data/porosity.dat

run 1000
