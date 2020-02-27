#------------------------------------------------------------------------------
# MAKE_FIG02.PY
#  
# PURPOSE
# Plot a heatmap of GLOBE Observer data on a world map
# This is Figure 2 from Amos & Starke et al. 2019 (in prep)
#
# RESOURCES
# - GLOBE Observer website: observer.globe.gov
# - GLOBE Data User Guide: https://www.globe.gov/globe-data/globe-data-user-guide
# - Download the GLOBE Observer app: https://observer.globe.gov/about/get-the-app
#
# MODIFICATION HISTORY
# 01 Oct 2019 - HM Amos - v1.0 created based on example_geographic_heatmap.py
#                         and figure_0S10.py by MJ Starke
# 02 Dec 2019 - HM Amos - move global variables used by other plotting modules
#                         to data_common.py
# 24 Jan 2020 - HM Amos - set colorbar limits at 10,000
#
# CITATION
# Amos, H.M. and M.J. Starke et al., 2020, GLOBE Observer
# Data:2016-2019, in prep. *Check back for updated journal
# information and publication DOI*
#
# CORRESPONDING AUTHOR
# Helen Amos, helen.m.amos@nasa.gov
#
# DISCLAIMER
# This code comes as is without guarantees of any kind. 
#------------------------------------------------------------------------------

# Imports
from figure_common import *
from data_common import *
from globeqa import plotters
import matplotlib.pyplot as plt

def mainfig02():   
    
    #--------------------------------------------------------------------------
    # Figure A: Heatmap world map of GLOBE Observer data
    #--------------------------------------------------------------------------

    # Create lists of x and y points for the observations of interest.
    x = [ob.lon for ob in obs]
    y = [ob.lat for ob in obs]

    # Create a 2D histogram.
    histo, xedges, yedges = np.histogram2d(x, y, (np.arange(-180.0, 180.1, 1.0), np.arange(-90.0, 90.1, 1.0)))

    # In order to use pcolormesh, we need to transpose the array.
    histo = histo.T

    # Take logarithm of the array.  In this context, values naturally span multiple orders of magnitude.
    histo = np.log10(histo)
    
    # Do this so the colorbar saturates at 1e4
    # - histo is log10 transformed
    histosat = histo
    histosat[histo > 4] = 4


    # Create a figure and axis with cartopy projection.
    ax = plotters.make_pc_fig()

    # Convert the 1D lists of bin edges to 2D lists.
    xx, yy = np.meshgrid(xedges, yedges)

    # Plot as colormesh.
    pcm = ax.pcolormesh(xx, yy, histosat, cmap="Reds")

    # Decide what values should be labeled on the colorbar.
    ticks = [1, 2, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000]

    # Create colorbar with specific ticks.  We take the log of the ticks since the data is also logarithmic.
    pcmcb = plt.colorbar(pcm, ticks=np.log10(ticks), fraction=0.04)
    # Create tick labels to account for the logarithmic scaling.
    pcmcb.set_ticklabels(ticks)
    pcmcb.ax.tick_params(labelsize=18)
    

    # Figure title
    ax.set_title("GLOBE Observer observations ({}".format(startdate)+" to {})".format(enddate),size=24)

    plt.tight_layout()
    plt.savefig("img/fig02_go_heatmap.png")

    #--------------------------------------------------------------------------
    # Figure B: Heatmap world map of GLOBE Observer data
    #--------------------------------------------------------------------------

    # Create lists of x and y points for the observations of interest.
    x = [ob.lon for ob in globeobs]
    y = [ob.lat for ob in globeobs]

    # Create a 2D histogram.
    histo, xedges, yedges = np.histogram2d(x, y, (np.arange(-180.0, 180.1, 1.0), np.arange(-90.0, 90.1, 1.0)))

    # In order to use pcolormesh, we need to transpose the array.
    histo = histo.T

    # Take logarithm of the array.  In this context, values naturally span multiple orders of magnitude.
    histo = np.log10(histo)

    # Do this so the colorbar saturates at 1e4
    # - histo is log10 transformed
    histosat = histo
    histosat[histo > 4] = 4

    # Create a figure and axis with cartopy projection.
    ax = plotters.make_pc_fig()

    # Convert the 1D lists of bin edges to 2D lists.
    xx, yy = np.meshgrid(xedges, yedges)

    # Plot as colormesh.
#    pcm = ax.pcolormesh(xx, yy, histo, cmap="Reds")
    pcm = ax.pcolormesh(xx, yy, histosat, cmap="Reds")

    # Create colorbar with specific ticks.  We take the log of the ticks since the data is also logarithmic.
    pcmcb = plt.colorbar(pcm, ticks=np.log10(ticks), fraction=0.04)
    # Create tick labels to account for the logarithmic scaling.
    pcmcb.set_ticklabels(ticks)
    pcmcb.ax.tick_params(labelsize=18)

    # Figure title
    ax.set_title("GLOBE observations ({}".format(startdate)+" to {})".format(enddate),size=24)

    plt.tight_layout()
    plt.savefig("img/fig02_globe_only_heatmap.png")


if __name__ == "__mainfig02__":
    mainfig02()