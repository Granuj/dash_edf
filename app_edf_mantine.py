# Importation bibliothèques et données
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
# import dash_design_kit as ddk
import dash_mantine_components as dmc

# Importation data
df = pd.read_csv('edf_cleaned.csv')

# Initialisation de l'app + Mantine
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Corps de app.layout

app.layout = dmc.Container([
    dmc.Title("Infos sur les distributeurs et leurs points de livraisons", color="darkblue", size="h3",
              style={'textAlign': 'center', 'color': 'darkblue', 'fontSize': 35, 'font-family': 'Arial, sans-serif',
                     'font-variant': 'small-caps',
                     'backgroundColor': 'lightgrey'}),

    dmc.RadioGroup([dmc.Radio(i, value=i) for i in ["conso", "pdl", "indqual"]], id='dmc_radio_id', value='conso',
                   size="sm"),
    dmc.Grid([
        dmc.Col([
            dash_table.DataTable(data=df.to_dict('records'), page_size=12, style_table={'overflowX': 'auto'}),
            dmc.Col([dcc.Graph(figure={}, id='graph-placeholder')], span=6)])
    ])
], fluid=True)


@callback(
    Output(component_id='graph-placeholder', component_property='figure'),
    Input(component_id='dmc_radio_id', component_property='value')

)
def update_graph_bar(col_chosen):
    fig = px.histogram(df, x='libelle_region', y=col_chosen, histfunc='sum')
    return fig


# lance app
if __name__ == "__main__":
    app.run(debug=True)
