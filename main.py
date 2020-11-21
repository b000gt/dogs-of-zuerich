import pandas as pd
import numpy as np

import dash
import dash_html_components as html

import dash_core_components as dcc
import plotly.graph_objects as go

from dash.dependencies import Input, Output

df = pd.read_csv('20170308hundehalter.csv')
df['dog_count'] = 1

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

sections = []
STADTKREIS = df['STADTKREIS'].unique()
STADTKREIS.sort()
for x in STADTKREIS:
    if not np.isnan(x):
        print(x)
        sections.append({'label': f'Kreis {x:.0f}', 'value': x})

races = []
RASSE1 = df['RASSE1'].unique()
RASSE1.sort()
for x in STADTKREIS:
    if not np.isnan(x):
        sections.append({'label': f'Kreis {x:.0f}', 'value': x})

years = []
GEBURTSJAHR_HUND = df['GEBURTSJAHR_HUND'].unique()
GEBURTSJAHR_HUND.sort()
for x in GEBURTSJAHR_HUND[::-1]:
    years.append({'label': f'{x:.0f}', 'value': x})

app.layout = html.Div(children=[    
    html.H1('Dogs of Zuerich'),
    html.Div(style={'width': '33%', 'float': 'left'}, children=[
        html.H2('Adoptions over the Years'),
        dcc.Dropdown(id='select-section',
                    options=sections,
                    multi=True,
                    value=1
                    ),
        dcc.Graph(id='dog-years', figure={})
    ]),
    html.Div(style={'width': '33%', 'float': 'left'}, children=[
        html.H2('Race Distribution'),
        dcc.Slider(id='select-race-count', min=1, max=40, step=1, value=7),
        dcc.Dropdown(id='select-year',
                     options=years,
                     multi=False,
                     value=2016
                     ),
        dcc.Graph(id='dog-races', figure={})
    ])
])

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


@app.callback(
    Output(component_id='dog-races', component_property='figure'),
    [Input(component_id='select-year', component_property='value'),
     Input(component_id='select-race-count', component_property='value')]
)
def update_races(year, race_count):
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

if __name__ == '__main__':
    app.run_server(debug=True)
