#------------------------------------------------------------------------------
# MAKE_FIG06.PY
#  
# PURPOSE
# Plot pie chart of completeness of GLOBE Observer photo submissions
# This is Figure 6 from Amos & Starke et al. 2019 (in prep)
#
# RESOURCES
# - GLOBE Observer website: observer.globe.gov
# - GLOBE Data User Guide: https://www.globe.gov/globe-data/globe-data-user-guide
# - Download the GLOBE Observer app: https://observer.globe.gov/about/get-the-app
#
# MODIFICATION HISTORY
# 09 Oct 2019 - HM Amos - v1.0 created based on figure_S002.py by MJ Starke
# 02 Dec 2019 - HM Amos - Move global variables used by other plotting modules
#                         to data_common.py. Modify so make_fig02 can be called 
#                         by main.py            
# 27 Feb 2020 - HM Amos - Updates to deal with latest API update. Photo URLs
#                         are now 'null' if a participant didn't submit anything,
#                         so you have to explicitly check for 'nulls' when
#                         counting photos.         
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
from globeqa import tools

def mainfig06(): 

    # Figure 6 only plots clouds and land cover because they're the only 
    # protocols with 6 standard photos (north, east, south, west, up, down)
    
    # If you want to see what the pie charts look like just for clouds, uncomment:
    #obs5 = go_cld_obs
    #
    # If you want to see what the pie charts look like just for land cover, uncomment:
    #obs5 = go_lc_obs
    
    # Prepare dict to collect plotted values.
    vals = {"0 photos": 0, "1 photo": 0, "2 photos": 0, "3 photos": 0, "4 photos": 0, "5 photos": 0, "6 photos": 0}
    vals_2 = {"North": 0, "East": 0, "South": 0, "West": 0, "Upward": 0, "Downward": 0}

    # For each observation...
    for ob in tqdm(obs5, desc="Sifting observations"):
        # Count how many photos are included, check for 'nulls'
#        photos = len(ob.photo_urls)
        photos = 0
        if ob.photo_urls['North'] != 'null': photos +=1
        if ob.photo_urls['East'] != 'null': photos +=1
        if ob.photo_urls['South'] != 'null': photos +=1
        if ob.photo_urls['West'] != 'null': photos +=1
        if ob.photo_urls['Upward'] != 'null': photos +=1
        if ob.photo_urls['Downward'] != 'null': photos +=1                

        # Increment count 
        vals["{} photo{}".format(photos, "s" if photos != 1 else "")] += 1

        # If 5 (of 6) photos were submitted, record which direction was submitted
        # Check for 'nulls'
        if photos == 5:
            for direction in vals_2.keys():
#                if direction not in ob.photo_urls.keys():
                if ob.photo_urls[direction] != 'null':
                    vals_2[direction] += 1

    # Compute total number of observations for calculating percentages for slice labels
    total = sum(vals[k] for k in vals)    

    #--------------------------------------------------------------------------
    # Figure A: Pie chart of number of photos submitted per observation
    #-------------------------------------------------------------------------- 
    
    # Define figure and frame size
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    # Draw pie chart    
    ax.pie([vals[k] for k in vals], labels=["{} ({:.2%})".format(k, v / total) for k, v in vals.items()],
           labeldistance=1.1, colors=["silver", "gold", "yellowgreen", "lightcoral", "orange", "plum","lightskyblue"])

    # Figure title
    ax.set_title("Photos submitted with a GO observation\n" 
                 "({}".format(startdate)+" to {}".format(enddate)+")")

    # Fill frame with figure
    plt.tight_layout()
    
    # Save figure without legend
    plt.savefig("img/fig05a_photonum_pie_wolegend.png")
        
    # Add legend
#    ax.legend()
        
    # Save figure with legend
    plt.savefig("img/fig06a_photonum_pie_wlegend.png")
    
    #--------------------------------------------------------------------------
    # Figure B: Pie chart of direction omitted when 5 photos are submitted
    #--------------------------------------------------------------------------    
    
    # Compute total number of observations for calculating percentages for slice labels
    total = sum(vals_2[k] for k in vals_2)
    print(total)

    # Define figure and frame size
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)

    # Draw pie chart
    ax.pie([vals_2[k] for k in vals_2], labels=["{} ({:.2%})".format(k, v / total) for k, v in vals_2.items()],
               labeldistance=1.1,colors=["gold", "yellowgreen", "lightcoral", "orange", "plum","lightskyblue"])

    # Figure title
    ax.set_title("Direction omitted when 5 photos are submitted\n" 
                 "({}".format(startdate)+" to {}".format(enddate)+")")

    # Fill frame with figure
    plt.tight_layout()

    # Save figure without legend
    plt.savefig("img/fig06b_photodiromit_pie_wolegend.png")

    # Add legend
#    ax.legend()

    # Save figure with legend
    plt.savefig("img/fig06b_photodiromit_pie_wlegend.png")

if __name__ == "__mainfig06__":
    mainfig06()
