"""
Copyright (c) 2022 Center for Astrophysics | Harvard & Smithsonian

This software is licensed for use as described in the LICENSE file in
the root directory of this distribution.

Plots a map with antenna locations shown.

Requires the plotly library ('pip install plotly')

Originator: Aaron Oppenheimer March 2020
"""

import plotly.graph_objs as go
from ngehtutil.station import Station


eht_sites = [
    'ALMA', 
    'APEX', 
    'GLT', 
    'IRAM', 
    'JCMT', 
    'KP', 
    'LMT', 
    'NOEMA', 
    'SMA', 
    'SMT', 
    'SPT'
]

phase_1_sites = [
    'HAY', 
    'OVRO', 
    'BAJA', 
    'CNI', 
    'LAS'
]

phase_2_sites = [
    'BAN', 
    'BAR', 
    'BGA', 
    'BMAC', 
    'BOL', 
    'BRZ', 
    'CAS', 
    'CAT', 
    'FAIR', 
    'GAM', 
    'GARS', 
    'GLTS', 
    'JELM', 
    'KILI', 
    'LLA', 
    'PAR', 
    'PIKE', 
    'SAN', 
    'SGO', 
    'SKS', 
    'SPX', 
    'TRL', 
    'YAN'
]

sites=[eht_sites, phase_1_sites, phase_2_sites]
legend=['Existing EHT', 'ngEHT Phase 1', 'Poss. ngEHT Phase 2']
colors=['blue','orange', 'white']

centerlon = -100

show_names = False

fig = go.Figure()
for i,lst in enumerate(sites):
    lats = []
    lons = []
    names = []
    for s in lst:
        s=Station.from_name(s)
        lats.append(s.latitude)
        lons.append(s.longitude)
        names.append(s.name)

    fig.add_trace(
        go.Scattergeo(
            lon = lons,
            lat = lats,
            text = names if show_names else None,
            textposition="top center",
            mode = 'markers+text',
            marker = dict(
                size = 10,
                color = colors[i],
                line = dict(
                    width = 1,
                    color = 'black'
                )
            ),
            name = legend[i]
        )
    )

fig.update_geos(
    center=dict(lat=0, lon=-100), # this will center on the point
    lataxis=dict(range=[-90,90]),
    lonaxis=dict(range=[-180+centerlon,180+centerlon]),
)

fig.update_layout(legend=dict(
    yanchor="bottom",
    y=0.05,
    xanchor="left",
    x=0.01,
    borderwidth = 1,
))

fig.show()
