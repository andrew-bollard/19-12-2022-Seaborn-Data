#!/usr/bin/env python
# coding: utf-8

# In[40]:


import pandas as pd
import seaborn as sns
import requests
from bs4 import BeautifulSoup
import json 
import numpy as np
import os
cwd = os.getcwd()


# In[41]:


# The aim of this project is to explore the number and geographic distribution of Ukrainian refugees in Ireland since 2022. 
# I intend to map this to housing data and the Pobal Deprivation Index to explore the relationship between:
# 1. The number of Ukrainian refugees in a given area;
# 2. The relative wealth of that area;
# 3. The current housing stock in that area.
# From this analysis, I wish to derive insights into the appropriateness of a given area for housing refugees

# First I will import a CSO dataset on the number of Ukrainian refugees who have arrived in each Local Electoral Area in Ireland in 2022 in XLSX format:
ukraine_arrivals_county_xlsx  = pd.read_excel(r"C:\Users\andyb\OneDrive\Documents\Ukraine Arrivals 2022.xlsx", sheet_name = "No. of arrivals")
ua_df1 = pd.DataFrame(ukraine_arrivals_county_xlsx)
ua_df1.head()

# Note that the data in this table is cumulative; the figure in each LEA for each successive month includes the previous figures from previous months.


# In[42]:


# I will filter by December 12th to get the latest figure for each LEA
mask1 = ua_df1["Day"].str.contains("2022 December 12")
ua_df1[mask1].head()


# In[43]:


# Next, I will import another sheet from the same XLSX file with the number of Ukrainian refugees in each LEA as a percentage of the population:
ukraine_arrivals_percentage_of_pop_xlsx  = pd.read_excel(r"C:\Users\andyb\OneDrive\Documents\Ukraine Arrivals 2022.xlsx", sheet_name = "Arrivals as % of Pop")
ua_df2 = pd.DataFrame(ukraine_arrivals_percentage_of_pop_xlsx)


# In[44]:


# I will filter by December 12th to get the latest figure for each LEA
mask2 = ua_df2["Day"].str.contains("2022 December 12")
ua_df2[mask2].head()


# In[45]:


# I will now merge these tables 
ua_arrivals_overview = pd.merge(ua_df1, ua_df2)
ua_arrivals_overview.loc[(ua_arrivals_overview["County"] == "Kerry") & (ua_arrivals_overview["Day"] == "2022 December 12")]


# In[46]:


mask3 = ua_arrivals_overview["Day"].str.contains("2022 December 12")
ua_arrivals_overview[mask3].loc[:]


# In[18]:


grouped_counties = ua_arrivals_overview[mask3].groupby(["Day", "County"]).sum("No. of people")
ua_arrivals_overview_grouped = pd.DataFrame(grouped_counties)
ua_arrivals_overview_grouped.loc[:]
    


# In[ ]:





# In[ ]:




