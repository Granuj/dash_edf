# Import librairies
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Import data
df = pd.read_csv("edf_cleaned.csv")
df_g = df.groupby(by="libelle_grand_secteur", as_index=False).sum()
df_pca = df[["conso", "pdl", "indqual"]]

# Initialisation de "app"
app = Dash(__name__)

# Création des contenus des onglets
tab_1_Table = html.Div(className="six columns", children=[
    dash_table.DataTable(data=df.to_dict("records"), page_size=10, style_table={"overflowX": "auto"})
])

tab_2_scatter = html.Div(dcc.Graph(figure=px.scatter(
    x=df["conso"], y=df["indqual"], labels={"x": "conso", "y": "indqual"}
)))

tab_3_scatter_3d = html.Div(dcc.Graph(figure=px.scatter_3d(
    x=df["conso"], y=df["indqual"], z=df["pdl"], labels={"x": "conso", "y": "indqual", "z": "pdl"}
)))

tab_4_interact_1 = (
    dcc.Dropdown(options=["conso", "pdl", "indqual"], value="conso", id="input_Dropdown_bar"),
    # dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dcc.Graph(figure={}, id="receiver_Dropdown_bar"),
    dcc.Graph(figure={}, id="receiver_Dropdown_pie"))

# Layout / corps principal
app.layout = html.Div([

    # Titrage Dash
    html.Div(className="row", children="Information sur la distribution de l'électricité en France",
             style={"textAlign": "center", "color": "white", "fontSize": 35, "backgroundColor": "rgb(0,128,255)"}),
    html.Br(),

    # Titrage Analyse descriptive
    html.Div(children="Analyse descriptive", style={"textAlign": "center", "fontSize": 20}),
    html.Br(),

    # Onglet analyse descriptive data
    dcc.Tabs(id="tabs", value="onglets", children=[
        dcc.Tab(label='Data_Table', value='tab1', children=tab_1_Table),
        dcc.Tab(label='Scatter_plot', value='tab2', children=tab_2_scatter),
        dcc.Tab(label='Scatter 3d', value='tab3', children=tab_3_scatter_3d),
        dcc.Tab(label='Input - Output', value='tab4', children=tab_4_interact_1)
    ]),
    html.Hr(style={"width": 500, "border-color": "red", }),
    html.Br(),

    # Titrage analyse exploratoire
    html.Div(children="Analyse exploratoire", style={"textAlign": "center"}),
    html.Br(),

    # Onglet analyse exploratoire data
    dcc.Tabs(id="tabs_2", value="onglets_2", children=[
        dcc.Tab(label='Data_Table', value='tab1', children=tab_1_Table)
    ])
])


# @callback et génération des graphiques par callback
# Callback pour le bar plot
@callback(
    Output(component_id="receiver_Dropdown_bar", component_property="figure"),
    Input(component_id="input_Dropdown_bar", component_property="value")
)
def update_figure(col_chosen):
    fig = px.histogram(df, x="libelle_region", y=col_chosen, histfunc="sum")
    return fig


# Callback pour le Pie chart
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
