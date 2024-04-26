#!/bin/bash

source ~/miniconda3/bin/activate pss-env

#set -x

sh_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

src_dir="$(realpath "${sh_dir}/src")"

data_dir="$(realpath "${sh_dir}/data")"

if (( $# != 6 )); then
    echo "Usage: run_model.s model_name lpressure lq ldiffusion lchi dr"
    exit 1
fi


model=$1
lp=$(python3 -c "print('{:.2f}'.format($2))")
lq=$(python3 -c "print('{:.2f}'.format($3))")
ld=$(python3 -c "print('{:.2f}'.format($4))")   
lc=$(python3 -c "print('{:.2f}'.format($5))")
dr=$(python3 -c "print('{:.2f}'.format($6))")

run=1
pii=0.1
gamma0=5.0
K=5
rhoseed=0.16
T=10
n_steps=1e+5
dt_dump=0.01
lambda=2
r_p=1
rho_in=3.2
rhoisoend=4.5
rhonemend=6.0
mx=50
my=50
dx=$dr
dy=$dr

alphabygamma=$(python3 -c "print('{:.2f}'.format(($lq)**2))")
p0bygamma=$(python3 -c "print('{:.2f}'.format(($lp)**2))")       # pressure when cells are close packed, should be very high
D=$(python3 -c "print('{:.2f}'.format(($ld)**2))")   # Density diffusion coefficient in density dynamics
chi=$(python3 -c "print('{:.2f}'.format(($lc)**2))")

save_dir="${sh_dir}/data/$model/gamma0_${gamma0}_rhoseed_${rhoseed}_pi_${pii}/lp_${lp}_lq_${lq}_ld_${ld}_lc_${lc}/dr_${dr}/run_$run/"

if [ ! -d $save_dir ]; then
    mkdir -p $save_dir
fi

params_file="${save_dir}/parameters.json"

echo \
"
{
    "\"run\"" : $run,
    "\"T\"" : $T,
    "\"n_steps\"" : $n_steps,
    "\"dt_dump\"" : $dt_dump,
    "\"K\"" : $K,
    "\"Gamma0\"" : $gamma0,
    "\"alphabygamma\"" : $alphabygamma,
    "\"Pi\"" : $pii,
    "\"chi\"": $chi,
    "\"lambda\"": $lambda,
    "\"D\"": $D,
    "\"p0bygamma\"": $p0bygamma,
    "\"r_p\"":$r_p,
    "\"rhoseed\"" : $rhoseed,
    "\"rho_in\"" : $rho_in,
    "\"rhoisoend\"" : $rhoisoend,
    "\"rhonemend\"" : $rhonemend,
    "\"mx\"" : $mx,
    "\"my\"" : $my,
    "\"dx\"" : $dx,
    "\"dy\"" : $dy
}
" > $params_file


model_dir=$(realpath "${sh_dir}/models")

python3 -m models.$model -s $save_dir
python3 -m src.analysis.create_avgs -s $save_dir
python3 -m src.analysis.create_videos -s $save_dir