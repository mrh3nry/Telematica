# -*- coding: utf-8 -*-
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

# Cores pra deixa mais bonito :)
color = dict(color=[
    'hsla(0, 70%, 70%, 1)',
    'hsla(30, 70%, 70%, 1)',
    'hsla(60, 70%, 70%, 1)',
    'hsla(90, 70%, 70%, 1)',
    'hsla(120, 70%, 70%, 1)',
    'hsla(150, 70%, 70%, 1)',
    'hsla(180, 70%, 70%, 1)',
    'hsla(210, 70%, 70%, 1)',
    'hsla(240, 70%, 70%, 1)',
    'hsla(270, 70%, 70%, 1)'])

# Tabalas
etaria = pd.read_csv('../csv/Faixa-etaria.csv').transpose()
xadrez = pd.read_csv('../csv/O-xadrez-do-carcere.csv').transpose()
causa = pd.read_csv('../csv/A-causa-da-exclusao.csv')
grau = pd.read_csv('../csv/Grau-de-Instrucao.csv').transpose()


##########
# Opções #
##########
uf = []
for u in etaria.columns.tolist():
    uf.append({'label': u, 'value': u})

op_causa = []
for c in causa.columns.tolist():
    op_causa.append({'label': c, 'value': c})

years = [y for y in xadrez.columns.tolist()]

plots = [
    {'label': 'Pie', 'value': 'Pie'},
    {'label': 'Line', 'value': 'Line'}
]
############
# graficos #
############

styler_div = {
    'margin': 30,
    'padding': 50,
    'width': '80%',
    'height': '50%',
    'justify-content': 'center',
    'box-shadow': '0px 5px 15px #aaaaaa'
}

causa_exclusao = html.Div([
    html.H2('Causa da exclusão'),

    dcc.Dropdown(
        id='dropdown-causa',
        options=op_causa,
        value='Total'
    ),

    dcc.Graph(id='graph-causa')
], style=styler_div, className='card')

faixa_etaria = html.Div([
    html.H2('Faixa etária'),

    html.Label('Estado'),

    dcc.Dropdown(
        id='dropdown-faixa',
        options=uf,
        value='Acre'
    ),

    dcc.Graph(id='graph-faixa')
], style=styler_div, className='card')

grau_instituicao = html.Div([
    html.H2('Grau de instituição'),

    dcc.Dropdown(
        id='dropdown-grau',
        options=uf,
        value='Acre'
    ),

    dcc.Graph(id='graph-grau')
], style=styler_div, className='card')

xadrez_carcere = html.Div([
    html.H2('O xadrez do cárcere'),

    dcc.Dropdown(
        id='dropdown-xadrez',
        options=plots,
        value='Pie'
    ),

    dcc.Graph(id='graph-xadrez'),

    dcc.Slider(
        id='slider-xadrez',
        min=years[0],
        max=years[-1],
        value=years[0],
        marks={y: str(y) for y in years}
    )
], style=styler_div, className='card')


########
# Dash #
########
external_stylesheets = [
    'https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    xadrez_carcere,
    causa_exclusao,
    faixa_etaria,
    grau_instituicao
], style={
    'padding-top': 40,
    'background-color': '#ebebeb',
    'justify-content': 'center',
    'align-items': 'center',
    'display': 'flex',
    'flex-wrap': 'wrap'
})


############################
# Atualização dos graficos #
############################
@app.callback(
    Output(component_id='graph-xadrez', component_property='figure'),
    [Input(component_id='dropdown-xadrez', component_property='value'),
     Input(component_id='slider-xadrez', component_property='value')])
def update_graph(value, slide):
    if value == 'Pie':
        data = [go.Pie(
            values=xadrez[slide].tolist(),
            labels=xadrez.index.tolist()
        )]
    elif value == 'Line':
        xa = xadrez.transpose()
        data = [
            go.Scatter(
                x=xa.index,
                y=xa['Presos'],
                name='Presos'),
            go.Scatter(
                x=xa.index,
                y=xa['Vagas'],
                name='Vagas'),
            go.Scatter(
                x=xa.index,
                y=xa['Déficite'],
                name='Déficite')
        ]

    return go.Figure(data=data)


@app.callback(
    Output(component_id='graph-faixa', component_property='figure'),
    [Input(component_id='dropdown-faixa', component_property='value')])
def update_faixa(value):
    data = [go.Bar(
        y=etaria[value].tolist(),
        x=etaria.index.tolist(),
        marker=color)]

    return go.Figure(data=data)


@app.callback(
    Output(component_id='graph-causa', component_property='figure'),
    [Input(component_id='dropdown-causa', component_property='value')])
def update_causa(value):
    data = [go.Bar(
        y=causa[value].tolist(),
        x=causa.index.tolist(),
        marker=color)]

    return go.Figure(data=data)


@app.callback(
    Output(component_id='graph-grau', component_property='figure'),
    [Input(component_id='dropdown-grau', component_property='value')])
def update_grau(value):
    data = [go.Bar(
        y=grau[value].tolist(),
        x=grau.index.tolist(),
        marker=color)]

    return go.Figure(data=data)


if __name__ == '__main__':
    app.run_server(debug=True)
