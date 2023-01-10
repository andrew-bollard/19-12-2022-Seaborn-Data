#!/usr/bin/env python
# coding: utf-8

# In[66]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import json 
import numpy as np
import folium
import os
cwd = os.getcwd()


# In[41]:


# The aim of this project is to explore the number and geographic distribution of Ukrainian refugees in Ireland since 2022. 
# I will use Python to create:
# 1. Dataframes with the number of Ukrainian refugees in a given area;
# 2. a geographic plot of the top 5 counties by number of refugees hosted.

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
ua_arrivals_overview.dropna()
ua_arrivals_overview.loc[(ua_arrivals_overview["County"] == "Kerry") & (ua_arrivals_overview["Day"] == "2022 December 12")]


# In[46]:


mask3 = ua_arrivals_overview["Day"].str.contains("2022 December 12")
ua_arrivals_overview[mask3].loc[:]


# In[18]:


grouped_counties = ua_arrivals_overview[mask3].groupby(["Day", "County"]).sum("No. of people")
ua_arrivals_overview_grouped = pd.DataFrame(grouped_counties)
ua_arrivals_overview_grouped.loc[:]


# In[65]:


# I'll drop those columns in the middle; I'm not sure how they appeared, but they're adding no value:
ua_arrivals_overview_grouped.columns.get_level_values(0)


# In[67]:


ua_arrivals_overview_grouped.columns


# In[69]:


ua_arrivals_overview_grouped.drop(columns=['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7'], inplace=True, errors='ignore')


# In[70]:


ua_arrivals_overview_grouped.loc[:]


# In[71]:


# The Kenmare entry for Kerry appears to be missing, so that will need to be appended. A bigger problem is that the percentages have been summed, giving incorrect figures. 
# The percentage figures are for each LEA rather than the county as a whole and so cannot be summed.
#I will correct this now by dropping the percentage column from this DataFrame:
ua_arrivals_overview_people_only = ua_arrivals_overview_grouped.drop(columns = "Percentage (%) of Population")
ua_arrivals_overview_people_only.loc[:]


# In[72]:


# Now to append the value for Kerry by replacing 4743 with 6493 (4743 + 1750 which is the missing total no. of arrivals in Kenmare):
ua_arrivals_overview_people_appended = ua_arrivals_overview_people_only.replace(to_replace = 4743, value = 6493)
ua_arrivals_overview_people_appended.loc[:]


# In[73]:


# Now I'm going to create a chart for the top 5 counties by number of Ukrainians living there (Dublin, Kerry, Cork, Donegal, and Galway). 
# First, I need to create a dictionary for each county with the number of Ukrainians living there in each month.
# For this use case, I feel that it's qucker to pull the numbers from Excel, and I also want to demonstrate converting a dictionary into a chart;
# Therefore, I will simpply copy the numbers into my dictionaries:
dublin_ukrainians_by_month = {"May" : 5909, "June": 7479, "July": 9310, "August": 9644, "September": 10469, "October" : 10469, "November": 11108, "December": 11349}


# In[74]:


# I can now use Dublin as a template to quickly create the other dictionaries:
kerry_ukrainians_by_month = {"May" : 2248, "June": 2796, "July": 3027, "August": 3448, "September": 4717, "October" : 4717, "November": 5796, "December": 6493}
cork_ukrainians_by_month = {"May" : 2959, "June": 3828, "July": 4385, "August": 4682, "September": 5054, "October" : 5054, "November": 5475, "December": 6135}
donegal_ukrainians_by_month = {"May" : 1236, "June": 1683, "July": 1884, "August": 2298, "September": 3740, "October" : 3740, "November": 4441, "December": 4789}
galway_ukrainians_by_month = {"May" : 1585, "June": 2358, "July": 2790, "August": 3206, "September": 3291, "October" : 3291, "November": 3611, "December": 4025}


# In[75]:


# Now to create a DataFrame combining all these dictionaries:
D_UA_df = pd.DataFrame( data = dublin_ukrainians_by_month, index = ["Dublin"], columns = ["May", "June", "July", "August", "September", "October", "November", "December"])


# In[76]:


KY_UA_df = pd.DataFrame( data = kerry_ukrainians_by_month, index = ["Kerry"], columns = ["May", "June", "July", "August", "September", "October", "November", "December"])


# In[77]:


C_UA_df = pd.DataFrame( data = cork_ukrainians_by_month, index = ["Cork"], columns = ["May", "June", "July", "August", "September", "October", "November", "December"])


# In[78]:


DL_UA_df = pd.DataFrame( data = donegal_ukrainians_by_month, index = ["Donegal"], columns = ["May", "June", "July", "August", "September", "October", "November", "December"])


# In[79]:


G_UA_df = pd.DataFrame( data = galway_ukrainians_by_month, index = ["Galway"], columns = ["May", "June", "July", "August", "September", "October", "November", "December"])


