#------------------------------------------------------------------------------
# MAIN.PY
#  
# PURPOSE
# Wrapper script that calls code to make the figures from Amos & Starke et al. 
# 2020 (in prep)
#
# MODIFICATION HISTORY
# 26 Nov 2019 - HM Amos - v1.0 created 
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

# Figure 1 of the manuscript is a schematic created in PowerPoint

# Imports
import make_fig02
import make_fig03
import make_fig04
import make_fig05
import make_fig06
import make_fig07
import stats_for_paper

# Call modules to make figures
make_fig02.mainfig02()
make_fig03.mainfig03()
make_fig04.mainfig04()
make_fig05.mainfig05()
make_fig06.mainfig06()
make_fig07.mainfig07()

# Compute and print statistics for the paper
stats_for_paper.mainstats()
