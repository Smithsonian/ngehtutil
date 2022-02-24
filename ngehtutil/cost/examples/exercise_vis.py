import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

data = pd.read_excel('exercise_out.xlsx', index_col=0)
data.loc['eht_sites'] = data.loc['eht_sites'].apply(lambda x: str(len(eval(x))))
data.loc['ngeht_sites'] = data.loc['ngeht_sites'].apply(lambda x: str(len(eval(x))))
data.loc['TOTAL CAPEX'] = data.loc['TOTAL CAPEX'].apply(lambda x: x/1e6)
data.loc['ANNUAL OPEX'] = data.loc['ANNUAL OPEX'].apply(lambda x: x/1e6)

app = dash.Dash(__name__)

inputs = []
factors = ['ngeht_sites', 'eht_sites', 'recording_frequencies', 'recording_bandwidth', 'dish_size', 'campaigns_per_year'] 

selectors = []
for i in factors:
    options = []
    for j in data.loc[i].unique():
        option = {'label':j, 'value': j}
        options.append(option)
    selector = html.Div([
        html.Label(i),
        dcc.Dropdown(
            id=f'{i}-dropdown',
            options=options,
        )],
        style={"width": "30%"}
    )
    selectors.append(selector)
    input = Input(f'{i}-dropdown', "value")
    inputs.append(input)


app.layout = html.Div(children=[
    html.H1(children='ngEHT Cost Estimating'),
    html.Div(children=selectors),
    # *selectors,
    dcc.Graph(
        id='example-graph'
    ),
])


@app.callback(
inputs=inputs,
output=Output('example-graph','figure')
)
def update_output(*args):
    x = data.copy()
    xmax = x.loc['TOTAL CAPEX'].max()+50
    ymax = x.loc['ANNUAL OPEX'].max()+1

    for i,f in enumerate(factors):
        if args[i]:
            x = x.loc[:,x.loc[f]==args[i]]

    fig = px.scatter(x.transpose(), x='TOTAL CAPEX', y='ANNUAL OPEX', \
        hover_data=factors,
        labels={
            'TOTAL CAPEX': 'Total Capex ($MM)',
            'ANNUAL OPEX': 'Annual Opex ($MM)',
        },
        title=f'Capex vs. Opex for {len(x.columns)} Configurations'
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(range=[0, xmax])
    fig.update_yaxes(range=[0, ymax])

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
