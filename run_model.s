#!/bin/bash

source ~/miniconda3/bin/activate pss-env

#set -x

sh_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

src_dir="$(realpath "${sh_dir}/src")"

data_dir="$(realpath "${sh_dir}/data")"

if (( $# != 5 )); then
    echo "Usage: run_model.s model_name p0 alpha D chi"
    exit 1
fi


model=$1
p0bygamma=$(python3 -c "print('{:.2f}'.format($2))")
alphabygamma=$(python3 -c "print('{:.2f}'.format($3))")
D=$(python3 -c "print('{:.2f}'.format($4))")   
chi=$(python3 -c "print('{:.2f}'.format($5))") 

run=3
pii=0.0
gamma0=5.0
K=5
rhoseed=2.0
T=20
n_steps=2e+5
dt_dump=0.01
lambda=2
r_p=1
rho_in=3.2
rhoisoend=4.5
rhonemend=6.0
mx=100
my=100
dx=1.0
dy=1.0

save_dir="${sh_dir}/data/$model/gamma0_${gamma0}_rhoseed_${rhoseed}_pi_${pii}/p0_${p0bygamma}_alpha_${alpha}_D_${D}_chi_${chi}/run_${run}"

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

python3 -m models.$model -s $save_dir
python3 -m src.analysis.create_avgs -s $save_dir
python3 -m src.analysis.create_videos -s $save_dir