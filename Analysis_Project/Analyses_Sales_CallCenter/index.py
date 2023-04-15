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

tab_card = {'height': '100%'}

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

base = pd.read_csv('D:\Documentos-Victor\GitHub\Machine_Learning\Analysis_Project\Analyses_Sales_CallCenter\dataset.csv')
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
base['Dia'] = base['Dia'].astype(int)

base['Chamadas Realizadas']=base['Chamadas Realizadas'].astype(int)

base.loc[base['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
base.loc[base['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0 
base['Status de Pagamento'] = base['Status de Pagamento'].astype(int)

base['Valor Pago'] = base['Valor Pago'].str.lstrip('R$ ')
base['Valor Pago'] = base['Valor Pago'].astype(int)


# Criando opções para os filtros:
options_month = [{'label':'Ano todo', 'value':0}]
for i, j in zip(base_cru['Mês'].unique(), base['Mês'].unique()):
    options_month.append({'label':i, 'value':j})
options_month=sorted(options_month, key=lambda x: x['value'])

options_team = [{'label':'Todos Equipes', 'value':0}]
for i in base['Equipe'].unique():
    options_team.append({'label':i, 'value':i})

def month_filter(month):
    if month == 0:
        mask = df['Mês'].isin(df['Mês'].unique())
    else:
        mask = df['Mês'].isin([month])
    return mask

def team_filter(team):
    if team == 0:
        mask = df['Equipe'].isin(df['Equipe'].unique())
    else:
        mask = df['Equipe'].isin([team])
    return mask

def convert_to_text(month):
    match month:
        case 0:
            x = 'Ano Todo'
        case 1:
            x = 'Janeiro'
        case 2:
            x = 'Fevereiro'
        case 3:
            x = 'Março'
        case 4:
            x = 'Abril'
        case 5:
            x = 'Maio'
        case 6:
            x = 'Junho'
        case 7:
            x = 'Julho'
        case 8:
            x = 'Agosto'
        case 9:
            x = 'Setembro'
        case 10:
            x = 'Outubro'
        case 11:
            x = 'Novembro'
        case 12:
            x = 'Dezembro'
    return x

# ======= Layout ====== #
app.layout = dbc.Container(children=[
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([  
                            html.Legend("Sales Analytics")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Asimov Academy")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://asimov.academy/", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Top Consultores por Equipe')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dcc.Graph(id='graph7', className='dbc', config=config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph8', className='dbc', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    # Row 3:
    dbc.Row([
        dbc.Col([
          dbc.Card([
            dbc.CardBody([
                html.H4('Distribuição de Propaganda'),
                dcc.Graph(id='graph9', className='dbc', config=config_graph)
            ]),
          ], style=tab_card), 
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Valores de Propaganda Convertidos Por Mês'),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ]),
            ], style=tab_card),
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                        dcc.Graph(id='graph11', className='dbc', config=config_graph)
                ]),
            ], style=tab_card),
        ], sm=12, lg=5),
        dbc.Col([
            html.H5('Escolha a Equipe'),
            dbc.RadioItems(
                id='radio-team',
                options=options_team,
                value=0,
                inline=True,
                labelCheckedClassName="text-warning",
                inputCheckedClassName="border border-warning bg-warning",
            ),
            html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
        ], sm=12, lg=3)
    ])

], fluid=True, style={'heigth':'100vh'})

# ======= CallBack ====== #

app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Output('graph3', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)

def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_1 = df.loc[mask]

    df_1 = df_1.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum()
    df_1 = df_1.sort_values(ascending=False)
    df_1 = df_1.groupby('Equipe').head(1).reset_index()

    fig2 = go.Figure(go.Pie(labels=df_1['Consultor'] + ' - ' + df_1['Equipe'], values=df_1['Valor Pago'], hole=.6))
    fig1 = go.Figure(go.Bar(x=df_1['Consultor'], y=df_1['Valor Pago'], textposition='auto', text=df_1['Valor Pago']))
    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template, showlegend=False)

    select = html.H1(convert_to_text(month))

    return fig1, fig2, select

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
