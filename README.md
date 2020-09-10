# Seasonal Trend Analysis
For visualizing seasonality of historical keyword data from Google Keyword Planner Tool


## Requirements 
- Plotly Credentials (which can be created by [making an account](https://plotly.com/python/getting-started-with-chart-studio/)
- Historical keyword data in .csv format from [Google Keyword Planner Tool](https://ads.google.com/home/tools/keyword-planner/)

## How to Use
- Add plotly credentials within chart_studio.tools.set_credential_file()

(I store credentials in a separate JSON but they can be hardcoded in)
<br>
```
chart_studio.tools.set_credentials_file(username=creds['username'], 
                                        api_key=creds['password']) 
```

- Path location of histocial data to `path`
<br>

With Plotly, the visual should appear on your plotly account for additional editing and exporting
<br>
If you do not wish to use Plotly, you can also use matplotlib for visualizing purposes
<br>
```
fig = plt.figure(figsize=(20,5))

for year in range(len(final_pivot.index)):
    plt.plot(final_pivot.iloc[year])
    
plt.xticks(np.arange(len(final_pivot.columns)), final_pivot.columns, rotation = 90)
_ = plt.legend(final_pivot.index)
```
