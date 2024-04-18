#!/bin/zsh

# create pss-env on workstation, find where miniconda is
source ~/miniconda3/bin/activate pss-env

set -x

sh_dir -> current run directory

run_exe -> directory where src code resides

# for lp lq ld lc gamma, run the next two snippets of code

python3 create_param_file.py -m model_Q_rho_dry -j parameters.json -lp -lq -ld -lc -g

# change directory to wherever param_file was created

#change model_Q_rho_dry to just run in whatever directory it is in

python3 model_Q_rho_dry.py -j parameters.json