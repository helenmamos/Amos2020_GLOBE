#------------------------------------------------------------------------------
# MAKE_FIG03.PY
#  
# PURPOSE
# Plot locations of GLOBE Observer observations on a map as symbols
# This is Figure 3 of the Amos & Starke et al. (in prep)
#
# RESOURCES
# - GLOBE Observer website: observer.globe.gov
# - Download the GLOBE Observer app: https://observer.globe.gov/about/get-the-app
# - GLOBE Data User Guide: https://www.globe.gov/globe-data/globe-data-user-guide
# - GLOBE API: https://www.globe.gov/globe-data/globe-api
#
# MODIFICATION HISTORY
# XX Jul 2019 - MJ Starke - v1.0 created
# 01 Oct 2019 - HM Amos   - Modified to plot a range of dates instead of just
#                           one day of observations, and to have the option to 
#                           plot only observations made with the GLOBE Observer
#                           mobile app. Based on example_scatter_map.py and
#                           figure_S012.py by MJ Starke   
# 02 Dec 2019 - HM Amos   - Move global variables used by other plotting 
#                           routines to data_common.py. Modify so make_fig02 
#                           can be called by main.py            
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

def mainfig03(): 
    
    #--------------------------------------------------------------------------
    # Figure A: Plot locations of clouds, land cover, mosquito, and tree heigh
    #           GLOBE observer data on a single world map
    #--------------------------------------------------------------------------

    # Create a figure and axis with cartopy projection.
    ax = plotters.make_pc_fig()

    # Prepare to collect artists for the legend.
    artists = []

    # Define colors and makers for each protocol.
    # - use the same standard colors used in Figure 6
    colors = ("blue", "orange", "firebrick", "darkgreen")
    markers = ("^", "v", "X", "d")    
    
    # For each of those sources...
    for a in range(4):
        # Get the observations that have that protocol.
        obs_from_protocol = [ob for ob in obs if ob["protocol"] == protocols[a]]
       
        # Plot
        artists.append(plotters.plot_ob_scatter(obs_from_protocol, ax, s=40, marker=markers[a], color=colors[a]))

    # Add a legend.
    legend_labels = ["Clouds","Land Cover", "Mosquito Habitats","Tree Height"]
    ax.legend(artists, legend_labels, loc="lower left",prop={'size':16})    

    # Add figure title
    ax.set_title("GLOBE Observer observations from {}".format(startdate)+" to {}".format(enddate),size=20)

    # Finalize plot
    plt.tight_layout()

    # Save figure                           
    plt.savefig("img/fig03_go_obs_locations.png")
    
    #--------------------------------------------------------------------------
    # Figure B: Plot locations of clouds, land cover, mosquito, and tree heigh
    #           GLOBE observer data on separate maps
    #--------------------------------------------------------------------------
    
    # Legend labels
    # - Each label has to be passed as an iterable string (list or tuple), so
    #   that's why it's a list of lists
    legend_labels2 = [['Clouds'],['Land Cover'],['Mosquito Habitats'],['Tree Height']]

    for a in range(4):

        # Create a figure and axis with cartopy projection.
        ax = plotters.make_pc_fig()
        
        # Create artists for legend
        artists = []
    
        # Get the observations that have that protocol.
        obs_from_protocol = [ob for ob in obs if ob["protocol"] == protocols[a]]
        
        # Plot
        artists.append(plotters.plot_ob_scatter(obs_from_protocol, ax, s=40, 
                                                marker="^", color=colors[a]))

        # Add a legend
        ax.legend(artists,legend_labels2[a], loc="lower left",prop={'size':26},
                  markerscale=3)    

#    # Add figure title
#    ax.set_title("GLOBE Observer observations from {}".format(startdate)+" to {}".format(enddate),size=20)

        # Finalize plot
        plt.tight_layout()
 
        # Save figure                           
        plt.savefig("img/fig03_obs_locations_"+protocols[a]+".png")



if __name__ == "__mainfig03__":
    mainfig03()