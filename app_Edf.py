# Importation bibliothèques et données
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('edf_cleaned.csv')
# df_g = df.groupby(by="libelle_region", as_index=False).sum()
# df = df.drop("")

# Initialisation de "app" ?
app = Dash(__name__)

# Layout / corps de "app"
app.layout = html.Div([
    html.Div(children='Premier élément du app.layout / html.Div'),

    html.Hr(),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),
    #dash_table.DataTable(data=df_g.to_dict('records'), page_size=10),

    html.Hr(),  # "records" arguments ? affiche un df
    dcc.Graph(figure=px.histogram(df, x='libelle_region', y='conso', histfunc='sum')),
    dcc.Graph(figure=px.histogram(df, x="libelle_grand_secteur", y='conso', histfunc='sum')),

    # Radio
    # options_radio
    html.Hr(style={'width': '5'}),
    dcc.RadioItems(options=["conso", "pdl", "indqual"], value="conso", id='controls-and-radio-item'),
    dcc.Graph(figure={}, id='controls-and-graph')

])


# Contrôle de Radio
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='libelle_region', y=col_chosen, histfunc='sum')
    return fig


# permet de lancer / run "app"
if __name__ == '__main__':
    app.run(debug=True)
