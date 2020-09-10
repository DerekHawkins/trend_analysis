# Plotly credentials can be created by creating a Plotly account 
import json
with open('C:/Users/Derek.Hawkins/Credentials/PlotlyCredentials.json') as f:
    creds = json.load(f)

import math
x = float('nan')

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

import chart_studio
chart_studio.tools.set_credentials_file(username=creds['username'], 
                                        api_key=creds['password']) #add credentials 
import plotly.graph_objects as go
import chart_studio.plotly as py

# Path to your Keyword Planner Tool CSV file
path = 'historical_data.csv'


# Data Import and Structuring
df = pd.read_csv(path, encoding = "utf-16", skiprows=2, sep='\t').drop(index=[0,1]).reset_index(drop=True)
df = df.drop(columns=['Currency', 'Segmentation', 'Competition (indexed value)' ,
                      'Competition', 'Top of page bid (low range)', 
                     'Top of page bid (high range)', 'Ad impression share', 
                      'Organic average position', 
                     'Organic impression share', 'In Account'])

# Formatting and Sum
trend_data = []
for i in df.columns[2:len(df.columns)]:
    search_sum = df[i].sum()
    date = str(i).replace('Searches: ', '')
    data = {'Date': date,
           'Search Volume': search_sum}
    trend_data.append(data)
    
df_trend = pd.DataFrame(trend_data)
df_trend["Date"] = pd.to_datetime(df_trend["Date"])
df_trend.index = df_trend['Date']
df_trend = df_trend.drop(columns=['Date'])
#normalized =(df_trend-df_trend.min())/(df_trend.max()-df_trend.min())

# Pivoting, percentage calculation and reformatting
pivot = df_trend.pivot_table(index=df_trend.index, values='Search Volume', aggfunc=np.sum)
df_trend['Year'] = df_trend.index.year
df_trend['Month'] = df_trend.index.month
pivot_year = df_trend.pivot_table(index=['Year'], values='Search Volume', aggfunc=np.mean)
pivot_month = df_trend.pivot_table(index=['Year','Month'], values='Search Volume', aggfunc=np.mean)
pivot_month = pivot_month.rename(columns={'Search Volume': 'svMonth'})
df_merge = pivot_year.merge(pivot_month, left_index=True, right_index=True, how='left')
df_merge = df_merge.rename(columns={'Search Volume': 'Yearly Average', 
                                   'svMonth': 'Monthly Volume'})
df_merge = df_merge[['Monthly Volume', 'Yearly Average']]
df_merge['Percentage Change'] = (df_merge['Monthly Volume']-df_merge['Yearly Average'])/df_merge['Yearly Average']
final_pivot = df_merge.pivot_table(index=['Year'], columns=['Month'], values='Percentage Change')
for i in range(len(final_pivot)):
    final_pivot.iloc[i] = final_pivot.iloc[i].apply(lambda x: f'{round(x, 2)}%' if math.isnan(x) == False else float('NaN'))
final_pivot = final_pivot.rename(columns={1: 'January', 2: 'February', 3: 'March', 4: 'April', 
                                         5: 'May', 6: 'June', 7: 'July', 8: ' August', 9:'September', 
                                         10: 'October', 11: 'November', 12: 'December'})

#Data Plotting
data = [go.Scatter(x=final_pivot.columns,
                   y=final_pivot.loc[year],
                   name=year) for year in final_pivot.index]

layout = go.Layout(
    title='title',
    yaxis=dict(title='Percentage Change', 
              tickformat=".2%"),
    xaxis=dict(title='Months')
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='title')