# In[80]:


top_5_counties = [D_UA_df, KY_UA_df, C_UA_df, DL_UA_df, G_UA_df]


# In[81]:


top_5_df = pd.concat(top_5_counties)


# In[82]:


top_5_df.loc[:]


# In[83]:


top_5_df.index.name = "County"
top_5_df.loc[:]


# In[84]:


# I'm going to use Matplotlib to create a line plot of the data now:
fig, ax = plt.subplots()
top_5_df.plot(ax=ax)
ax.set_xlabel("County")
ax.set_ylabel("Number of Ukrainians")
plt.show()


# In[85]:


# This plot is not easy to understand in this format, so I'm going to transpose it to make it clearer:
top_5_df_transposed = top_5_df.T
fig, ax = plt.subplots()
top_5_df_transposed.plot(ax=ax)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Ukrainians")
ax.set_xticks(range(len(top_5_df_transposed.index)))
ax.set_xticklabels(top_5_df_transposed.index)
ax.set_xticklabels(top_5_df_transposed.index, rotation=20, fontsize=10)
plt.show()


# In[86]:


# Much better! This plot shows the clear difference between the number of Ukrainian refugees living in Dublin versus the next highest counties. 
# It also shows a more or less steady upward trend in numbers in all counties from May to December.


# In[87]:


# It would be interesting to plot the final number for 2022 (i.e. the December number) on a map:
counties = {
    'Dublin': [53.3498, -6.2603],
    'Donegal': [54.65, -8.11],
    'Kerry': [52.14, -9.52],
    'Cork': [51.89, -8.47],
    'Galway': [53.27, -9.05]
}

m = folium.Map(location=[53.1424, -7.6921], zoom_start=6)
for i, row in top_5_df.iterrows():
    folium.CircleMarker(location=counties[row.name],
                        radius=row['December']*0.01,
                        color='blue',
                        fill=True,
                        fill_color='blue').add_to(m)
m


# In[88]:


# Very nice; let's vary the colour a bit:

color_map = {'Dublin': 'blue', 'Cork': 'red', 'Kerry': 'green', 'Donegal': 'yellow', 'Galway': 'maroon'}

def color_by_county(county):
    return color_map[county]

m = folium.Map(location=[53.1424, -7.6921], zoom_start=7)
for county, coordinates in counties.items():
    folium.CircleMarker(location=coordinates,
                        radius=top_5_df.loc[county, "December"]*0.007,
                        color=color_by_county(county),
                        fill=True,
                        fill_color=color_by_county(county)).add_to(m)
m


# In[89]:


# The map plot further helps visualise the geographic distribution of refugees hosted among the top 5 counties in 2022.

# It's interesting that Kerry overtook Cork in 2nd place between October and November; why is this?
# I suspect it could be due to the availability of holiday homes, as Kerry has a large number of these.
# Holiday homes are typically vacant in the winter months and thus could potentially be used for temporary refugee accommodation, so this could be an explanation.
# To investigate, I will create a DataFrame with these 5 counties and the number of vacant holiday homes in each from May-December 2022.
# I will then create a plot with this data, similar to above, and see what I find.
# Of course, correlation does not equal causation, so I will have to corroborate any such finding with other sources.


# In[90]:


# First I will import another CSV file downloaded from the CSO website with data on the number of unoccupied holiday homes in Ireland in 2022:
holiday_homes_xlsx  = pd.read_excel(r"C:\Users\andyb\OneDrive\Documents\Holiday Homes and Vacant Dwelling Data.xlsx", sheet_name = "Data Cleaned")
holiday_homes_df1 = pd.DataFrame(holiday_homes_xlsx)
holiday_homes_df1.loc[:]


# In[ ]:





# In[91]:


# Time to clean this DataFrame.
# I'll start by removing the Vacant Dwelling rows:
holiday_homes_df2 = holiday_homes_df1[holiday_homes_df1['Type'] != 'Vacant Dwellings']
holiday_homes_df2.loc[:]


# In[92]:


# Next, I'll remove the other counties so that we're only left with the administrative counties that comprise Dublin, Cork, Kerry, Donegal, and Galway:
county_list = county_list = ['Cork County', 'Donegal', 'Galway County', 'Kerry', 'Dún Laoghaire-Rathdown', 'Cork City', 'Fingal', 'South Dublin', 'Galway City']
holiday_homes_filtered_df3 = holiday_homes_df2.loc[holiday_homes_df2['Administrative County'].isin(county_list)]
holiday_homes_filtered_df3.loc[:]


# In[93]:


