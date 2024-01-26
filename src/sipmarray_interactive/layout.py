import plotly.graph_objects as go
from dash import dcc, html
from sipmarray_interactive.utils.interactive_aux_functions import build_updated_array
import dash_bootstrap_components as dbc


# Initial SiPMarray
initial_model = 'tile'
initial_diameter = 160
initial_margin = 10
array = build_updated_array(initial_model, initial_diameter, initial_margin)

# Initial text
n_sipms = array.n_sipms
active_area = array.total_sipm_active_area
coverage = array.sipm_coverage
text_result_string = f'Number of sensors: {n_sipms}\nActive area: {active_area:.2f} mm2\nCoverage: {coverage:.2f} %'

text_active_corners = ''

def get_layout():
    return dbc.Cointainer(html.Div([
    html.H1("SiPM Array Display - Alpha version"),
    html.Div([
        html.Div(
                id='text-model',
                children=f'SiPM Model:',
                style={'marginLeft': '10px'}  # Add some margin for better separation
            ),
        dcc.Dropdown(
            id='dropdown-selection',
            options=[
                {'label': 'UZH Tile', 'value': 'tile'},
                {'label': 'Quad (12x12 mm2)', 'value': 'quad'},
                {'label': '6x6 mm2', 'value': '6x6'},
                {'label': '3x3 mm2', 'value': '3x3'}
                # Add more options as needed
            ],
            value='tile',  # Default value
            style={'width': '180px', 'marginLeft': '5px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div([
        html.Div(
                id='text-diameter',
                children=f'Array diameter [mm]:',
                style={'marginLeft': '10px', 'marginTop': '15px'}
            ),
        dcc.Input(
            id='diameter-input',
            type='number',
            value=initial_diameter,
            debounce=True,
            min=1,
            max=10000,
            style={'width': '150px', 'marginLeft': '10px', 'marginTop': '15px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div([
        html.Div(
                id='text-margin',
                children=f'Margin to border [mm]:',
                style={'marginLeft': '10px', 'marginTop': '15px'}
            ),
        dcc.Input(
            id='margin-input',
            type='number',
            value=initial_margin,
            debounce=True,
            style={'width': '145px', 'marginLeft': '10px', 'marginTop': '15px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center'}),

    
    dcc.Textarea(
        id='text-result',
        value=text_result_string,
        readOnly=True,
        style={'marginLeft': '10px','width': '300px',
                'height': '80px', 'margin-top': '10px',
                'resize': 'none', 'margin-bottom': '10px'}  
    ),

    html.Div([
        dcc.Graph(
            id='sipm-array-plot',
            figure=go.Figure(),
            style = {'width': '60%'},
            responsive=True,
            )
        ],
        style = {'marginLeft': '10px', 'margin-top': '10px',
            'margin-bottom': '10px'}),
    html.Div([
        html.Button(
            'Export active corners',
            id='download-btn-active-corners',
            className='btn btn-success',
            style={'margin-top': '10px', 'margin-left': '10px'}
        ),
        html.Button(
            'Export packaging corners',
            id='download-btn-packaging-corners',
            className='btn btn-success',
            style={'margin-top': '10px', 'margin-left': '10px'}
        ),
        html.Button(
            'Export sensor centers',
            id='download-btn-centers',
            className='btn btn-success',
            style={'margin-top': '10px', 'margin-left': '10px'}
        ),
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div([
        dcc.Textarea(
            id='export-text',
            value='',
            readOnly = True,
            style={'marginLeft': '10px','width': '60%',
                    'height': '200px', 'margin-top': '10px',
                    'resize': 'none', 'margin-bottom': '0px'}  
        )],
    ),
    
    html.Footer("by R. Peres for the DARWIN collaboration, Jan 2024")
    ])
    )
