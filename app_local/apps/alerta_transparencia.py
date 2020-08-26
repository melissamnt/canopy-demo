import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from app import app
from data import df_transparency

# Table parameters ------------
PAGE_SIZE = 10
PAGE_SIZE_CONTRATISTAS = 3

# Dash components ---------

# Table
steps_header = [html.Thead(
    html.Tr(
            html.Div(
            'Pasos para filtrar', 
            className='font-weight-bold text-steps font-medium py-2',
        ),
    ),
)]

row1 = html.Tr([html.P("1. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row2 = html.Tr([html.P("2. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row3 = html.Tr([html.P("3. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])
row4 = html.Tr([html.P("4. And an even wittier subheading to boot.", className='m-3 lead font-weight-normal text-dark font-home-m')])

steps_body = [html.Tbody([row1, row2, row3, row4])]


steps_table = html.Table(steps_header + steps_body)

# Filters table
filter_depto = dcc.Dropdown(
    options=[{'label': i, 'value': i} for i in df_transparency.Departamento.drop_duplicates()],
    value=None,
    id='filter-depto',
)  




# Section layout --------------------

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    'Alerta: Transparencia activa', 
                                                    className='display-4 font-weight-bold text-home-title font-medium pb-4',
                                                ),
                                                html.Div(
                                                    [
                                                        html.P(
                                                            """
                                                            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor 
                                                            incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud 
                                                            exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure 
                                                            dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
                                                            """, 
                                                            className='lead font-weight-normal text-dark font-home-m'
                                                        ),
                                                    ],
                                                    className='mb-5',
                                                ),
                                                
                                            ], 
                                            className='justify-content-center mx-5 mt-5 pt-5 pb-2 paragraph-alerta',
                                        ),
                                    ],
                                    className='col',
                                ),
                                html.Div(
                                    [
                                        steps_table
                                    ], 
                                    className='col-4 justify-content-center mx-5 px-5 pt-5 pb-2',
                                ),
                            ],
                            className='row pb-5 pt-5 div-for-alerta',
                        ),
                        html.Div(
                            [
                                html.A(
                                    'VER ALERTA', 
                                    className='btn btn-outline-secondary p-3 text-dark font-home-m btn-ver-alerta', 
                                    href="#tabla-container",
                                ),
                            ],
                            className='row mx-auto justify-content-center mt-5',
                        ),
                    ],
                    className='mx-auto mb-5 mt-1',
                ),
            ],
        ),
        html.Div (
            [
                html.Div(
                    [
                        dbc.Card(
                            [
                                html.Div (
                                    [
                                        html.Div(
                                            "Alerta Temprana - Transparencia Activa",
                                            className= 'col align-items-center text-header-table',
                                            style={'display': 'flex'},
                                        ),
                                        html.Div(
                                            [
                                                html.Div('Filtrar por departamento', className='text-header-table pb-2'),
                                                filter_depto
                                            ],
                                            className='col pr-5'
                                        ),
                                    ],
                                    className='row p-5'
                                ),                                
                                html.Div (
                                    [
                                        html.Div(
                                            id='table-transparency',
                                            className='table my-0 div-for-table-alertas'
                                        ),
                                    ],
                                    className='row mx-0',
                                ),
                                html.Div (
                                    [
                                        html.Div(
                                            id='count_entries',
                                            className='col my-auto',
                                        ),
                                        html.Div(
                                            className='col my-auto buttons-footer-table',
                                            children=[
                                                    dbc.Button("Anterior", id='previous-page', n_clicks=0, className='buttons-footer'), 
                                                    dbc.Button("Siguiente", id='next-page', n_clicks=0, className='buttons-footer'),
                                            ],
                                        ),
                                    ],
                                    className='row mai-datatable-footer'
                                ),
                            ],
                            className='border-0',
                        ),
                    ],
                    className='container',
                ),
            ],
            className='main-content-table',
            id="tabla-container",
        ),
    ]
)

MIN_VAL = 0
MAX_VAL = 10
NUM_ENTRIES = 10

# create callback for modifying page layout
@app.callback(
    [Output("table-transparency", "children"),
    Output("count_entries", "children"),
    Output("previous-page", "disabled"),
    Output("next-page", "disabled")], 
    [Input('previous-page', 'n_clicks'),
    Input('next-page', 'n_clicks'),
    Input('filter-depto', 'value')])
def update_table(btn_prev, btn_next, depto_filter):

    print(depto_filter)
    print('------')
    if depto_filter != None:
        df_transparency_subset = df_transparency[df_transparency['Departamento']==depto_filter]
    
    else:
        df_transparency_subset = df_transparency.copy()

    global MIN_VAL
    global MAX_VAL
    global NUM_ENTRIES
    LEN_DF_COMPLETE = len(df_transparency_subset)


    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if 'previous-page' in changed_id:
        MIN_VAL = max(0, MIN_VAL-NUM_ENTRIES-1)
        MAX_VAL = min(LEN_DF_COMPLETE, MAX_VAL-NUM_ENTRIES-1)
    elif 'next-page' in changed_id:
        MIN_VAL = max(0, MIN_VAL+NUM_ENTRIES+1)
        MAX_VAL = min(LEN_DF_COMPLETE, MAX_VAL+NUM_ENTRIES+1)

    if 'dropdown-entries' == 10:
        MIN_VAL = MIN_VAL
        MAX_VAL = min(LEN_DF_COMPLETE, MAX_VAL-NUM_ENTRIES-1)

    if MIN_VAL < 1:
        disabled_prev = True
    else:
        disabled_prev = False

    if MAX_VAL == LEN_DF_COMPLETE:
        disabled_next = True
    else:
        disabled_next = False

    df_transparency_subset = df_transparency_subset.iloc[MIN_VAL:MAX_VAL,:]

    table_transparencia = html.Table(
        # Header
        [html.Thead([html.Th(col) for col in df_transparency_subset.columns]) ] +
        # Body - Here we stablish the link
        [html.Tr(
                # List comprehension
                [
                    html.Td(df_transparency_subset.iloc[i][col]) if col != 'SECOP URL' 
                    # Link to SECOP URL
                    else html.Td(
                        html.A(html.I(className="fas fa-external-link-alt", style={'color': '#238ae5'}), href=df_transparency_subset.iloc[i][col],), 
                        className='text-center',
                        ) 
                    for col in df_transparency_subset.columns
                ]
            )
        for i in range(min(len(df_transparency_subset), 20))],
        # className="table border-collapse",
        id='table-transparency',
        style={"overflowY": "scroll"}
    )

    text_entries = 'Mostrando {} a {} de {} resultados'.format(MIN_VAL+1, min(LEN_DF_COMPLETE, MAX_VAL+1), LEN_DF_COMPLETE)
    
    return table_transparencia, text_entries, disabled_prev, disabled_next