import dash
import dash_bootstrap_components as dbc
from dash import html

from arraymaker.pages.common import make_footer, make_navbar

dash.register_page(__name__, path='/', title='ArrayMaker')

navbar = make_navbar()
footer = make_footer()

card_sensors = dbc.Card([
    dbc.Row([
        dbc.Col(
            dbc.CardImg(src="/arraymaker/assets/vuv4quad.jpg", top=True,
                        className="card-img-top overflow-hidden",
                        style={'height': '100%', "object-fit": "cover"}),

        ),
        dbc.Col(
            dbc.CardBody([
                html.H4("Sensor types", className="card-title"),
                html.P(
                    "Get information about the different sensor types.",
                    className="card-text",
                ),
                dbc.Button("Sensor types", color="primary",
                           href="/arraymaker/photosensors"),

            ]),
            style={"height": "100%", "display": "flex",
                   "flexDirection": "column"})  # Col (body)
    ], className="g-0",
        style={"height": "100%", "display": "flex",
               "flexDirection": "row"})  # Row
], className="mb-0 border-0 shadow", style={"height": "100%"}  # card
)

card_sipms = dbc.Card([
    dbc.Row([
        dbc.Col(
            dbc.CardImg(src="/arraymaker/assets/sipmarray_small.jpg", top=True,
                        className="card-img-top overflow-hidden",
                        style={'height': '100%', "object-fit": "cover"}),

        ),
        dbc.Col(
            dbc.CardBody([
                html.H4("SiPM array", className="card-title"),
                html.P(
                    "Fill an array with the novel SiPMs.",
                    className="card-text",
                ),
                dbc.Button("SiPM ArrayMaker", color="primary",
                           href="/arraymaker/sipmarray"),

            ]),
            style={"height": "100%", "display": "flex",
                   "flexDirection": "column"})  # Col (body)
    ], className="g-0",
        style={"height": "100%", "display": "flex",
               "flexDirection": "row"})  # Row
], className="mb-0 border-0 shadow", style={"height": "100%"}  # card
)

card_pmts = dbc.Card([
    dbc.Row([
        dbc.Col(
            dbc.CardImg(src="/arraymaker/assets/pmts_zoom_small.JPG", top=True,
                        className="card-img-top overflow-hidden",
                        style={'height': '100%', "object-fit": "cover"}),

        ),
        dbc.Col(
            dbc.CardBody([
                html.H4("PMT array", className="card-title"),
                html.P(
                    "Choose the and old or new PMT and make an array.",
                    className="card-text",
                ),
                dbc.Button("PMT ArrayMaker", color="primary",
                           href="/arraymaker/pmtarray"),

            ]),
            style={"height": "100%", "display": "flex",
                   "flexDirection": "column"})  # Col (body)
    ], className="g-0",
        style={"height": "100%", "display": "flex",
               "flexDirection": "row"})  # Row
], className="mb-0 border-0 shadow", style={"height": "100%"}  # card
)

text_whatis = """Array maker is a tool to help plan photosensor arrays. It 
provides a set of standard, currently common, photosensors and allows to 
idealy place them in a circular array. It then provides detailed information 
on the number of sensors required, their total coverage, and the option to 
export the sensor coordinates for further use."""

text_howto = """To use ArrayMaker, simply define the diameter of the planned 
circular array, select the type of sensor you want to use and the spacing 
between sensors. The tool will then display how they would be optimally 
placed, the total coverage of the array and the number of sensors required. 
the coordinates of the sensors can then be exported to use."""

layout = dbc.Container([
    navbar,
    html.H1('ArrayMaker', style={'margin-top': '1rem',
                                 'text-align': 'center'}),
    html.H4('Quickly and easily plan your future detector array',
            style={'text-align': 'center'}),
    html.Hr(style={'margin-bottom': '1rem'}),
    dbc.Row([
            dbc.Col([
                html.H3('What is ArrayMaker?', style={'text-align': 'center'}),
                html.Div(text_whatis, style={'text-align': 'justify',
                                             'padding-right': '2rem',
                                             'padding-left': '2rem'})
            ]),
            dbc.Col([
                html.H3('How to use?', style={'text-align': 'center'}),
                html.Div(text_howto, style={'text-align': 'justify',
                                            'padding-right': '2rem',
                                            'padding-left': '2rem'})
            ]),

            ], style={'margin-top': '1rem', 'margin-bottom': '2rem'}),
    html.Hr(style={'margin-bottom': '2rem'}),
    html.Div([
        dbc.Row(
            [
                dbc.Col(card_sensors, width=12, sm=6,
                        md=4, lg=3, align='start'),
                dbc.Col(card_sipms, width=12, sm=6, md=4, lg=3, align='start'),
                dbc.Col(card_pmts, width=12, sm=6, md=4, lg=3, align='start'),
            ],
            justify='center',
            className='flex-wrap'
        )
    ]),
    footer
], fluid=True)
