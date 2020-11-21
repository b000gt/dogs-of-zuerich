import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import numpy as np

from .server import app
from .data import df, years, sections


@app.callback(
    Output(component_id='dog-years', component_property='figure'),
    Input(component_id='select-section', component_property='value')
)
def update_sections(sections):
    if type(sections) != type([]):
        sections = [sections]
    dff = df.copy()
    dff = dff.groupby(by=['STADTKREIS', 'GESCHLECHT_HUND', 'GEBURTSJAHR_HUND'])['dog_count'].count().reset_index()
    dff = dff[dff['STADTKREIS'].isin(sections)]
    fig = go.Figure()
    for sex in dff['GESCHLECHT_HUND'].unique():
        df_sex = dff.copy()
        df_sex = df_sex[df_sex['GESCHLECHT_HUND'] == sex]
        fig.add_trace(go.Bar(
            x=df_sex['GEBURTSJAHR_HUND'],
            y=df_sex['dog_count'],
            name=sex
        ))
    return fig

input = html.Div(className='col-md-12', children=[
    dcc.Dropdown(id='select-section',
        options=sections,
        multi=True,
        value=1
        )
    ])
title = html.H2('Adoptions over the Years', className='col-md-6')

output = dcc.Graph(id='dog-years', className='col-md-6', figure={})