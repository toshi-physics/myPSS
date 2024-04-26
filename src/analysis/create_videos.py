import numpy as np
import json, argparse, os
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox


def main():

    initParser = argparse.ArgumentParser(description='model_Q_v_rho_create_videos')
    initParser.add_argument('-s','--save_dir', help='directory to save data')
    initargs = initParser.parse_args()
    savedir = initargs.save_dir
    if os.path.isfile(savedir+"/parameters.json"):
        with open(savedir+"/parameters.json") as jsonFile:
              parameters = json.load(jsonFile)
    
    T         = parameters["T"]        # final time
    dt_dump   = parameters["dt_dump"]
    n_steps   = int(parameters["n_steps"])  # number of time steps
    dt        = T / n_steps     # time step size
    n_dump    = round(T / dt_dump)
    K         = parameters["K"]        # elastic constant, square of nematic correlation length
    
    mx        = np.int32(parameters["mx"])
    my        = np.int32(parameters["my"])
    dx        = np.float32(parameters["dx"])
    dy        = np.float32(parameters["dy"])
    Lx        = mx*dx/np.sqrt(K)
    Ly        = my*dy/np.sqrt(K)
    
    #setup a meshgrid
    tol = 0.001
    
    x   = np.linspace(0+tol, Lx-tol, mx)
    y   = np.linspace(0+tol, Ly-tol, my)
    xv, yv  = np.meshgrid(x,y)
    
    times = np.arange(0, n_dump, 1)*dt_dump

    
    figrho, axrho= plt.subplots(figsize=(12, 8), ncols=1)
    figQ, axQ= plt.subplots(figsize=(12, 8), ncols=1)
    figvort, axvort= plt.subplots(figsize=(12, 8), ncols=1)

    n=0
    p_factor = 2
    
    rho = np.loadtxt(savedir+'/data/'+'rho.csv.{:d}'.format(n), delimiter=',')
    Qxx = np.loadtxt(savedir+'/data/'+'Qxx.csv.{:d}'.format(n), delimiter=',')
    Qxy = np.loadtxt(savedir+'/data/'+'Qxy.csv.{:d}'.format(n), delimiter=',')
    curldivQ = np.loadtxt(savedir+'/data/'+'curldivQ.csv.{:d}'.format(n), delimiter=',')
    vx = np.loadtxt(savedir+'/data/'+'vx.csv.{:d}'.format(n), delimiter=',')
    vy = np.loadtxt(savedir+'/data/'+'vy.csv.{:d}'.format(n), delimiter=',')
    S = np.sqrt(2*(Qxx**2+Qxy**2))
    Sp = pixelate(S, p_factor)
    theta = pixelate(np.arctan2(Qxy, Qxx)/2, p_factor)
    nx    = np.cos(theta)
    ny    = np.sin(theta)
    
    crho = [axrho.pcolormesh(xv, yv, S, cmap='viridis', vmin=0, vmax=1.8), axrho.quiver(xv,yv,vx,vy, color='w', pivot='middle')]
    cQ   = [axQ.pcolormesh(xv, yv, S, cmap='viridis', vmin=0, vmax=1.8), axQ.quiver(xv[p_factor:-1:p_factor, p_factor:-1:p_factor], yv[p_factor:-1:p_factor, p_factor:-1:p_factor],Sp*nx,Sp*ny, color='w', pivot='middle', headlength=0, headaxislength=0)]
    cvort= axvort.pcolormesh(xv, yv, curldivQ, vmin=-0.1, vmax=0.1)

    figrho.colorbar(crho[0])
    axrho.set_title(r"$\rho$")
    figQ.colorbar(cQ[0])
    axQ.set_title('S')
    figvort.colorbar(cvort)
    axvort.set_title('Vorticity')
    
    tbaxrho = figrho.add_axes([0.05, 0.93, 0.04, 0.04])
    tbrho = TextBox(tbaxrho, 'time')
    tbaxQ = figQ.add_axes([0.05, 0.93, 0.04, 0.04])
    tbQ = TextBox(tbaxQ, 'time')    
    tbaxvort = figvort.add_axes([0.05, 0.93, 0.04, 0.04])
    tbvort = TextBox(tbaxvort, 'time')
    
    def plt_snapshot_rho(val):
        val = (abs(times-val)).argmin()
        
        rho = np.loadtxt(savedir+'/data/'+'rho.csv.{:d}'.format(val), delimiter=',')
        vx = np.loadtxt(savedir+'/data/'+'vx.csv.{:d}'.format(val), delimiter=',')
        vy = np.loadtxt(savedir+'/data/'+'vy.csv.{:d}'.format(val), delimiter=',')
        
        crho[0].set_array(rho)
        crho[1].set_UVC(vx, vy)
        
        figrho.canvas.draw_idle()

    def plt_snapshot_Q(val):
        val = (abs(times-val)).argmin()
        
        Qxx = np.loadtxt(savedir+'/data/'+'Qxx.csv.{:d}'.format(val), delimiter=',')
        Qxy = np.loadtxt(savedir+'/data/'+'Qxy.csv.{:d}'.format(val), delimiter=',')
        S = np.sqrt(2*(Qxx**2+Qxy**2))
        Sp = pixelate(S, p_factor)
        theta = pixelate(np.arctan2(Qxy, Qxx)/2, p_factor)
        nx    = np.cos(theta)
        ny    = np.sin(theta)
        
        cQ[0].set_array(S)
        cQ[1].set_UVC(Sp*nx, S*ny)
        
        figQ.canvas.draw_idle()
    
    def plt_snapshot_vort(val):
        val = (abs(times-val)).argmin()
        
        curldivQ = np.loadtxt(savedir+'/data/'+'curldivQ.csv.{:d}'.format(val), delimiter=',')
        
        cvort.set_array(curldivQ)
        
        figvort.canvas.draw_idle()

    
    from matplotlib.animation import FuncAnimation
    animrho = FuncAnimation(figrho, plt_snapshot_rho, frames = n_dump, interval=1, repeat=True)
    animrho.save(savedir+'/videos/'+'0_rho.mp4')

    animQ = FuncAnimation(figQ, plt_snapshot_Q, frames = n_dump, interval=1, repeat=True)
    animQ.save(savedir+'/videos/'+'0_Q.mp4')

    animvort = FuncAnimation(figvort, plt_snapshot_vort, frames = n_dump, interval=1, repeat=True)
    animvort.save(savedir+'/videos/'+'0_vorticity.mp4')

def pixelate(x, gridpoints):
    nx, ny = np.shape(x)
    xpad = np.pad(x, (gridpoints, gridpoints), 'wrap')
    ret = np.zeros(np.shape(x))
    for cx in np.arange(nx):
        for cy in np.arange(ny):
            ret[cx, cy] += np.average(xpad[cx:cx+1+2*gridpoints, cy:cy+1+2*gridpoints])
    ret = ret[gridpoints:-1:gridpoints, gridpoints:-1:gridpoints]
    return ret

if __name__=="__main__":
    main()
