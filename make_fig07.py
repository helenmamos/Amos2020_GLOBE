#------------------------------------------------------------------------------
# MAKE_FIG07.PY
#  
# PURPOSE
# Plot the count for each GLOBE Observer quality flag
# This is Figure 7 from Amos & Starke et al. 2020 (in prep)
#
# RESOURCES
# - GLOBE Observer website: observer.globe.gov
# - GLOBE Data User Guide: https://www.globe.gov/globe-data/globe-data-user-guide
# - Download the GLOBE Observer app: https://observer.globe.gov/about/get-the-app
#
# MODIFICATION HISTORY
# 17 Oct 2019 - HM Amos - v1.0 created based on figure_S006.py by MJ Starke
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
import pprint

def mainfig07(): 
    
    # Uncomment this line if you want to see what the quality flags look like
    # for traditional GLOBE data only. 
    # !!! Don't forget to comment it out when you're done !!!
    #obs = globeobs
    
    # Total number of observations per protocol
    num_obs_pro = np.empty(len(protocols))
    for k in range(len(protocols)):
        num_obs_pro[k] = len([ob for ob in obs if ob["protocol"] == protocols[k]])
        
    # Print stats for the paper    
    print('---+ Number of GO obs per protocol = ', num_obs_pro) # 

    # Do QC, to include land geometry detection.
    tools.do_quality_check(obs, tools.prepare_earth_geometry())

    # This dictionary is {'flag code': count}, where
    # - 'flag code' is a 2-3 letter abbreviation for given quality flag
    # - count is the total number of incidences of that quality flag 
    flags = tools.get_flag_counts(obs)

    # This dictionary will be {'flag code': {'protocol: count}} - i.e., it is 
    # a dictionary of dictionaries. 
    # Example: {'LW': {'GLOBE Observer App': 26}}
    flags2 = dict()

    # For each flag...
    for flag in flags:
        # Filter to only the obs which have this flag
        obsFlagged = tools.filter_by_flag_sets(obs, all_of=[flag])
    
        # Set the flags2 entry to the dictionary of source=count pairs
        flags2[flag] = tools.find_all_values(obsFlagged, "protocol")# debugging

    # Pretty print counts by flag and protocol   
    print(' ')    
    print('Quality flag counts by GLOBE Observer protocol: ')    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(flags2)
    print(' ')
    print('----+ Number of GO obs flagged           : ',sum(flags.values()))
    
    # FOR THE PAPER
    print('----+ Percent of GO observations flagged      : ',sum(flags.values())/len(obs)*100.)
    print('----+ Percent of GO observations with LW flag : ',sum(flags2['LW'].values())/len(obs)*100) 

    # This dictionary will contain a list of all the counts for a given flag 
    # from each source. Since the key for a given source may not exist, we 
    # check specifically for that and set to 0 when a key doesn't exist.
    source_counts = dict()

    for source_name in ['sky_conditions','land_covers', 'mosquito_habitat_mapper','tree_heights']:
        source_counts[source_name] = [
            flags2[flag][source_name] if source_name in flags2[flag] else 0 for flag in sorted(flags2.keys())
        ]

    #------------------------------------------------------------------------------
    # FIGURE A: Absolute flag counts
    #------------------------------------------------------------------------------
    
    # Array of aboslute counts for plotting
    y_array = np.array([source_counts[k] for k in source_counts])

    # Draw bar chart of absolute counts
    ax = plotters.plot_stacked_bars(
        x=range(len(flags)),
        ys=y_array,
        labels=['Clouds','Land Cover','Mosquito Habitat Mapper','Trees'],
        colors=[std_colors[k] for k in source_counts],
        figsize=(8, 6)
    )

    # Axes labels and tick marks
    ax.set_xticks(range(len(flags)))
    ax.set_xticklabels(sorted(flags2.keys()))
    ax.set_xlabel("Flag")
    ax.set_ylabel("Count")
    ax.grid(axis="y")

    # Figure title
    ax.set_title("GLOBE Observer quality control flags ({}".format(startdate)+
    " to {}".format(enddate)+")")

    # Fill frame with figure
    plt.tight_layout()

    # Save figure to png
    plt.savefig("img/fig07a_go_qaflags_abs.png")

    #------------------------------------------------------------------------------
    # FIGURE B: Flag counts expressed as a percent (relative to each protocol) 
    #           and stacked on top of each other
    #------------------------------------------------------------------------------

    # Array of percents for plotting
    pr_array = np.array([source_counts[k] for k in source_counts]) # integer
    pr_array = pr_array * 1.                                       # float64

    # Calculate the percent (%) of observations flagged by protocol
    for j in range(len(protocols)):
        # For each protocol, divide the absolute flag count by the total number of observations
        pr_array[j,] = np.divide(pr_array[j,], num_obs_pro[j])

        # Multiple by 100% to convert to a percent
        pr_array[j,] = np.multiply(pr_array[j,],100.)

    # Draw bar chart of flag percentages
    ax = plotters.plot_stacked_bars(
        x=range(len(flags)),
        ys=pr_array,
        labels=['Clouds','Land Cover','Mosquito Habitat Mapper','Tree Height'],
        colors=[std_colors[k] for k in source_counts],
        figsize=(8, 6)
    )

    # Axes labels and tick marks
    ax.set_xticks(range(len(flags)))
    ax.set_xticklabels(sorted(flags2.keys()))
    ax.set_xlabel("Flag")
    ax.set_ylabel("Percent (%)")
    ax.grid(axis="y")

    # Figure title
    ax.set_title("GLOBE Observer quality control flags ({}".format(startdate)+
    " to {}".format(enddate)+")")

    # Fill frame with figure
    plt.tight_layout()

    # Save figure to png
    plt.savefig("img/fig07b_go_qaflags_percent.png")

    #------------------------------------------------------------------------------
    # FIGURE C: Flag counts expressed a total percent % of the data
    #------------------------------------------------------------------------------

    # Initialize array of percents for plotting
    pr_array = np.array([source_counts[k] for k in source_counts]) # integer
    pr_array = pr_array * 1.                                       # float64
    
    # Sanity check
    if 0:
        print(pr_array.shape)
    
    # Sum over all protocols to get total number of observations per flag
    sum_array = np.sum(pr_array,axis=0)
    
    # Calculate total number of GLOBE Observer observations
    total_num_go_obs = np.sum(num_obs_pro)
    
    # Calculate the total percent of obs per flag
    total_pr_array = np.divide(sum_array, total_num_go_obs)
    
    # Multiply to convert to percent
    total_pr_array = np.multiply(total_pr_array,100.)
    
    # Sanity check
    if 0:
        print(total_pr_array.shape)

    # Create a figure.
    fig = plt.figure(figsize=(8,6))
    ax = fig.add_subplot(111)

    # Collect artists for the legend.
    artists = []

    # Plot the group of bars.
    bar = ax.bar(range(len(flags)), total_pr_array, color='dimgray')
    artists.append(bar)


    # Add legend
    ax.legend(artists, labels=['All GLOBE Observer data'])

    # Axes labels and tick marks
    ax.set_xticks(range(len(flags)))
    ax.set_xticklabels(sorted(flags2.keys()))
    ax.set_xlabel("Flag")
    ax.set_ylabel("Percent (%)")
    ax.grid(axis="y")

    # Figure title
    ax.set_title("GLOBE Observer quality control flags ({}".format(startdate)+
    " to {}".format(enddate)+")")

    # Fill frame with figure
    plt.tight_layout()

    # Save figure to png
    plt.savefig("img/fig07c_go_qaflags_totalpercent.png")


if __name__ == "__mainfig07__":
    mainfig07()
