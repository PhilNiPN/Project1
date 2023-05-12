import numpy as np
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

energy_comp_df = pd.read_csv('household_power_consumption.txt', sep=';', na_values='?', parse_dates=[['Date', 'Time']],
                              infer_datetime_format=True, index_col=0)

time_df = energy_comp_df.interpolate(method='time')
hourly_df = time_df.resample('H').mean()
daily_df = time_df.resample('D').mean()
monthly_df = time_df.resample('M').mean()

minute_fig = go.Figure()
for feat in time_df.columns:
    minute_fig.add_trace(go.Scatter(x=time_df.index, y=time_df[feat], mode='lines', name=feat))
minute_fig.update_layout(title='Resample the data to minute index')

hour_fig = go.Figure()
# create plot for hour resample data
for feat in hourly_df.columns:
    hour_fig.add_trace(go.Scatter(x=hourly_df.index, y=hourly_df[feat], mode='lines', name=feat))
hour_fig.update_layout(title='Resample the data to hourly index')

day_fig = go.Figure()
# create plot for day resample data
for feat in daily_df.columns:
    day_fig.add_trace(go.Scatter(x=daily_df.index, y=daily_df[feat], mode='lines', name=feat))
day_fig.update_layout(title='Resample the data to daily index')

month_fig = go.Figure()
# create plot for month resample data
for feat in monthly_df.columns:
    month_fig.add_trace(go.Scatter(x=monthly_df.index, y=monthly_df[feat], mode='lines', name=feat))
month_fig.update_layout(title='Resample the data to monthly index')

# Define the layout of the dashboard
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Minutes', value='tab-1', children=[
            dcc.Graph(id='minute-graph', figure=minute_fig)
        ]),
        dcc.Tab(label='Hours', value='tab-2', children=[
            dcc.Graph(id='hour-graph', figure=hour_fig)
        ]),
        dcc.Tab(label='Days', value='tab-3', children=[
            dcc.Graph(id='day-graph', figure=day_fig)
        ]),
        dcc.Tab(label='Months', value='tab-4', children=[
            dcc.Graph(id='month-graph', figure=month_fig)
        ]),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)
