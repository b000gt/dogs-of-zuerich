import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np

from .server import app
from .data import df, ages, years

@app.callback(
    Output(component_id='dog-ages', component_property='figure'),
    Input(component_id='select-section', component_property='value')
)
def update_graph(sections):
    if type(sections) != type([]):
        sections = [sections]
    fig = go.Figure()
    for section in sections:
        ages_count = []
        dff = df.copy()
        dff = dff[dff['STADTKREIS'] == section]
        dff = dff.groupby(by=['ALTER'])['dog_count'].count().reset_index()
        for age in ages:
            if len(dff[dff['ALTER'] == age]) == 0:
                ages_count.append(0)
            ages_count.extend(dff.loc[dff['ALTER'] == age, 'dog_count'].values)
        fig.add_trace(go.Scatter(
            x=ages,
            y=ages_count,
            mode='lines',
            name=f'Kreis {section:.0f}'
        ))
    return fig

title = html.H2('Age Distribution', className='col-md-6')

input = None

output = dcc.Graph(id='dog-ages', className='col-md-6', figure={})