# Importation bibliothèques
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Importation data
df = pd.read_csv('edf_cleaned.csv')
dfg = df.groupby(by="libelle_grand_secteur", as_index=False).sum()
for_pca = df[["conso", "pdl", "indqual"]]

# Initialisation de "app"
app = Dash(__name__)

# Corps principal / Layout html de "app"
app.layout = html.Div([  # Élément Div contenant tous les autres éléments de Layout

    # Titrage
    html.Div(className="row", children="Information sur la distribution de l'électricité en France",
             # style={"textAlign": "center", "color": "white", "fontSize": 35, "backgroundColor": "lightblue"}),
             style={"textAlign": "center", "color": "white", "fontSize": 35, "backgroundColor": "rgb(0,128,255)"}),

    # Bar de séparation
    html.Hr(style={"width": 500, "border-color": "red", }),
    # Titrage
    html.Br(),  # Saut à la ligne (linebreak)
    html.Div(children="DataFrame nettoyé", style={"textAlign": "center"}),
    html.Div(children="(18128 individus, 15 variables)", style={"textAlign": "center"}),
    html.Br(),
    # Affichage du DataFrame
    # dash_table.DataTable(data=df.to_dict("records"), page_size=10), # sans css ?
    html.Div(className="six columns", children=[
        dash_table.DataTable(data=df.to_dict("records"), page_size=10, style_table={"overflowX": "auto"})]),

    # Bar de séparation
    html.Hr(style={"width": 500, "border-color": "red", }),
    # Titrage
    html.Br(),  # Saut à la ligne (linebreak)
    html.Div(children="Scatterplot", style={"textAlign": "center"}),
    html.Br(),
    html.Div(children="X = conso, Y = indqual Z = pdl", style={"textAlign": "center"}),
    html.Div(dcc.Graph(figure=px.scatter(x=df["conso"], y=df["indqual"], labels={"x": "conso", "y": "indqual"}))),
    html.Div(dcc.Graph(figure=px.scatter_3d(
        x=df["conso"], y=df["indqual"], z=df["pdl"], labels={"x": "conso", "y": "indqual", "z": "pdl"}))),

    # Bar de séparation
    # html.Div(html.Hr(style={"width": 500, "border-color": "lightblue", })), # peut être mis dans un .div
    html.Hr(style={"width": 500, "border-color": "red", }),
    # Titrage
    html.Br(),
    html.Div(children="Répartition par région", style={"textAlign": "center"}),
    html.Br(),
    # Commande dropdown_bar
    dcc.Dropdown(options=["conso", "pdl", "indqual"], value="conso", id="input_Dropdown_bar"),
    dcc.Graph(figure={}, id="receiver_Dropdown_bar"),
    # Commande dropdown_bar
    # dcc.RadioItems(options=["conso", "pdl", "indqual"], value="conso", inline=True, id="input_RadioItems_pie"),
    dcc.Graph(figure={}, id="receiver_Dropdown_pie"),

    # Bar de séparation
    html.Hr(style={"width": 500, "border-color": "red", }),
    # Titrage
    html.Br(),  # Saut à la ligne (linebreak)
    html.Div(children="PCA", style={"textAlign": "center"}),
    html.Br(),

])


# callback de drop_Down
@callback(
    Output(component_id="receiver_Dropdown_bar", component_property="figure"),
    Input(component_id="input_Dropdown_bar", component_property="value")
)
def update_figure(col_chosen):
    fig = px.histogram(df, x="libelle_region", y=col_chosen, histfunc="sum")
    return fig


@callback(
    Output(component_id="receiver_Dropdown_pie", component_property="figure"),
    Input(component_id="input_Dropdown_bar", component_property="value")
)
def update_figure(col_chosen):
    fig = px.pie(df, values=col_chosen, names="libelle_region", hole=0.1)
    return fig


# Lancement de "app"
if __name__ == "__main__":
    app.run(debug=True)
