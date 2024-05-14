import matplotlib.pyplot as plt

def PLOT_PARAMS(SIZE=10,LS=14,MS=6):
    TICKLABELSIZE=SIZE
    LABELSIZE=LS
    plt.rcParams["axes.linewidth"]  =  1
    plt.rcParams["axes.axisbelow"]  =  True
    plt.rcParams["axes.titlesize"]  =  LABELSIZE         # fontsize of the axes title
    plt.rcParams["axes.labelsize"]  =  LABELSIZE         # fontsize of the x and y labels
    plt.rcParams["xtick.labelsize"] =  TICKLABELSIZE    # fontsize of the tick labels
    plt.rcParams["ytick.labelsize"] =  TICKLABELSIZE    # fontsize of the tick labels
    plt.rcParams["legend.fontsize"] =  LABELSIZE
    plt.rcParams["xtick.direction"] =  'inout'
    plt.rcParams["ytick.direction"] =  'inout'
    plt.rcParams["xtick.top"]       =  True
    plt.rcParams["ytick.right"]     =  True

    #plt.rcParams["lines.markerfacecolor"] =  'red'               # default=6
    #plt.rcParams["lines.markeredgecolor"] =  'black'               # default=6
    plt.rcParams["xtick.minor.visible"] =  True
    plt.rcParams["ytick.minor.visible"] =  True
    
    plt.rcParams["xtick.major.width"]   =  2.0
    plt.rcParams["xtick.minor.width"]   =  1.2
    
    plt.rcParams["ytick.major.width"]   =  2.0
    plt.rcParams["ytick.minor.width"]   =  1.2

    plt.rcParams["xtick.major.size"]   =  5.5
    plt.rcParams["xtick.minor.size"]   =  4.0
    
    plt.rcParams["ytick.major.size"]   =  5.5
    plt.rcParams["ytick.minor.size"]   =  4.0

    plt.rcParams['figure.facecolor']    = 'white'
    plt.rcParams["lines.markersize"]    =  MS
    
PLOT_PARAMS()