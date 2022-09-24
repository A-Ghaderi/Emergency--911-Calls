#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Import numpy and pandas ##
import numpy as np
import pandas as pd

## Import visualization libraries and set %matplotlib inline ##
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')

## Read data ##
df = pd.read_csv('911.csv')

## Check the info ##
df.info()

## Check the head ##
df.head(3)


# In[ ]:


## Top 5 zipcodes for 911 calls ##
df['zip'].value_counts().head(5)

## Unique title codes ##
df['title'].nunique()


# In[ ]:


## A new column called "Reason" that contains just reasons from Title column ##
df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])

## The most common Reason for a 911 call based off of this new column ##
df['Reason'].value_counts()

## Countplot of 911 calls by Reason ##
sns.countplot(x='Reason',data=df,palette='viridis')


# In[ ]:


## Convert the column of TimeStamp from strings to DateTime objects ##
df['timeStamp'] = pd.to_datetime(df['timeStamp'])

## creating 3 new columns called Hour, Month, and Day of Week ##
df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)

dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)

## Countplot of the Month column with the hue based off of the Reason column ##
sns.countplot(x='Month',data=df,hue='Reason',palette='viridis')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


# In[ ]:


## Creating a gropuby object called byMonth, where you group the DataFrame by the month column and using the count() method for aggregation ##
byMonth = df.groupby('Month').count()
byMonth.head()

## create a simple plot off of the dataframe indicating the count of calls per month ##
byMonth['twp'].plot()
sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())


# In[ ]:


## Create a new column called 'Date' that contains the date from the timeStamp column ##
df['Date']=df['timeStamp'].apply(lambda t: t.date())

## groupby this Date column with the count() aggregate and create a plot of counts of 911 calls ## 
df.groupby('Date').count()['twp'].plot()
plt.tight_layout()

df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()


# In[ ]:


##  restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week ##
dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour.head()

##  create a HeatMap using this new DataFrame ##
plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')

## create a clustermap using this DataFrame ##
sns.clustermap(dayHour,cmap='viridis')

