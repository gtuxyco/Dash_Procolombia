import dash_bootstrap_components as dbc
from dash import dcc
from dash import html,  callback
from dash.dependencies import Input, Output, State
from components import summary
import plotly.express as px
from assets import style
from logica import controlador
import time
from dash import dash_table
from datetime import datetime as dt
from datetime import date



dropdowns = dbc.Col([

    dbc.Col([
        html.P(html.B("Seleccione una región: ")),  
    ]),
    
    dbc.Col([
        dcc.Dropdown(
                id="dropdown_region_region",
                options = [{'label': t, 'value': t} for t in controlador.getRegions()],
                value = controlador.getRegions()[0],
                clearable=False,  
            ),
    ],lg=10, md=12),
    html.Br(),
    html.Br(),
    dbc.Col([
        html.P(html.B("Elija cantidad de rezagos: ")),  
    ]),
    html.Br(),
    dbc.Col([
        dcc.Slider(0, 20, 1,
               value=5,
               id='slider_region'
    )
    ]
    )
    
    
    
] ,className="dropdowns")


content = html.Div(
    [
        html.Hr(),
        dropdowns,
        html.H2('Actividades de Promoción Turística: Nivel de Influencia por país', style={"text-align":"center"}, id = "lblInfluence_region"),
        
        dcc.Loading(
                    id="ls-loading-2_region",
                    children=[
                dbc.Row([
                    dbc.Col([
            
                        #summary.details_table
                ],lg=5, md=12, id="influence_table_region", style={'margin-left' : "15px"}),
                dbc.Col([

                ],lg=5, md=12, id="influence_table2_region", style={'margin-left' : "15px"})
                ]),
                dbc.Row([
                    
                ],id="bestmodel_region", style={'align' : "center"})
                
                ],
                    type="circle",
                ),

        
        
        html.Hr(),
        html.H2('Resumen General por país', style={"text-align":"center"}, id="lblGeneralSummary_region"),
          
        html.Div([


    dbc.Row([
        dbc.Col([dcc.Graph(id="graph_hub_region")], lg=9, md=12 ),
        dbc.Col([
            dbc.Row(html.P(html.B("Seleccione las actividades de promoción: "))),
       
            dcc.Dropdown(
                options=controlador.actividades,
                value=controlador.actividades[0]["label"],
                #options=controlador.getActividades(),
                #value=controlador.getActividades(),
                clearable=False,
                id="dropdown_promotion_activity_region",
                multi=True
            ),
        dbc.Row ( html.P(html.B("Seleccione rango inicial - final: "))),
        dbc.Row([
            dbc.Col([
                dcc.DatePickerRange(
                id = "datapicker_region",
                start_date = date(2012, 1, 1), 
                end_date=date(2022, 6, 1),
                min_date_allowed="2012-01",
                display_format='YYYY-MM',
                start_date_placeholder_text='YYYY-MM'
            )], style={"width":"30px" ,"height":"","font-size":"10px"}),       
            
            
        ]),
        ], lg=3, md=12)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id="graph_pasajeros_pais_region")]),
        dbc.Col([ dcc.Graph(id="graph_barplot_region")])
    ]),
    html.Div([
        '''
        dbc.Col([
            dcc.Graph(id="graph_heatmaps")
        ],lg=12, md=12)
        '''
        
    ], id = "heatmaps_container")
]),

            html.H2('Predicción de visitantes por País ', style={"text-align":"center"}, id = "lblVisitors_region"),
        html.Hr(),
        dbc.Row([
        
        dbc.Col([

            dcc.Loading(
                    id="ls-loading-2",
                    children=[
                        dcc.Graph(id="graph_visitors_region")
                        ],
                    type="circle",
                ),
            #dcc.Dropdown(['Enero', 'Febrero', 'Marzo'],id="dropdown-inner")
        ], lg =8, md = 12),
        ]
            
        ),
        
        
        
       
    ],
    className="contentDiv"
    #style=style.CONTENT_STYLE
)



@callback(
    Output("graph_visitors_region", "figure"), 
    Input("dropdown_region_region", "value"),
    Input('datapicker_region', 'start_date'),
    Input('datapicker_region', 'end_date'),
    )

def displayvisitors(hub, inicio, fin):
    #print("Displaying prophet")
    start_date = dt.strptime(inicio, '%Y-%m-%d')
    end_date = dt.strptime(fin, '%Y-%m-%d')
    fig = controlador.heatmap_visitors(hub, start_date,end_date)

    return fig

@callback(
    Output("graph_hub_region", "figure"),
    Output("graph_pasajeros_pais_region", "figure"),
    Output("graph_barplot_region", "figure"),
    #Output("graph_heatmaps", "figure"),
    Input ('dropdown_region_region', 'value'),
    Input('dropdown_promotion_activity_region', "value"),
    Input('datapicker_region', 'start_date'),
    Input('datapicker_region', 'end_date')
)
def generateGeneralGraphs(region, actividades,inicio,fin):
    #start_date = dt(2012, 1, 1)
    #end_date = dt(2020, 12, 1)
    start_date = dt.strptime(inicio, '%Y-%m-%d')
    end_date = dt.strptime(fin, '%Y-%m-%d')
    paises_region = controlador.getCountriesByRegion(region)
    return controlador.display_map_single_country(start_date,end_date, region), controlador.display_time_series(None,paises_region, start_date,end_date), controlador.display_barplot(paises_region,actividades, start_date,end_date) #, controlador.display_heatmap_hub(paises_region,actividades)





@callback(
    Output("influence_table_region", "children"),
    Output("influence_table2_region", "children"),
    #Output("bestmodel_region", "children"),
    Input("dropdown_region_region", "value"),
    Input("slider_region", "value"),
)
def display_influence_table(hub,rezagos):
    table, table_activities= controlador.tabla_influencia_variable(hub, rezagos) 
    return dash_table.DataTable(table.to_dict('records'), [{"name": i, "id": i} for i in table.columns]), dash_table.DataTable(table_activities.to_dict('records'), [{"name": i, "id": i} for i in table_activities.columns])

@callback(
    Output("heatmaps_container", "children"),
    Input("dropdown_promotion_activity_region", "value"),
    Input("dropdown_region_region", "value"),
    Input('datapicker_region', 'start_date'),
    Input('datapicker_region', 'end_date')
)
def generateHeatmaps(activities, region, inicio, fin):
    
    start_date = dt.strptime(inicio, '%Y-%m-%d')
    end_date = dt.strptime(fin, '%Y-%m-%d')
    rows=[]
    for act in activities:
        if len(activities) != 0:
            rows.append(
            dbc.Row([
                dbc.Col([
                    dcc.Graph(
                        figure = controlador.display_heatmap_hub(controlador.getCountriesByRegion(region),act, start_date, end_date),
                    )
                ],lg=12, md=12)
            ])
        )
        
    return rows


@callback(
    Output("lblGeneralSummary_region", "children"),
    Output("lblVisitors_region", "children"),
    Output("lblInfluence_region", "children"),
    Input("dropdown_region_region", "value")
)
def reloadTitles(region):
    return "Resumen General "+ "("+ region+")",  "Predicción de visitantes (" + region+")",  "Actividades de Promoción Turística: Nivel de Influencia en (" + region+")"