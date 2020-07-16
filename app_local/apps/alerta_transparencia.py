import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import numpy as np
import json


# DATAFRAMES -----------------

# 1. Dataframe SECOP I & II items
df_raw_items = pd.read_csv("https://storage.googleapis.com/secop_data/secop_join_suministros_w_sobrecosto.csv")
df_items = df_raw_items.copy()
df_items = df_items.rename(columns={
    'nombre_entidad': 'Nombre de la entidad',
    'departamento': 'Departamento',
    'ciudad': 'Municipio',
    'id_contrato': 'ID contrato',
    'descripcion_del_proceso': 'Descripcion del contrato',
    'tipo_de_contrato': 'Tipo de contrato',
    'modalidad_de_contratacion': 'Modalidad de contratacion',
    'proveedor_adjudicado': 'Proveedor adjudicado',
    'url': 'SECOP URL',
    'valor_del_contrato': 'Valor del contrato',
    'item_code': 'Código del item',
    'item_description': 'Descripción del item',
    'item_quantity': 'Cantidad del item',
    'item_price': 'Precio por item',
    'precio_piso': 'Precio minimo',
    'precio_techo': 'Precio maximo',
    'alarma_sobrecosto': 'Alerta de sobrecosto'
})

df_items = df_items[['Alerta de sobrecosto', 'Descripción del item', 'Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato', 'Código del item',
              'Cantidad del item', 'Precio por item', 'Precio minimo', 'Precio maximo',
             'Descripcion del contrato', 'ID contrato',
             'Tipo de contrato', 'Modalidad de contratacion',  'SECOP URL']]
df_items['Alerta de sobrecosto'] = np.where(df_items['Alerta de sobrecosto']==True, 'Si', 'No')
df_items['SECOP URL'] = '[Link](' + df_items['SECOP URL'] + ')'


entidades_items = df_items['Municipio'].unique()


# 2. Dataframe SECOP I & II transparency
df_raw_transparency = pd.read_csv("https://storage.googleapis.com/secop_data/secop_2_covid_singleitem.csv")
df_transparency = df_raw_transparency.copy()
df_transparency = df_transparency.rename(columns={
    'nombre_entidad': 'Nombre de la entidad',
    'departamento': 'Departamento',
    'ciudad': 'Municipio',
    'id_contrato': 'ID contrato',
    'descripcion_del_proceso': 'Descripcion del contrato',
    'tipo_de_contrato': 'Tipo de contrato',
    'modalidad_de_contratacion': 'Modalidad de contratacion',
    'proveedor_adjudicado': 'Proveedor adjudicado',
    'url': 'SECOP URL',
    'valor_del_contrato': 'Valor del contrato',
    'items_per_contract': 'Items por contrato'
})

df_transparency = df_transparency[['Nombre de la entidad', 'Departamento', 'Municipio', 'Proveedor adjudicado', 'Valor del contrato',
             'Descripcion del contrato', 'ID contrato',
             'Tipo de contrato', 'Modalidad de contratacion',  'SECOP URL']]

df_transparency['SECOP URL'] = '[Link](' + df_items['SECOP URL'] + ')'


# Table parameters ------------
PAGE_SIZE = 10
PAGE_SIZE_CONTRATISTAS = 3

# Dash components ---------

# Table
table_transparencia = dash_table.DataTable(
    id='table-editing-simple-2',
    # Data
    columns=(
        [{'id': c, 'name': c, 'type':'text', 'presentation':'markdown'} for c in df_transparency.columns]
    ),
    data=df_transparency.to_dict('records'),
    # Table interactivity
    # Table styling
    style_table={
        'overflowX': 'auto',
        'margin': '0',
        'overflowY': 'scroll',
    },
    style_data={
        'border': '0px'
    },
    # Style cell
    style_cell={
        'fontFamily': 'Open Sans',
        'fontSize': '15px',
        'height': '60px',
        'padding': '2px 22px',
        'whiteSpace': 'inherit',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'backgroundColor': 'rgb(49, 48, 47)',
        'boxShadow': '0 0',
        'whiteSpace': 'normal',
        'height': 'auto',
        'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'
    },
    # Style header
    style_header={
        'backgroundColor': 'rgb(63, 65, 63)',
        'border': '0px'
    },
    # Style filter
    style_filter={
        'fontFamily': 'Open Sans',
        'height': '40px',
        'backgroundColor': 'rgb(217, 217, 217)',
        'fontColor': 'black',
    },
    # style_data_conditional=[{
    #     'if': {
    #         'column_id': 'Alerta de sobrecosto',
    #         'filter_query': '{Alerta de sobrecosto} = "Alerta"'
    #     },
    #     'fontColor': 'black',
    #     'backgroundColor': '#ffb575',
    # }],
    page_action='native',
    page_size= PAGE_SIZE,
    persistence=True,
    sort_action='native',
    filter_action='native',
)


# Section layout --------------------

layout = html.Div(
    [
        html.Div (
            className='div-for-paragraphs text-secondary',
            children=[
                # Title
                html.Div(
                    [
                        html.H2("Alerta: Falta Transparencia Activa"),
                    ],
                    className='text-left p-5'
                ),
                html.Div(
                    [
                        html.P(
                            """
                            En esta sección podrá acceder a los datos sobre alertas en la
                            contratación destinada a atender la emergencia COVID-19 que carezcan
                            de una publicación adecuada de los ítems a contratar.
                            Esto genera falencias en la aplicación del principio de proactividad de
                            ley 1712 de 2014 conocido como el cumplimiento de la Transparencia Activa.

                            """
                        ),
                        html.P(
                            """
                            Como usuario puede realizar la búsqueda por las siguientes categorías:
                            Ítem - Nombre de la entidad que contrata – Departamento – Municipio –
                            Proveedor seleccionado – Valor del contrato – Precio por Item.


                            """
                        ),

                        html.P(
                            """
                            Para iniciar la búsqueda debe escribir debajo del título de cada columna la palabra clave de interés.
                            Por ejemplo en la columna Ítem: puede buscar elementos como kits de emergencia y le saldrán a nivel
                            nacional los contratos realizados para adquirir este producto.
                            Como otro ejemplo, si desea ver la contratación en su departamento o municipio, puede buscar escribiendo
                            el nombre de su territorio debajo de la columna correspondiente.

                            """
                        ),
                    ],
                    className='text-left p-5'
                ),
            ]
        ),
        html.Div (
            # Table: Alerta: Sobrecosto
            className='div-for-table',
            children=[
                table_transparencia
            ]
        ),
    ]
)