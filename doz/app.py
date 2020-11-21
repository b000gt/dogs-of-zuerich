from .server import app
from . import race, years, age
import dash_html_components as html


app.layout = html.Div(children=[    
    html.H1('Dogs of Zuerich'),
    html.Div(className='col-md-12', children=[
        html.Div(className='row', children=[years.title, age.title]),
        html.Div(className='row', children=[years.input, age.input]),
        html.Div(className='row', children=[years.output, age.output]),

        html.Div(className='row', children=[race.title]),
        html.Div(className='row', children=[race.input]),
        html.Div(className='row', children=[race.output])

    ])
])