# Dublin City, Donegal, and Galway County are missing from the dataframe, so I will append them manually:
missing_counties = {"Dublin City": 753, "Donegal": 12377, "Galway County": 4252}
missing_counties_df = pd.DataFrame({'Administrative County': ['Dublin City', 'Donegal', 'Galway County'], 'Type': ['Unoccupied Holiday Homes', 'Unoccupied Holiday Homes', 'Unoccupied Holiday Homes'], 'Number': [753, 12377, 4252]})
missing_counties_df = missing_counties_df.reset_index(drop=True)
holiday_homes_df4 = pd.concat([holiday_homes_filtered_df3, missing_counties_df], ignore_index=True)

# I'm dropping the "Type" column because it's irrelevant and starting to annoy me:
holiday_homes_df4 = holiday_homes_df4.drop(columns=['Type'])
holiday_homes_df4.loc[:]


# In[94]:


# Now we need to add the values for city and county:
holiday_homes_df5 = holiday_homes_df4.groupby('Administrative County', as_index=False)['Number'].sum()
dublin_mask = holiday_homes_df5['Administrative County'].isin(['Dublin City', 'Dún Laoghaire-Rathdown', 'Fingal', 'South Dublin'])
selected_rows = holiday_homes_df5[dublin_mask]
dublin_row = pd.DataFrame({'Administrative County': ['Dublin'], 'Number': [selected_rows['Number'].sum()]})
holiday_homes_df5 = holiday_homes_df5.drop(holiday_homes_df5[dublin_mask].index)
holiday_homes_df5 = pd.concat([holiday_homes_df5, dublin_row])
holiday_homes_df5.loc[:]


# In[95]:


holiday_homes_df6 = holiday_homes_df5.groupby('Administrative County', as_index=False)['Number'].sum()
cork_mask = holiday_homes_df6['Administrative County'].isin(['Cork City', 'Cork County'])
selected_rows = holiday_homes_df6[cork_mask]
cork_row = pd.DataFrame({'Administrative County': ['Cork'], 'Number': [selected_rows['Number'].sum()]})
holiday_homes_df6 = holiday_homes_df6.drop(holiday_homes_df6[cork_mask].index)
holiday_homes_df6 = pd.concat([holiday_homes_df6, cork_row])
holiday_homes_df6.loc[:]


# In[104]:


holiday_homes_df7 = holiday_homes_df5.groupby('Administrative County', as_index=False)['Number'].sum()
galway_mask = holiday_homes_df7['Administrative County'].isin(['Galway City', 'Galway County'])
selected_rows = holiday_homes_df7[galway_mask]
galway_row = pd.DataFrame({'Administrative County': ['Galway'], 'Number': [selected_rows['Number'].sum()]})
holiday_homes_df7 = holiday_homes_df6.drop(holiday_homes_df7[galway_mask].index)
holiday_homes_df7 = pd.concat([holiday_homes_df7, galway_row])
holiday_homes_df7.loc[:]


# In[105]:


# Just need to amend the value for Donegal:
holiday_homes_df7.loc[holiday_homes_df7['Number'] == 24754, 'Number'] = 12377
holiday_homes_df7.loc[:]


# In[106]:


# Now, a quick bar plot will help visualise this data:
sns.barplot(x='Administrative County', y='Number', data=holiday_homes_df7)


# In[107]:


# I want to reorder the bars from largest to smallest to be more aesthetically pleasing:
holiday_homes_df7_sorted = holiday_homes_df7.sort_values(by='Number', ascending=False)
sns.barplot(x='Administrative County', y='Number', data=holiday_homes_df7_sorted)
plt.show()


# In[108]:


# Perfect! Interesting to see that Donegal actually had the most number of unoccupied holiday homes in 2022. 
# This makes sense, since Donegal is a popular holiday destination in the summer but not as desirable for year-round residency.
# This is due to the unforgiving climate in winter, geographic isolation, underdeveloped infrastructure, and lack of economic opportunities.
# Based on these factors, one wonders if it is suitable long-term to accommodate refugees there.

# Back to the original question behind this data, Kerry did indeed have more unoccupied holiday homes than Cork in 2022.
# Kerry is another popular summer destination that's less desirable year-round for similar reasons to Donegal.
# I suspect that West Galway (i.e. Connemara) and West Cork account for the majority of unoccupied holiday homes in those counties.

# Kerry, Donegal, West Galway, and West Cork account for the most holiday homes in Ireland for the following reasons:
# Famous natural beauty,e.g. beaches and mountains
# A climate that can be pleasant in summer but harsh in winter, discouraging some people from year-round residency in favour of summer residency in holiday homes.
# Geographic isolation, including underdeveloped infrastructure
# The result of these factors is a large seasonal summer population in each county.

# These factors also beg the question of the suitability of holiday homes for long-term accommodation of refugees.
# Refugees need a wide range of supports, e.g. access to social welfare infrastructure, public transport, schools for children, and English language lessons for adults.
# These are generally less abundant in areas with large numbers of holiday homes, due to the seasonal nature of the population size.
# Jobs are also less abundant.
# All of these factors pose challenges for successful accommodation of refugees in these areas, and possible integration if that is their wish.


# In[ ]:




