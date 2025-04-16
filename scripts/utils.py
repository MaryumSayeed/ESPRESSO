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

from scipy import interpolate
import os
from astropy.io import fits
import numpy as np

def download_spectra(sobject_id,ccd,sample,v):
    """
    Try to download the specfici spectrum from Datacentral
    """
    #print('Trying to download '+str(sobject_id)+str(ccd)+'.fits from')
    #print('https://cloud.datacentral.org.au/apps/files/?dir=/GALAH/DR3/data/galah/dr3/spectra/'+str(sobject_id)+str(ccd)+'.fits')
    #url       ='https://cloud.datacentral.org.au/apps/files/?dir=/GALAH/DR3/data/galah/dr3/spectra/'+str(sobject_id)+str(ccd)+'.fits'
    output_fname='../../lithium/galah/galah_data/%s/dr3/spectra/hermes/'%sample+str(sobject_id)+str(ccd)+'.fits'
    if os.path.exists(output_fname) is False:
        if v:
            print(output_fname,'data does not exist.')
        return None
    return output_fname

def interpolate_to_grid(xdata, ydata, xgrid):
    f = interpolate.interp1d(xdata, ydata,fill_value="extrapolate")
    new_ydata= f(xgrid)
    return xgrid, new_ydata

def get_spectra(sobject_id,sample,verbose=False):
    # If not already available, try to download
    fits_files = [[], [], [], []]

    for each_ccd in [1,2,3,4]:
        if fits_files[each_ccd-1] == []:
            fits_files[each_ccd-1] = download_spectra(sobject_id,each_ccd,sample,verbose)#fitspath+'%s%s.fits' % (sobject_id,each_ccd)
    fits_files=[i for i in fits_files if i is not None]
    # print(len(fits_files),'FITS files found for ID',sobject_id)
    # Extract wavelength grid for the normalised spectrum
    spectrum = dict()

    for each_ccd in range(len(fits_files)):
        each_ccd=each_ccd+1
        ff = fits.open(fits_files[each_ccd-1])
        fidx=4
        if len(ff)!=5:
            fidx=3
        start_wavelength = ff[fidx].header["CRVAL1"]
        dispersion       = ff[fidx].header["CDELT1"]
        nr_pixels        = ff[fidx].header["NAXIS1"]
        reference_pixel  = ff[fidx].header["CRPIX1"]
        if reference_pixel == 0:
            reference_pixel=1
        spectrum['wave_norm_'+str(each_ccd)] = ((np.arange(0,nr_pixels)--reference_pixel+1)*dispersion+start_wavelength)

        # Extract flux and flux error of normalized spectrum
        spectrum['sob_norm_'+str(each_ccd)] = np.array(ff[fidx].data)
        if each_ccd != 4:
            spectrum['uob_norm_'+str(each_ccd)] = np.array(ff[fidx].data * ff[1].data)
        else:
            # for normalised error of CCD4, only used appropriate parts of error spectrum
            spectrum['uob_norm_4'] = np.array(ff[fidx].data * (ff[1].data)[-len(spectrum['sob_norm_4']):])
        ff.close()
    spectrum['wave_norm'] = np.concatenate(([spectrum['wave_norm_'+str(each_ccd+1)] for each_ccd in range(len(fits_files))]))
    spectrum['sob_norm'] = np.concatenate(([spectrum['sob_norm_'+str(each_ccd+1)] for each_ccd in range(len(fits_files))]))
    spectrum['uob_norm'] = np.concatenate(([spectrum['uob_norm_'+str(each_ccd+1)] for each_ccd in range(len(fits_files))]))
    return spectrum