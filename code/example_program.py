import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import optparse
import os

def read_data(FILE):
    data = np.loadtxt(FILE)
    return data 

def plot_data(DATA,OUTPATH):
    fig,ax = plt.subplots(figsize=(4,3))
    ax.plot(DATA[:,0],DATA[:,1],color='black')
    ax.set_xlabel('time')
    ax.set_ylabel('intensity')
    plotname = "beautiful_example.png"
    pname = os.path.join(OUTPATH,plotname)
    plt.tight_layout()
    plt.savefig(pname) 

if __name__ == "__main__":
    desc = "test for Docker/Singularity tutorial"
    parser = optparse.OptionParser(description=desc)
    parser.add_option('--data',dest='d',type='str',help="where is your data?")
    parser.add_option('--outdir',dest='o',type='str',help="where do you want your pretty plot?") 
    (opts,args) = parser.parse_args()
    DATA = read_data(opts.d)
    plot_data(DATA,opts.o) 
    
