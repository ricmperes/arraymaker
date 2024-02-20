import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html

from arraymaker.utils.sipm_aux_functions import (build_updated_sipm_array,
                                                 get_sipm_properties_to_print)

from arraymaker.pages.common import make_footer, make_navbar

dash.register_page(__name__, path='/sipmarray/', title='ArrayMaker - SiPMs')

navbar = make_navbar()
footer = make_footer()


# Initial SiPMarray
initial_model = 'tile'
initial_diameter = 300
initial_margin = 0
initial_intra_sipm_distance = 10
array = build_updated_sipm_array(
    initial_model, initial_diameter, 
    initial_margin, initial_intra_sipm_distance)

# Initial text
text_result_string = get_sipm_properties_to_print(array)
text_active_corners = ''


option_card = dbc.Card([
    dbc.CardBody([
        html.H4("Select SiPM options", className="card-title"),
        # html.P(
        #     "Select options for the SiPM array.",
        #     className="card-text",
        # ),

        html.Div([html.Div(
            id='text-model-sipm',
            children=f'SiPM Model:',
            # Add some margin for better separation
            style={'marginLeft': '10px'}
        ),
            dcc.Dropdown(
            id='dropdown-selection-sipm',
            options=[
                {'label': 'UZH Tile', 'value': 'tile'},
                {'label': 'Quad (12x12 mm2)', 'value': 'quad'},
                {'label': '6x6 mm2', 'value': '6x6'},
                {'label': '3x3 mm2', 'value': '3x3'},
                {'label': 'Digital SiPM modules', 'value': 'digital'},
                # Add more options as needed
            ],
            value='tile',  # Default value
            style={'width': '200px', 'marginLeft': '5px'}
        ),
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            html.Div(
                id='text-diameter-sipm',
                children=f'Array diameter [mm]:',
                style={'marginLeft': '10px', 'marginTop': '15px'}
            ),
            dcc.Input(
                id='diameter-input-sipm',
                type='number',
                value=initial_diameter,
                debounce=True,
                min=1,
                max=10000,
                style={'width': '100px', 'marginLeft': '10px',
                       'marginTop': '15px'}
            ),
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            html.Div(
                id='text-margin-sipm',
                children=f'Margin to border [mm]:',
                style={'marginLeft': '10px', 'marginTop': '15px'}
            ),
            dcc.Input(
                id='margin-input-sipm',
                type='number',
                value=initial_margin,
                debounce=True,
                style={'width': '100px',
                       'marginLeft': '10px', 'marginTop': '15px'}
            ),
            html.I(id='coverage-warning-icon-sipm',
                   className="bi bi-exclamation-triangle-fill me-2",
                   style={'color': 'red', 'margin-top': '0.5rem',
                          'margin-left': '1rem', 'display': 'none'}),
            dbc.Tooltip(
                "If margin > 0, the ative area coverage should be "
                "taken as approximate, as sensros outside the "
                "array are still counted as active area.",
                target="coverage-warning-icon-sipm",
            ),
        ], style={'display': 'flex', 'align-items': 'center'},),
        html.Div(id='div-intra-distance-sipm',
                 children=[
                     html.Div(
                         id='text-intra-distance-sipm',
                         children=f'Intra-SiPM distance [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='intra-distance-input-sipm',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'})
    ]),
])

text_results = dcc.Textarea(
    id='text-result-sipm',
    value=text_result_string,
    readOnly=True,
    style={'width': '100%', 'height': '8rem',
           # 'margin-left': '1rem',
           'margin-top': '1rem',
           'resize': 'none', 'margin-bottom': '1rem'}
),

export_buttons = html.Div([
    dbc.Button(
        f'Export active\ncorners',
        id='download-btn-active-corners-sipm',
        color='primary',
        className='mb-2',
        style={'width': '60%'}
    ),
    dbc.Button(
        f'Export packaging\ncorners',
        id='download-btn-packaging-corners-sipm',
        color='primary',
        className='mb-2',
        style={'width': '60%'}
    ),
    dbc.Button(
        f'Export sensor\ncenters',
        id='download-btn-centers-sipm',
        color='primary',
        className='mb-2',
        style={'width': '60%'}
    ),
], className='d-flex flex-column align-items-center',
)  # style={'display': 'col', 'align-items': 'center'})


plot = dcc.Graph(
    id='sipm-array-plot-sipm',
    figure=go.Figure(),
    style={'width': '90%',
                    'height': '100%',
                    'align-items': 'center'},
    responsive=True,
)

# style={'marginLeft': '10px', 'margin-top': '10px',
#    'margin-bottom': '10px'}),

export_text = dcc.Textarea(
    id='export-text-sipm',
    value='',
    readOnly=True,
    style={'marginLeft': '1rem', 'width': '90%',
           'height': '100%',
           'resize': 'none', }
)
layout = dbc.Container([
    navbar,
    html.H1("SiPM Array Display",
            style={'margin-top': '1rem',
                   'text-align': 'center'}),
    html.Hr(style={'margin-bottom': '1rem'}),
    dbc.Row([  # row of options, text and plot
        dbc.Col([  # colum of options and text
            dbc.Row(dbc.Col(  # row of options
                option_card
            )),
            dbc.Row(dbc.Col(  # row of property text
                text_results
            ))
        ], width={'size': 6, 'offset': 0}, ),  # style={'margin-left': '1rem'}),
        dbc.Col([  # column of plot
            dcc.Loading(
                plot,
                type='circle',
            )

        ], width={'size': 6})
    ]),
    dbc.Row([  # row of export options and export box
        dbc.Col([  # column of export options

            export_buttons

        ], width={'size': 6}, ),  # style={'margin-left': '1rem'}), style={'margin-left': '1rem'}),
        dbc.Col([  # column of export box

            export_text

        ], width={'size': 6})
    ]),

    footer
], fluid=True)
