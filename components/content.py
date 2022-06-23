import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output, State
from components.summary import details_table, general_summary

import plotly.express as px
from assets import style
from logica import graficos



dropdowns = dbc.Col([

    dbc.Col([
        html.P(html.B("Select a Region: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                ['Agenda comercial de turismo', 'Agendas de Cooperación', 'Capacitaciones y presentaciones de destino', 'FAM - PRESS Trips', 'Feria internacional de Turismo', 'Macrorruedas y Encuentros Comerciales', 'Primera Visita', 'Entrega informacion valor agregado', 'Otras Acciones promocion turismo', 'Preparación y adecuación '],
                'Primera Visita',
                clearable=False,
                id="dropdown_region",
            ),
    ],lg=10, md=12),
    html.Br(),

    dbc.Col([
        html.P(html.B("Select a Country: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                options=graficos.getCountries(), 
                value = graficos.getCountries()[0],  
                clearable=False,
                id='dropdown_countryy',
            ),
    ], lg=10, md=12),
    
    
] )


content = html.Div(
    [
        
        html.H2('Visitors Predicitions (by Region)', style={"text-align":"center"}),
        html.Hr(),
        dbc.Row([
        dropdowns,
        dbc.Col([
           dcc.Graph(id="graph-inner"),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =9, md = 12),
        ]
            
        ),
        
        html.Hr(),
        html.H2('Touristic promotion activities: Level of Influence by region', style={"text-align":"center"}),
        dbc.Col([
            
            details_table
        ],lg=9, md=12),
        html.Hr(),
        html.H2('General Summary by country', style={"text-align":"center"}, id="lblGeneralSummary"),
          
        general_summary,
        
        #content_first_row,
        #content_second_row,
        #content_third_row,
        #content_fourth_row,
        
    ],
    #style=style.CONTENT_STYLE
)




