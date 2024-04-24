#!/bin/bash

source ~/miniconda3/bin/activate pss-env

#set -x

dx_start=0.05
dx_end=1.01
ddx=0.05

lp=0.0
lq=0.1
ld=2.0
lc=5.0

dx=$(python3 -c "print('{:.2f}'.format($dx_start))")
while (( $(bc <<< "$dx <= $dx_end") ))
    do
        echo "Creating files for dr = $dx"
        ./run_model_gamma.s model_Q_rho_dry_tests $lp $lq $ld $lc $dx
        dx=$(python3 -c "print('{:.2f}'.format($dx+$ddx))")
    done