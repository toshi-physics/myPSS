#!/bin/bash

source ~/miniconda3/bin/activate pss-env

#set -x

lp_start=1.0
lp_end=21.1
dlp=5.0

lq_start=1.0
lq_end=21.1
dlq=2.0

ld_start=1.0
ld_end=21.1
dld=5.0

lc_start=1.0
lc_end=21.1
dlc=5.0

lp=$(python3 -c "print('{:.2f}'.format($lp_start))")
while (( $(bc <<< "$lp <= $lp_end") ))
do
    lq=$(python3 -c "print('{:.2f}'.format($lq_start))")
    while (( $(bc <<< "$lq <= $lq_end") ))
    do
    	ld=$(python3 -c "print('{:.2f}'.format($ld_start))")
    	while (( $(bc <<< "$ld <= $ld_end") ))
    	do
            lc=$(python3 -c "print('{:.2f}'.format($lc_start))")
    	    while (( $(bc <<< "$lc <= $lc_end") ))
    	    do
        		echo "Creating files for lp = $lp lq = $lq ld = $ld lc = $lc"
        		./run_model.s model_Q_rho_dry $lp $lq $ld $lc
                lc=$(python3 -c "print('{:.2f}'.format($lc+$dlc))")
    	    done
    	    ld=$(python3 -c "print('{:.2f}'.format($ld+$dld))")
    	done
        lq=$(python3 -c "print('{:.2f}'.format($lq+$dlq))")
    done
    lp=$(python3 -c "print('{:.2f}'.format($lp+$dlp))")
done