#!/usr/bin/env python
# coding: utf-8

# Import libraries and functions
import dash
from dash import dcc
from dash import html
from dash import Input, Output
import time
from main import get_data, convert_data, reduce_data
from map import map_gen

# Initialize the Dash app
app = dash.Dash(__name__)

# Define function to get map based on drop-down input below
@app.callback(
    Output("state-figure", "srcDoc"), 
    Input("select-state", "value"), prevent_initial_call=False)
def get_graph(state_code):
    api_endpoint = 'https://api.weather.gov/alerts/active/area/' + state_code
    data = get_data(api_endpoint)
    alerts_ = convert_data(data)
    alerts = reduce_data(alerts_)
    map_gen(state_code, alerts).save('state_map.html')
    return open('state_map.html', 'r').read()

# Initialize a map to the default dropdown item
get_graph('OR')

# Define function with callback decorator to update the state header
@app.callback([Output('state_title', 'children')], 
              [Input('select-state', 'value')])
def update_state_header(state_code):
    s = state_dict[state_code]
    # Add date and time to the header, to accompany the selected state
    d = time.strftime("%B %d %Y",time.localtime())
    t = time.strftime("%H:%M:%S",time.localtime())
    return [html.H2(s+' | '+d+' @ '+t)]

# Set the title of the dashboard
app.title = "Real-Time PNW Weather Alerts"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
# States List
state_list = [{'State':'Oregon','Code':'OR'},
              {'State':'Washington','Code':'WA'},
              {'State':'Idaho','Code':'ID'},
              {'State':'Alaska','Code':'AK'}]
# Rework the states list for use in the header
state_dict = {s['Code']:s['State'] for s in state_list}

#---------------------------------------------------------------------------------------
# Layout
app.layout = html.Div([
    # Dashboard Title
    html.H1("Current PNW Weather Alerts",
            style={'textAlign': 'center',
                   'font-family':'Calibri',
                   'color': '#FFFFFF',
                   'font-size': 72}),
    # Dropdown menu to select state
    html.Div([dcc.Dropdown(
            id='select-state',
            options=[{'label': i['State'], 'value': i['Code']} for i in state_list], 
            value='OR',
            placeholder='Oregon',
            multi=False,
            clearable=False)],
            style={'width':'25%',
                   'font-family':'Calibri',
                   'textAlign':'center',
                   'color':'#000000',
                   'font-size':28,
                   'margin':'0 auto'}),
    # Title, which includes the state
    html.Div(id='state_title',
            style={'textAlign': 'center',
                   'font-family':'Calibri',
                   'color': '#FFFFFF',
                   'font-size': 36}),
    # The figure itself, called from the defined fucntion and decorator
    html.Div([
        html.Iframe(id='state-figure', 
                    width='75%' ,height='700')
        ], style={ 'textAlign': 'center'})
],style={'backgroundColor':'black'})

if __name__ == '__main__':
    ## Run this in testing
    # app.run_server(debug=True) 
    ## Run this when going 'live'
    app.run_server(host='0.0.0.0',
                   debug=False,
                   port=8050) 