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

# ==== Reading and cleaning File ==== #

base = pd.read_csv('dataset.csv')
base_cru = base.copy()

base.loc[base['Mês'] == 'Jan', 'Mês'] = 1
base.loc[base['Mês'] == 'Fev', 'Mês'] = 2
base.loc[base['Mês'] == 'Mar', 'Mês'] = 3
base.loc[base['Mês'] == 'Abr', 'Mês'] = 4
base.loc[base['Mês'] == 'Mai', 'Mês'] = 5
base.loc[base['Mês'] == 'Jun', 'Mês'] = 6
base.loc[base['Mês'] == 'Jul', 'Mês'] = 7
base.loc[base['Mês'] == 'Ago', 'Mês'] = 8
base.loc[base['Mês'] == 'Set', 'Mês'] = 9
base.loc[base['Mês'] == 'Out', 'Mês'] = 10
base.loc[base['Mês'] == 'Nov', 'Mês'] = 11
base.loc[base['Mês'] == 'Dez', 'Mês'] = 12

base['Mês'] = base['Mês'].astype(int)

base['Chamadas Realizadas']=base['Chamadas Realizadas'].astype(int)

base.loc[base['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
base.loc[base['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0 
base['Status de Pagamento'] = base['Status de Pagamento'].astype(int)

base['Valor Pago'] = base['Valor Pago'].str.lstrip('R$ ')
base['Valor Pago'] = base['Valor Pago'].astype(int)


# ======= Layout ====== #
app.layout = dbc.Container(children=[], fluid=True, style={'height':'100vh'})

# Row 1:
dbc.Row([
    dbc.Col([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Legend("Sales Analytics")
                    ], sm=8),
                    dbc.Col([
                        html.I(className='fa fa-balance-scele', style={'font-size':'300%'})
                    ], sm=4, align="center"),
                ]),
                dbc.Row([
                    dbc.Col([
                        ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                        html.Legend("Data Analises")
                        ])
                        ], style={'margin-top':'10px'}),
                dbc.Row([
                    dbc.Button("Visite o meu GIT", href="https://github.com/VictorSayoan", target="")
                ], style={'margin-top':'10px'}),
                ]),
            ]),
        ]),
    ]),


# Run server
if __name__ == 'main':
    app.run_server(debug=True, port=8051)
