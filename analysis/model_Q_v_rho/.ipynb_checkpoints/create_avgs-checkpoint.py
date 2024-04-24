import numpy as np
import json, argparse, os

initParser = argparse.ArgumentParser(description='model_Q_v_rho_create_avgs')
    initParser.add_argument('-s','--save_dir', help='directory to save data')
    initargs = initParser.parse_args()
    savedir = initargs.save_dir
    if os.path.isfile(savedir+"/parameters.json"):
	    with open(savedir+"/parameters.json") as jsonFile:
              parameters = json.load(jsonFile

    T         = parameters["T"]        # final time
    dt_dump   = parameters["dt_dump"]
    n_steps   = int(parameters["n_steps"])  # number of time steps

    dt        = T / n_steps     # time step size
    n_dump    = round(T / dt_dump)

    meanrho = np.zeros(n_dump)
    meanS   = np.zeros(n_dump)
    meantheta = np.zeros(n_dump)
    stdtheta = np.zeros(n_dump)

    i=0
for n in np.arange(n_dump):
    meanrho[i] += np.average(np.loadtxt(datadir+'rho.csv.{:d}'.format(n), delimiter=','))
    Qxx = np.loadtxt(datadir+'Qxx.csv.{:d}'.format(n), delimiter=',')
    Qxy = np.loadtxt(datadir+'Qxy.csv.{:d}'.format(n), delimiter=',')
    theta = np.atan2(Qxy, Qxx)
    meantheta[i] += np.average(theta)
    stdtheta[i] += np.std(theta)
    i+=1

np.savetxt(savedir+'meanrho.csv', meanrho, delimiter=',')
np.savetxt(savedir+'meanS.csv', meanrho, delimiter=',')
np.savetxt(savedir+'meantheta.csv', meanrho, delimiter=',')
np.savetxt(savedir+'stdtheta.csv', meanrho, delimiter=',')