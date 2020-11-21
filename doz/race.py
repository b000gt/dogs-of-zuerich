import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np

from .server import app
from .data import df, years

@app.callback(
    Output(component_id='dog-races', component_property='figure'),
    [Input(component_id='select-year', component_property='value'),
     Input(component_id='select-race-count', component_property='value')]
)
def update_graph(year, race_count):
    dff = df.copy()
    dff = dff.groupby(by=['RASSE1', 'GEBURTSJAHR_HUND'])['dog_count'].count().reset_index()
    dff = dff[dff['GEBURTSJAHR_HUND'] == year]
    dff = dff.sort_values(by='dog_count', ascending=False)
    RASSE = dff['RASSE1'].unique()
    all_races = RASSE[:race_count]
    all_races_count = []
    for race in all_races:
        all_races_count.append(int(dff[dff['RASSE1'] == race]['dog_count']))

    if len(all_races) >= race_count:
        all_races = np.append(all_races, ['Sonstige'])
        not_popular_dogs = dff[~dff['RASSE1'].isin(all_races)]
        all_races_count.append(not_popular_dogs.sum().iloc[2])

    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=all_races,
        values=all_races_count
    ))
    return fig

title = html.H2('Race Distribution', className='col-md-6')

input = html.Div(className='col-md-6', children=[
        dcc.Slider(id='select-race-count', min=1, max=100, step=1, value=7),
        dcc.Dropdown(id='select-year',
            options=years,
            multi=False,
            value=2016
            ),
    ])

output = dcc.Graph(id='dog-races', className='col-md-6', figure={})