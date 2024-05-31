import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from pmtarray import PMTunit
from sipmarray import SiPMunit

#from arraymaker.utils.xemass_functions import make_initial_plot
from arraymaker.pages.common import make_footer, make_navbar

dash.register_page(__name__, path='/xe-mass/',
                   title='ArrayMaker - Xe mass calculator')


#initial_plot = make_initial_plot()


navbar = make_navbar()
footer = make_footer()


modal_failed_fmfile = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Failed upload")),
                dbc.ModalBody("The uploaded file could not be processed. "
                              "Make sure it is related to FM01"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal_fm", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_fail_fmupload",
            is_open=False,
        )

modal_failed_fcfile = dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Failed upload")),
                dbc.ModalBody("The uploaded file could not be processed. "
                                "Make sure it is related to FC01"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close_modal_fc", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal_fail_fcupload",
            is_open=False,
        )

upload_card = dbc.Card([
    dbc.CardBody([
        html.Div([
            html.H5("Files",
                    style={'margin-right': '3rem'},
                    ),
            html.Div([
                dcc.Upload(
                    dbc.Button("FM01", 
                            id = 'button-fm01',
                            color="primary"), 
                    id = 'upload-fm01',
                    multiple = False,
                    ),
                dcc.Upload(
                    dbc.Button("FC01", 
                            id = 'button-fc01',
                            color="primary"), 
                    id = 'upload-fc01',
                    multiple = False,
                    ),
                ], className='d-grid gap-3 d-flex justify-content-center'),
                ], style = {'display': 'flex',
                            'margin-left': '1rem',
                        'margin-bottom': '2rem',
                        'margin_top':'2rem'}),
        html.Div([html.H5("Flow offset [slpm]"),
                  dcc.Input(
                      id='input-flow-offset',
                      type='number',
                      value=0.0,
                      debounce=True,
                      style={'width': '5rem',
                             'marginLeft': '3rem', }),
                ], style={'margin-left': '1rem',
                          'margin-top': '2rem',
                          'margin-bottom': '1rem',
                          'display': 'flex'}),
        html.Div([html.H5("Mass offset [kg]"),
                  dcc.Input(
                      id='input-mass-offset',
                      type='number',
                      value=0.0,
                      debounce=True,
                      style={'width': '5rem',
                             'marginLeft': '3rem', }),
                ], style={'margin-left': '1rem',
                          'margin-top': '2rem',
                          'margin-bottom': '1rem',
                          'display': 'flex'}),
        html.Div([dbc.Button('Generate plot',
                             id = 'button-generate-plot',
                             color = 'primary',
                             disabled = True)],
                 className="d-grid gap-2 col-6 mx-auto my-4",),
        modal_failed_fmfile,
        modal_failed_fcfile,
        ],style={'margin_top' : '2rem'}),
    ])

plot_flow = dcc.Graph(
    id='plot-flow-mass',
    #figure=initial_plot,
     style={'width': '100%',
            'height': '100%',
            'align-items': 'center'},
    responsive=True,
)

tab_flow = dbc.Row([
    dbc.Col([  # left column
        dbc.Row([dbc.Col(upload_card,width={'size': 3, 'offset': 0}),
                 dbc.Col(plot_flow, width = 9)],
                 style = {'height' : '30rem' })
                 ],  # text properties of sensor
            style={'margin-bottom': '0rem',
                   'margin-top': '0rem'})
                   ])

flow_converter = dbc.Row([
            html.H5("Flow converter",
                             style={'margin-left': '1rem',
                                    'margin-bottom': '0.5rem'},),
            # slpm to gpm
            html.Div(
                [dcc.Input(
                    id='slpm-value',
                    type='number',
                    value=0.0,
                    debounce=True,
                    style={'width': '4rem','marginLeft': '1rem', 
                            'marginTop': '0.5rem'}),
                html.Div('slpm = ', style = {'margin-left': '0.5rem'}),
                html.Div(id = 'gpm-text'),], 
                style = {'display': 'flex', 'margin-left': '1rem',
                         'margin-top': '1rem',
                         'align-items': 'center'}),
            # gpm to slpm
            html.Div(
                [dcc.Input(
                    id='gpm-value',
                    type='number',
                    value=0.0,
                    debounce=True,
                    style={'width': '4rem','marginLeft': '1rem', 
                            'marginTop': '0.5rem'}),
                html.Div('gpm = ', style = {'margin-left': '0.5rem'}),
                html.Div(id = 'slpm-text'),], 
                style = {'display': 'flex', 'margin-left': '1rem',
                         'margin-bottom': '1rem', 
                         'align-items': 'center'})
        ])


# xenon properties table
xe_table_header = [
    html.Thead(html.Tr([html.Th("Property"), html.Th("Value")]))
]

row1 = html.Tr([html.Td("Density at std (0 ºC, 1 bar)"), html.Td("5.8980 g/l")])
row2 = html.Tr([html.Td("Density at 177 K, 2 bar"), html.Td("2.8609(57) g/ml")])
row3 = html.Tr([html.Td("Triple point temp"), html.Td("161.38 K")])
row4 = html.Tr([html.Td("Triple point press"), html.Td("0.816 bar")])

table_body = [html.Tbody([row1, row2, row3, row4])]

xe_properties_table = dbc.Table(xe_table_header + table_body, bordered=True)

tab_calc = dbc.Row([
    dbc.Col(  # left column
        flow_converter,style={'margin-bottom': '2rem',
                  'margin-top': '2rem'}),
    dbc.Col(  # left column
        xe_properties_table,
        style={'margin-bottom': '2rem',
               'margin-top': '2rem'})
        ])


# Main layout
layout = dbc.Container([
    navbar,
    html.H1("Xe Mass Calculator",
            style={'margin-top': '1rem',
                   'text-align': 'center'}),
    html.Hr(style={'margin-bottom': '1rem'}),

    dbc.Tabs([
        dbc.Tab(tab_flow, label="Flow integrator"),
        dbc.Tab(tab_calc, label="Mass calculator"),
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
