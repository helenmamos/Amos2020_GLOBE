#------------------------------------------------------------------------------
# MAKE_FIG04.PY
#  
# PURPOSE
# Plot time series of number of GLOBE Observer observations per day
# This is Figure 4 from Amos & Starke et al. 2019 (in prep)
#
# RESOURCES
# - GLOBE Observer website: observer.globe.gov
# - GLOBE Data User Guide: https://www.globe.gov/globe-data/globe-data-user-guide
# - Download the GLOBE Observer app: https://observer.globe.gov/about/get-the-app
#
# MODIFICATION HISTORY
# 08 Oct 2019 - HM Amos - v1.0 created based on figure_S007 by MJ Starke
# 02 Dec 2019 - HM Amos - Move global variables used by other plotting modules
#                         to data_common.py. Modify so make_fig02 can be called 
#                         by main.py            
# 27 Feb 2020 - HM Amos - Add error check in case startdate is after the 2017
#                         eclipse         
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
from data_common import *
from figure_common import *
from datetime import date, timedelta

def mainfig04(): 
    
    # For Colon-Robles et al., 2020, BAMS
    # - Uncomment this line to plot the figure with GO+GLOBE cloud data
    #obs = all_cld_obs
    
    # Create a list of dates 
    day = startdate
    dates = []
    while day <= enddate:
        dates.append(day)
        day += timedelta(days=1)

    # Histogram observations by their measured date.
    counts, bin_edges = np.histogram([ob.measured_dt.date() for ob in obs], dates)

    # Make figure
    fig = plt.figure(figsize=(11, 3.5))
    ax = fig.add_subplot(111)
    ax.stackplot(bin_edges[:-1], counts,colors="dimgray")
    ax.set_xlabel("Date (UTC)")
    ax.set_ylabel("Observations per day")
    ax.set_xlim(startdate, enddate)
    ax.set_ylim(0, 3000)  # Cut off eclipse spike.
    ax.grid(axis="y")

    # Label events with unusually high observation count
    if startdate < date(2017,8,26):
        ax.text(date(2017, 8, 26),1600, "North American\nEclipse")
        ax.text(date(2018, 4, 1), 1600, "2018 Spring \nClouds Challenge")
        ax.text(date(2019, 7, 1), 1600, "2019 Fall \nClouds Challenge")

    # Figure title
    ax.set_title("GLOBE Observer observations ({}".format(startdate)+" to {})".format(enddate))

    # Fill frame with figure
    plt.tight_layout()

    # Save figure to PNG file
    plt.savefig("img/fig04_go_obs_per_day.png")

if __name__ == "__mainfig04__":
    mainfig04()

