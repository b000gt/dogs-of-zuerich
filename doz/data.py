import pandas as pd
import numpy as np
import re


df = pd.read_csv('20170308hundehalter.csv')
df['dog_count'] = 1

sections = []
STADTKREIS = df['STADTKREIS'].unique()
STADTKREIS.sort()
for x in STADTKREIS:
    if not np.isnan(x):
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

ages = []
ALTER = df['ALTER'].unique()
for x in ALTER:
    if type(x) == str:
        ages.append(x)
ages.sort()