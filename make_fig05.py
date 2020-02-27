#------------------------------------------------------------------------------
# MAKE_FIG05.PY
#  
# PURPOSE
# Plot diurnal distribution of GLOBE Observer submissions
# This is Figure 5 from Amos & Starke et al. 2019 (in prep)
#
# RESOURCES
# - GLOBE Observer website: observer.globe.gov
# - GLOBE Data User Guide: https://www.globe.gov/globe-data/globe-data-user-guide
# - Download the GLOBE Observer app: https://observer.globe.gov/about/get-the-app
#
# MODIFICATION HISTORY
# 08 Oct 2019 - HM Amos - v1.0 created based on figure_S013 by MJ Starke
# 02 Dec 2019 - HM Amos - Move global variables used by other plotting modules
#                         to data_common.py. Modify so make_fig02 can be called 
#                         by main.py            
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

def mainfig05(): 
    
    # Uncomment this line and re-run make_fig04 to see the diurnal 
    # distribution of GLOBE observations
    #obs = globeobs

    # Convert observation time to minutes (UTC)
    times = [60 * ob.measured_dt.hour + ob.measured_dt.minute for ob in obs]

    # Make historgram
    histo, bin_lefts = np.histogram(times, np.arange(0, 1441, 15))

    # Record the observations reported at exactly 00:00:00 UTC
    # - This is an error and a known issue isolated to a few GLOBE schools
    zeros = sum(1 for ob in obs if ob.measured_dt.hour == ob.measured_dt.minute == 0)

    # Define figure size
    fig = plt.figure(figsize=(11, 5))
    ax = fig.add_subplot(111)

    # Plot diurnal distribution of times when GLOBE Observer data are submitted
    ax.bar(bin_lefts[:-1], histo, align="edge", width=15, color="dimgray")

    # Define axes ranges and labels
    ax.set_xticks(np.arange(0, 1441, 60))
    ax.set_xticklabels(["{:0>2.0f}Z".format(v / 60) for v in np.arange(0, 1440, 60)] + ["00Z"])
    ax.set_xlim(0, 1440)
    ax.set_xlabel("Time (UTC)")
    ax.set_ylabel("Count")

    artists = [
        #ax.bar([0], zeros, align="edge", width=15, color="pink"),
        ax.axvline(6.5*60, ls=":", lw=2, c="black"),
        ax.axvline(11*60, ls="--", lw=2, c="black"),
        ax.axvline(18*60, ls="-.", lw=2, c="black"),
    ]

    # Figure title
    ax.set_title("Diurnal patttern of GLOBE Observer data submissions ({}".format(startdate)+
    " to {}".format(enddate)+")")

    # Fill frame with figure
    plt.tight_layout()

    # Save figure without legend
    plt.savefig("img/fig05_go_diurnaldist_wolegend.png")

    # Add legend
    ax.legend(artists, ["Noon India Standard Time",
                        "Noon Central European Time",
                        "Noon Central US Time"], loc="upper left")

    # Save figure with legend 
    plt.savefig("img/fig05_go_diurnaldist_wlegend.png")

if __name__ == "__mainfig05__":
    mainfig05()