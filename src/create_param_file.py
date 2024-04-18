import numpy as np
import json, argparse, os

initParser = argparse.ArgumentParser(description='create param file')
initParser.add_argument('-m', '--model', help='name of the model, should have model_xyz.py file in directory')
initParser.add_argument('-j','--jsonfile', help='parameter file of type json', default='parameters.json')
initParser.add_argument('-lp', '--lpressure')
initParser.add_argument('-lq', '--lq')
initParser.add_argument('-ld', '--ldiffusion')
initParser.add_argument('-lc', '--lchi')
initParser.add_argument('-g', '--gamma')
initargs = initParser.parse_args()  
if os.path.isfile("%s" %(initargs.jsonfile)):
    with open(initargs.jsonfile) as jsonFile:
            parameters = json.load(jsonFile)

K         = float(initargs.lk) **2 # elastic constant, sets diffusion lengthscale of S with Gamma0
gamma     = float(initargs.gamma)   # traction coefficient
alpha     = (float(initargs.lq)**2) * gamma    # active contractile stress
p0        = (float(initargs.lpressure)**2) * gamma       # pressure when cells are close packed, should be very high
D         = float(initargs.ldiffusion)**2    # Density diffusion coefficient in density dynamics
chi       = float(initargs.lchi)**2      # coefficient of density gradients in Q's free energy

run       = parameters["run"]
T         = parameters["T"]        # final time
dt_dump   = parameters["dt_dump"]
n_steps   = int(parameters["n_steps"])  # number of time steps
Gamma0    = parameters["Gamma0"]   # rate of Q alignment with mol field H
#lambd     = parameters["lambda"]   # flow alignment parameter
#r_p       = parameters["r_p"]      # rate of pressure growth equal to rate of growth of cells
Pii       = parameters["Pi"]       # strength of alignment
rho_in    = parameters["rho_in"]   # isotropic to nematic transition density, or "onset of order in the paper"
rho_seed  = parameters["rhoseed"] /rho_in     # seeding density, normalised by 100 mm^-2
rho_iso   = parameters["rhoisoend"] /rho_in   # jamming density
rho_nem   = parameters["rhonemend"] /rho_in   # jamming density max for nematic substrate
mx        = np.int32(parameters["mx"])
my        = np.int32(parameters["my"])


savedir     = initargs.model+"/gamma0_{:.2f}_rhoseed_{:.2f}_pi_{:.3f}/lp_{:.1f}_lq_{:.1f}_ld_{:.1f}_lc_{:.1f}_gamma_{:.1f}/run_{:d}/".format(Gamma0, rho_seed, Pii, initargs.lpressure, initargs.lq, initargs.ldiffusion, initargs.lchi , gamma, run)
if not os.path.exists(savedir):
    os.makedirs(savedir)


parameters["K"] = K 
parameters["gammaf"] = gamma     
parameters["alpha"] = alpha  
parameters["p0"] = p0
parameters["D"] = D        
parameters["chi"] = chi 


with open(savedir+'parameters.json', 'w') as f:
    json.dump(parameters, f)