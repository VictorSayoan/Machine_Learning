from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from dash_bootstrap_templates import ThemeSwitchAIO # Alterar o tema de fundo do dash (Branco ou Preto)
import dash

FONT_AWESOME=["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app=dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server


# ======= Styles ====== #

tab_card = {'heigth' : '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBr":False, "ShowTips":False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# ======= Layout ====== #
app.layout = dbc.Container(children=[], fluid=True, style={'height':'100vh'})


# Run server
if __name__ == 'main':
    app.run_server(debug=True, port=8051)
