#------------------------------------------------------------------------------
# DATA_COMMON.PY
#  
# PURPOSE
# Define global variables used to read and parse GLOBE data for plotting
#
# MODIFICATION HISTORY
# 02 Dec 2019 - HM Amos - v1.0 created 
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
from datetime import date, timedelta
from globeqa import tools, plotters

# Define the GLOBE Observer protocols you want the data for
protocols = ["sky_conditions", "land_covers", "mosquito_habitat_mapper", "tree_heights"]

# Define start & end date of daterange
startdate = date(2019,11,28)    # start of date range, format is YYYY,MM,DD
enddate   = date(2019,12,1)   # end   of date range, format is YYYY,MM,DD

# Download GLOBE observations from API for given protocol(s) and date range
path = tools.download_from_api(protocols, startdate, enddate)

# Parse the downloaded file
rawobs = tools.parse_json(path)

# Filter for only observations made with the GLOBE Observer app
#   Tip: To display the contents of a single observation, type the following in
#        the iPython console: 
#   > tools.pretty_print_observation(obs[0])
obs = [ob for ob in rawobs if ob["DataSource"] == "GLOBE Observer App"]

# Filter for only GLOBE observations (i.e., not the app)
globeobs = [ob for ob in rawobs if ob["DataSource"] != "GLOBE Observer App"]

# Filter for cloud and land cover observations from the GLOBE Observer app
# - for Figure 5
obs5 = [ob for ob in rawobs if (ob["protocol"] in ["land_covers","sky_conditions"] and \
                             ob["DataSource"] == "GLOBE Observer App")]

# Filter for all (GO + GLOBE) cloud observations
# - for Colon-Robles et al. 2020, BAMS
all_cld_obs = [ob for ob in rawobs if (ob["protocol"] in ["sky_conditions"])]


# Filter for GLOBE Observer observations by protocol
# - for photo stats for the paper
go_cld_obs = [ob for ob in rawobs if (ob["protocol"] in ["sky_conditions"] and \
                             ob["DataSource"] == "GLOBE Observer App")]

go_mhm_obs = [ob for ob in rawobs if (ob["protocol"] in ["mosquito_habitat_mapper"] and \
                             ob["DataSource"] == "GLOBE Observer App")]

go_lc_obs = [ob for ob in rawobs if (ob["protocol"] in ["land_covers"] and \
                             ob["DataSource"] == "GLOBE Observer App")]

go_th_obs = [ob for ob in rawobs if (ob["protocol"] in ["tree_heights"] and \
                             ob["DataSource"] == "GLOBE Observer App")]

    
