#------------------------------------------------------------------------------
# STATS_FOR_PAPER.PY
#  
# PURPOSE
# Compute and print statistics for Amos et al. 2019 (in prep)
#
# MODIFICATION HISTORY
# 03 Dec 2019 - HM Amos - v1.0 created 
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
import numpy as np

# from christoph
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt

def mainstats(): 

    #--------------------------------------------------------------------------
    # Generic stats
    #--------------------------------------------------------------------------    
    
    # Number of total observations
    numallobs   = len(rawobs)     # GLOBE + GLOBE Observer
    numgoobs    = len(obs)        # just GLOBE Observer
    numglobeobs = len(globeobs)   # just GLOBE

    # Total number of GLOBE observations per protocol
    # - Number of GLOBE Observer observations per protocol computed in make_fig06.py
    num_globeobs_pro = np.empty(len(protocols))
    for k in range(len(protocols)):
        num_globeobs_pro[k] = len([ob for ob in globeobs if ob["protocol"] == protocols[k]])
         
    #--------------------------------------------------------------------------
    # Photo stats
    #--------------------------------------------------------------------------    
        
    # Compute total number of GLOBE Observer photos
    numphotos = 0    
    # For each observation...
    for ob in obs:
        # Number of photos included with a single observation
        photos = len(ob.photo_urls) 
        
        # Add to total photo count
        numphotos = numphotos + photos
        
    # Compute total number of GLOBE photos
    numglobephotos = 0    
    # For each observation...
    for ob in globeobs:
        # Number of photos included with a single observation
        photos = len(ob.photo_urls) 
        
        # Add to total photo count
        numglobephotos = numglobephotos + photos

    # Compute total number of GLOBE Observer photos by protocol
    
    # GLOBE Observer osbervations parsed by protocol
    # - this is a list of lists
    go_pro_obs = [go_cld_obs, go_mhm_obs, go_lc_obs, go_th_obs]
    
    # Intialize counters
    num_go_photos  = [0,0,0,0]
    num_go_classif = [0,0,0,0] 
    cc = 0
    
    # For each protocol...
    for go in go_pro_obs:   
        
       # # For each protocol...
       # go_obs = go_pro_obs[go]
        
        # For each observation...
        for ob in go:
            # Number of photos included with a single observation
            photos = len(ob.photo_urls) 
        
            # Add to total photo count
            num_go_photos[cc] = num_go_photos[cc] + photos
            
            # Check if cloud type was classified by observer
            if (cc == 0) and (len(ob.cloud_types) > 0):
                # Increment counter for number of cloud classifications
                num_go_classif[cc] = num_go_classif[cc] + 1
                
            # Check if mosquito genus was classified by observer
            if (cc == 1 ) and (len(ob.mosquito_genus) > 0):
                # Increment counter for number of mosquito genus classifications
                num_go_classif[cc] = num_go_classif[cc] + 1
                
            # Check if land cover type was classified by the observer
            if (cc == 2 ) and (ob.which_muc is not None):
                # Increment counter for number of land cover type classifications
                num_go_classif[cc] = num_go_classif[cc] + 1            
            
        
        # Increment index 
        cc = cc + 1

    #--------------------------------------------------------------------------
    # Calculate the number of unique participants contributing observations
    #
    # Acknowledgement:
    # H.M. Amos would like to thank C.A. Keller at NASA Goddard Space Flight
    # Center for help figuring out this block of code. (2020-02-21)
    #--------------------------------------------------------------------------  
    
    # extract user IDs
    # - Each app user is assigned a unique ID number 
    # - The user ID of the participant who took the observation is associated
    #   with each data point
    MyData = pd.DataFrame()
    MyData['Userid'] = [int(i['Userid']) for i in obs]

    # extract dates and add them to the data frame
    MyData['ObsDate'] = [dt.datetime.strptime(i['MeasuredAt'],"%Y-%m-%dT%H:%M:%S") for i in obs]
    
    # Start and end dates of the 2019 Fall GLOBE Clouds Challenge
    EventDateStart = dt.datetime(2019,10,15)
    EventDateEnd = dt.datetime(2019,11,15)
    
    # Unique user IDs up until the start of the 2019 Fall Challenge    
    UniqueIDsBefore2019 = MyData[MyData['ObsDate']<EventDateStart]['Userid'].unique()
    
    # Unique user IDs through the end of the 2019 Fall Challenge
    UniqueIDsAfter2019 = MyData[(MyData['ObsDate']<=EventDateEnd)]['Userid'].unique()
    
    # Start and end dates of the 2018 Spring GLOBE Clouds Challenge
    EventDateStart = dt.datetime(2018,3,15)
    EventDateEnd = dt.datetime(2018,4,15)
    
    # Unique user IDs up until the start of the 2018 Spring Challenge    
    UniqueIDsBefore2018 = MyData[MyData['ObsDate']<EventDateStart]['Userid'].unique()
    
    # Unique user IDs through the end of the 2018 Spring Challenge
    UniqueIDsAfter2018 = MyData[(MyData['ObsDate']<=EventDateEnd)]['Userid'].unique() 
    
    # Create a new data frame
    NewData = pd.DataFrame()
    
    # Extract just the unique days when we have observations
    NewData['Day'] = list(set([dt.datetime(i.year,i.month,i.day) for i in MyData['ObsDate']]))
    
    # Cumulative total of unique users contributing GLOBE Observer observations
    NewData['TotalUsers'] = [len(MyData[MyData['ObsDate']<idate]['Userid'].unique()) for idate in NewData['Day']]

    # Sort data by day
    NewData = NewData.sort_values(by='Day')
    
    # Number of new unique users contributing data each day
    NewData['NewUsers'] = [0]+list(np.diff(NewData['TotalUsers']))
    
    # Sanity check: Plot unique users
    if 0:
        plt.plot(NewData.Day,NewData.NewUsers)   # new users each day
        plt.plot(NewData.Day,NewData.TotalUsers) # cumulative total unique users over time
        plt.close()

 
    #--------------------------------------------------------------------------
    # Print stats to console
    #--------------------------------------------------------------------------    

    # Print numbers for the paper
    print('---+ Number of GLOBE obs per protocol                  : ', num_globeobs_pro)  
    print('---+ Number of GLOBE Observer observations             : ', numgoobs)
    print('---+ Ratio of (GLOBE+GO)/GLOBE observations            : ', numallobs/numglobeobs)
    print('---+ Number of GLOBE Observer photos                   : ', numphotos)
    print('---+ Number of GLOBE photos                            : ', numglobephotos)  
    print('---+ Number of GO cloud photos                         : ', num_go_photos[0])
    print('---+ Number of GO MHM photos                           : ', num_go_photos[1])
    print('---+ Number of GO land cover photos                    : ', num_go_photos[2])
    print('---+ Number of GO tree photos                          : ', num_go_photos[3])
    print('---+ Number of GO cloud obs with cloud type classified : ', num_go_classif[0])
    print('---+ Number of GO MHM obs with genus classified        : ', num_go_classif[1])
    print('---+ Number of GO LC obs with LC type classified       : ', num_go_classif[2])
    print('---+ Number of unique users who have contributed GO data    : ', NewData['TotalUsers'].values[-1])
    print('---+ Number of new users attracted by 2019 Fall Challenge   : ', len(UniqueIDsAfter2019)-len(UniqueIDsBefore2019))
    print('---+ Number of new users attracted by 2018 Spring Challenge : ', len(UniqueIDsAfter2018)-len(UniqueIDsBefore2018))
    
if __name__ == "__mainstats__":
    mainstats()