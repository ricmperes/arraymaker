import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html

from arraymaker.utils.plotly_functions import plot_circular_pmt_array
from arraymaker.utils.plotly_functions import plot_sipm_array
from arraymaker.utils.pmt_aux_functions import build_updated_pmt_array

from arraymaker.pages.common import make_footer, make_navbar

dash.register_page(__name__, path='/customarray/', 
                   title='ArrayMaker - custom unit')

navbar = make_navbar()
footer = make_footer()


# Initial PMTarray
initial_model = '3in'
initial_diameter = 300
initial_margin = 0
initial_intra_pmt_distance = 10
array = build_updated_pmt_array(initial_model, initial_diameter,
                                initial_margin, initial_intra_pmt_distance)

# Initial text
n_pmts = array.n_pmts
active_area = array.total_pmt_active_area
coverage = array.pmt_coverage
text_result_string = f'Number of sensors: {n_pmts}\nActive area: {active_area:.2f} mm2\nCoverage: {coverage:.2f} %'

text_active_corners = ''


option_card_array = dbc.Card([
    dbc.CardBody([
        html.H4("Define array properties", className="card-title"),
        html.Div([
            html.Div(
                id='text-diameter-custom',
                children=f'Array diameter [mm]:',
                style={'marginLeft': '10px', 'marginTop': '15px'}
            ),
            dcc.Input(
                id='diameter-input-custom',
                type='number',
                value=initial_diameter,
                debounce=True,
                min=1,
                max=10000,
                style={'width': '100px',
                       'marginLeft': '10px', 'marginTop': '15px'}
            ),
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div([
            html.Div(
                id='text-margin-custom',
                children=f'Margin to border [mm]:',
                style={'marginLeft': '10px', 'marginTop': '15px'}
            ),
            dcc.Input(
                id='margin-input-custom',
                type='number',
                value=initial_margin,
                debounce=True,
                style={'width': '100px',
                       'marginLeft': '10px', 'marginTop': '15px'}
            ),
            html.I(className="bi bi-exclamation-triangle-fill me-2",
                   id='coverage-warning-icon-custom',
                   style={'color': 'red', 'margin-top': '0.5rem',
                          'margin-left': '1rem', 'display': 'none'}),
            dbc.Tooltip(
                "If margin > 0, the ative area coverage should be "
                "taken as approximate, as sensros outside the "
                "array are still counted as active area.",
                target="coverage-warning-icon-custom",
            ),
        ], style={'display': 'flex', 'align-items': 'center'}),
        html.Div(id='div-intra-distance-custom',
                 children=[
                     html.Div(
                         id='text-intra-distance-custom',
                         children=f'Inter-sensor distance [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='intra-distance-input-custom',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

    ]),
])

option_card_sensor = dbc.Card([
    dbc.CardBody([
        html.H4("Select custom sensor unit options", className="card-title"),
        html.Div([html.Div(
            id='text-model-pmt',
            children=f'Sensor shape:',
            # Add some margin for better separation
            style={'marginLeft': '10px'}
        ),
            dcc.Dropdown(
            id='dropdown-selection-pmt',
            options=[
                {'label': 'round', 'value': 'round'},
                {'label': 'rectangular', 'value': 'rectangular'},
            ],
            value='3in',  # Default value
            style={'width': '180px', 'marginLeft': '5px'}
        ),
        ], style={'display': 'flex', 'align-items': 'center'}),

        html.Div(id='div-custom-width-package',
                 children=[
                     html.Div(
                         id='text-custom-width-package',
                         children=f'Packaging width [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-width-package',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),
            
            html.Div(id='div-custom-height-package',
                 children=[
                     html.Div(
                         id='text-custom-height-package',
                         children=f'Packaging height [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-height-package',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-width-tolerance',
                 children=[
                     html.Div(
                         id='text-custom-width-tolerance',
                         children=f'Packaging width tolerance [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-width-tolerance',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-height-tolerance',
                 children=[
                     html.Div(
                         id='text-custom-height-tolerance',
                         children=f'Packaging height tolerance [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-height-tolerance',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),
            
            html.Div(id='div-custom-width-active',
                 children=[
                     html.Div(
                         id='text-custom-width-active',
                         children=f'Packaging width active [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-width-active',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-height-active',
                 children=[
                     html.Div(
                         id='text-custom-height-active',
                         children=f'Packaging height active [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-height-active',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-D-corner-x-active',
                 children=[
                     html.Div(
                         id='text-custom-D-corner-x-active',
                         children=f'Width distance from packaging\nto active area [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-D-corner-x-active',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-D-corner-y-active',
                 children=[
                     html.Div(
                         id='text-custom-D-corner-y-active',
                         children=f'Height distance from packaging\nto active area [mm]:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-D-corner-y-active',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-active-area-correction',
                 children=[
                     html.Div(
                         id='text-custom-active-area-correction',
                         children=f'Active area correction factor:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-active-area-correction',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-fill-factor',
                 children=[
                     html.Div(
                         id='text-custom-fill-factor',
                         children=f'Fill factor:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-fill-factor',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

            html.Div(id='div-custom-pde',
                 children=[
                     html.Div(
                         id='text-custom-pde',
                         children=f'PDE:',
                         style={'marginLeft': '10px', 'marginTop': '15px'}
                     ),
                     dcc.Input(
                         id='input-custom-pde',
                         type='number',
                         value=initial_margin,
                         debounce=True,
                         min = 0.,
                         style={'width': '100px', 'marginLeft': '10px',
                                'marginTop': '15px'}
                     ),
                 ], style={'display': 'flex', 'align-items': 'center'}),

        
    ]),
])


text_results = dcc.Textarea(
    id='text-result-custom',
    value=text_result_string,
    readOnly=True,
    style={'width': '100%', 'height': '7rem',
           # 'margin-left': '1rem',
           'margin-top': '1rem',
           'resize': 'none', 'margin-bottom': '1rem'}
)

export_buttons = html.Div([
    dbc.Button(
        f'Export active\ncorners',
        id='download-btn-active-corners-custom',
        color='primary',
        className='mb-2',
        style={'width': '60%'}
    ),
    dbc.Button(
        f'Export packaging\ncorners',
        id='download-btn-packaging-corners-custom',
        color='primary',
        className='mb-2',
        style={'width': '60%'}
    ),
    dbc.Button(
        f'Export sensor\ncenters',
        id='download-btn-centers-custom',
        color='primary',
        className='mb-2',
        style={'width': '60%'}
    ),
], className='d-flex flex-column align-items-center',
)  # style={'display': 'col', 'align-items': 'center'})


plot = dcc.Graph(
    id='custom-array-plot-custom',
    figure=go.Figure(),
    style={'width': '90%',
                    'height': '100%',
                    'align-items': 'center'},
    responsive=True,
)

# style={'marginLeft': '10px', 'margin-top': '10px',
#    'margin-bottom': '10px'}),

export_text = dcc.Textarea(
    id='export-text-custom',
    value='',
    readOnly=True,
    style={'marginLeft': '1rem', 'width': '90%',
           'height': '100%',
           'resize': 'none', }
)

layout = dbc.Container([
    navbar,
    html.H1("Custom Sensor Array",
            style={'margin-top': '1rem',
                   'text-align': 'center'}),
    html.Hr(style={'margin-bottom': '1rem'}),
    dbc.Row([  # row of options, text and plot
        dbc.Col([  # colum of options and text
            dbc.Row(dbc.Col(  # row of options
                option_card_array
            ), style = {'margin-bottom': '1rem'}),
            dbc.Row(dbc.Col(  # row of options
                option_card_sensor
            )),
            dbc.Row(dbc.Col(  # row of property text
                text_results
            ))
        ], width={'size': 6, 'offset': 0}, ),  # style={'margin-left': '1rem'}),
        dbc.Col([  # column of plot
            dcc.Loading(plot,
                        type = 'circle',
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
