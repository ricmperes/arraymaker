import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from pmtarray import PMTunit
from sipmarray import SiPMunit

from arraymaker.utils.plotly_functions import (plot_circular_pmt_array,
                                               plot_sipm_array)
from arraymaker.utils.pmt_aux_functions import build_updated_pmt_array

from arraymaker.pages.common import make_footer, make_navbar

dash.register_page(__name__, path='/photosensors/',
                   title='ArrayMaker - photosensors')


# Inital PMTunit
pmtunit = PMTunit(model='3in')
pmt_properties = pmtunit.get_properties_str()

# Initial SiPMunit
sipmunit = SiPMunit(model='6x6')


navbar = make_navbar()
footer = make_footer()


# PMTs
options_pmt = html.Div([html.H5(
    id='text-model-pmtsensor',
    children=f'PMT Model:',
    # Add some margin for better separation
    style={'marginLeft': '1rem', 'align-items': 'center'}
),
    dcc.Dropdown(
    id='dropdown-selection-pmtsensor',
    options=[
        {'label': '3"', 'value': '3in'},
        {'label': '2"', 'value': '2in'},
    ],
    value='3in',  # Default value
    style={'width': '200px', 'marginLeft': '1rem',
           'align-items': 'center'}
),
], style={'display': 'flex', 'align-items': 'center',
          'margin-top': '2rem', 'margin-bottom': '2rem'}),

pmt_properties_df = pmtunit.get_properties_df()
table_properties_pmt = dbc.Table.from_dataframe(df=pmt_properties_df,
                                                striped=True, bordered=True,
                                                hover=True, size='sm',
                                                style={'margin-left': '2rem',
                                                       'margin-bottom': '2rem',
                                                       'margin-top': '1rem'})

plot_pmt = dcc.Graph(
    id='plot-pmt-unit',
    figure=go.Figure(),
    style={'width': '80%',
           'height': '80%',
           'align-items': 'center'},
    responsive=True,
)

tab_pmt = dbc.Row([
    dbc.Col([  # left column
        dbc.Row(dbc.Col(options_pmt)),  # dropdown sensor model
        dbc.Row(dbc.Col([html.H5("Photosensor properties",
                                 style={'margin-left': '1rem',
                                        'margin-bottom': '1rem'},),
                        html.Div(table_properties_pmt,
                                 id='table-properties-pmt')
                         ]))],  # text properties of sensor
            style={'margin-bottom': '2rem',
                   'margin-top': '2rem'}),
    dbc.Col([plot_pmt  # right column for plot
             ], style={'margin-left': '2rem', 'margin-right': '2rem',
                       'margin-bottom': '2rem', 'margin-top': '2rem',
                       'align-items': 'center'})
])


# SiPMs
options_sipm = html.Div([html.H5(
    id='text-model-sipmsensor',
    children=f'SiPM Model:',
    # Add some margin for better separation
    style={'marginLeft': '1rem',
           'align-items': 'center'}
),
    dcc.Dropdown(
    id='dropdown-selection-simpsensor',
    options=[
        {'label': 'UZH Tile', 'value': 'tile'},
        {'label': 'Quad (12x12 mm2)', 'value': 'quad'},
        {'label': '6x6 mm2', 'value': '6x6'},
        {'label': '3x3 mm2', 'value': '3x3'},
        {'label': 'Digital SiPM modules', 'value': 'digital'},
    ],
    value='tile',  # Default value
    style={'width': '200px', 'marginLeft': '1rem',
                   'align-items': 'center'}
),
], style={'display': 'flex', 'align-items': 'center',
          'margin-top': '2rem', 'margin-bottom': '2rem'}),

sipm_properties_df = sipmunit.get_properties_df()
table_properties_sipm = dbc.Table.from_dataframe(df=sipm_properties_df,
                                                 striped=True, bordered=True,
                                                 hover=True, size='md',
                                                 style={'margin-left': '2rem',
                                                        'margin-bottom': '2rem',
                                                        'margin-top': '1rem'})


plot_sipm = dcc.Graph(
    id='plot-sipm-unit',
    figure=go.Figure(),
    style={'width': '80%',
           'height': '80%',
           'align-items': 'center'},
    responsive=True,
)

tab_sipm = dbc.Row([
    dbc.Col([  # left column
        dbc.Row(dbc.Col(options_sipm)),  # dropdown sensor model
        dbc.Row(dbc.Col([html.H5("Photosensor properties",
                                 style={'margin-left': '1rem',
                                         'margin-bottom': '1rem'},),
                        html.Div(children=table_properties_sipm,
                                 id='table-properties-sipm')
                         ]))],  # text properties of sensor
            style={'margin-bottom': '2rem',
                   'margin-top': '2rem'}),
    dbc.Col([plot_sipm  # right column for plot
             ], style={'margin-left': '2rem', 'margin-right': '2rem',
                       'margin-bottom': '2rem', 'margin-top': '2rem',
                       'align-items': 'center'})
])


# Main layout
layout = dbc.Container([
    navbar,
    html.H1("Photosensor Database",
            style={'margin-top': '1rem',
                   'text-align': 'center'}),
    html.Hr(style={'margin-bottom': '1rem'}),

    dbc.Tabs([
        dbc.Tab(tab_pmt, label="PMT"),
        dbc.Tab(tab_sipm, label="SiPM"),
    ]),

    footer
], fluid=True)


# # Deprecated
# text_properties_pmt = html.Div([
#     html.H5("Photosensor properties", style = {'margin-left': '1rem',
#                                                'margin-bottom': '1rem'} ,),
#     dcc.Textarea(
#             id='text-result-pmt',
#             value=pmt_properties,
#             readOnly=True,
#             style={'width' : '100%','height': '20rem',
#                 'margin-left': '1rem',
#                 #'margin-top': '1rem',
#                 'resize': 'none', 'margin-bottom': '2rem',
#                 'margin-left': '1rem'}
#         )
#     ])
