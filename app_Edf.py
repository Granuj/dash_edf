# Importation bibliothèques et données
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('edf_cleaned.csv')
df_g = df.groupby(by="libelle_grand_secteur", as_index=False).sum()
# df = df.drop("")

# Initialisation de "app" ?
app = Dash(__name__)

# Layout / corps de "app"
app.layout = html.Div([
    html.Div(className='row', children='Infos sur les distributeurs et leurs points de livraisons',
             style={'textAlign': 'center', 'color': 'darkblue', 'fontSize': 30, 'backgroundColor': 'lightblue'}),
    # classname utilité ?

    html.Hr(style={'width': '50', "color": "darkblue"}),
    html.Div(children="Table de base"),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10),  # "records" arguments ? affiche un df
    # dash_table.DataTable(data=df_g.to_dict('records'), page_size=10),

    # Bar plot
    html.Hr(),
    html.Div(children="BarPlot"),
    dcc.Graph(figure=px.histogram(df, x='libelle_region', y='conso', histfunc='sum')),
    dcc.Graph(figure=px.histogram(df_g, x="libelle_grand_secteur", y='conso', histfunc='sum')),

    # Pie chart
    html.Hr(),
    html.Div(children="PieChart"),
    dcc.Graph(figure=px.pie(df, values="conso", names="libelle_grand_secteur", hole=0.1)),

    # Interactif
    html.Hr(style={'width': '5'}),
    html.Div(children="Radio & @callback"),
    # Radio Bar plot
    # options_radio
    dcc.RadioItems(options=["conso", "pdl", "indqual"], value="conso",inline=True, id='radio_for_bar'),
    dcc.Graph(figure={}, id='receiver_bar'),

    # Radio Pie Chart
    html.Hr(style={'width': '50', "color": "darkblue"}),
    dcc.RadioItems(options=["conso", "pdl", "indqual"], value="conso",id="radio_for_pie"),
    dcc.Graph(figure={}, id='receiver_pie'),

    # Essai css multiple
    html.Hr(style={'width': '50', "color": "darkblue"}),
    html.Div(children="Essai css multiple"),

    html.Div(className="row", children=[
        html.Div(className="six columns", children=[dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={'overflowX': 'auto'}),]),
        html.Div(className="six columns", children=[dcc.Graph(figure=px.pie(df, values="conso", names="libelle_grand_secteur", hole=0.1))])
    ])
])


# Callback de Radio_bar
@callback(
    # Output apparaissant dans component_id de figure
    Output(component_id='receiver_bar', component_property='figure'),
    Input(component_id='radio_for_bar', component_property='value')
)
def update_graph_bar(col_chosen):
    fig = px.histogram(df, x='libelle_region', y=col_chosen, histfunc='sum')
    return fig


# Callback de radio_pie
@callback(
    Output(component_id="receiver_pie", component_property='figure'),
    Input(component_id="radio_for_pie", component_property='value')
)
def update_graph_pie(col_chosen):
    fig = px.pie(df, values=col_chosen, names="libelle_region", hole=0.1)
    return fig


# permet de lancer / run "app"
if __name__ == '__main__':
    app.run(debug=True)
