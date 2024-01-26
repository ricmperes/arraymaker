import dash
from dash import html
import dash_bootstrap_components as dbc
from .common_navbar import make_navbar

dash.register_page(__name__, path='/')

navbar = make_navbar()
_text = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Arcu risus quis varius quam quisque id diam vel quam. Pharetra massa massa ultricies mi quis. Pellentesque sit amet porttitor eget dolor morbi non arcu risus. Vitae nunc sed velit dignissim sodales. Pharetra diam sit amet nisl suscipit adipiscing. Felis donec et odio pellentesque. Facilisi morbi tempus iaculis urna id volutpat lacus laoreet non. Ipsum faucibus vitae aliquet nec ullamcorper sit amet. Facilisis mauris sit amet massa. Bibendum at varius vel pharetra vel. Sed risus ultricies tristique nulla.

Libero nunc consequat interdum varius sit amet mattis vulputate enim. Id donec ultrices tincidunt arcu. Auctor neque vitae tempus quam pellentesque nec nam aliquam. Non nisi est sit amet facilisis magna. Viverra tellus in hac habitasse platea dictumst vestibulum rhoncus est. Massa sapien faucibus et molestie ac feugiat sed lectus vestibulum. Dolor sit amet consectetur adipiscing elit ut aliquam purus sit. Commodo viverra maecenas accumsan lacus vel facilisis volutpat est. Volutpat maecenas volutpat blandit aliquam etiam. Leo urna molestie at elementum eu facilisis sed odio. Sem integer vitae justo eget magna fermentum iaculis eu non. Risus nullam eget felis eget nunc lobortis mattis aliquam faucibus. Sed augue lacus viverra vitae congue.

Purus sit amet volutpat consequat mauris nunc congue. Consequat interdum varius sit amet mattis vulputate enim. Erat nam at lectus urna duis convallis. Vitae elementum curabitur vitae nunc. Est ante in nibh mauris cursus mattis molestie a. Mauris a diam maecenas sed enim ut. Sed egestas egestas fringilla phasellus. Lobortis scelerisque fermentum dui faucibus in ornare quam viverra. Nisl nisi scelerisque eu ultrices vitae. Hac habitasse platea dictumst quisque sagittis purus sit amet volutpat. Eu feugiat pretium nibh ipsum. Risus viverra adipiscing at in tellus integer feugiat scelerisque varius. Faucibus interdum posuere lorem ipsum dolor sit amet. Nunc vel risus commodo viverra.
"""

card_sensors = dbc.Card([
    dbc.CardImg(src="/arraymaker/assets/vuv4quad.jpg", top=True, 
                ),#style={'width': '100%'}),
    dbc.CardBody([
        html.H4("Sensor types", className="card-title"),
        html.P(
            "Get information about the different sensor types.",
            className="card-text",
        ),
        dbc.Button("Go to sensors", color="primary", 
                    href="/arraymaker/sensors"),
    ])
    ], style={"width": "18rem"})

card_sipms = dbc.Card([
    dbc.CardImg(src="/arraymaker/assets/sipmarray_small.jpg", top=True, 
                ),#style={'width': '100%'}),
    dbc.CardBody([
        html.H4("Make a SiPM array!", className="card-title"),
        html.P(
            "Define the type of sensor, spacing and array size and get your SiPM array.",
            className="card-text",
        ),
        dbc.Button("Go to array", color="primary", 
                    href="/arraymaker/sipmarray"),
    ])
    ], style={"width": "18rem"})

card_pmts = dbc.Card([
    dbc.CardImg(src="/arraymaker/assets/pmts_zoom_small.JPG", top=True, 
                ),#style={'width': '100%'}),
    dbc.CardBody([
        html.H4("Make a PMT array!", className="card-title"),
        html.P(
            "Define the type of sensor, spacing and array size and get your PMT array.",
            className="card-text",
        ),
        dbc.Button("Go to array", color="primary", 
                    href="/arraymaker/pmtarray"),
    ])
    ], style={"width": "18rem"})


layout = dbc.Container([
    navbar, 
    html.H1('This is just a title', style = {'margin-top': '1rem'}),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.Div(_text)),
        #dbc.Col(html.Div('This is our Home page content right.')),
        ]),
    dbc.Row([
        dbc.Col(card_sensors),
        dbc.Col(card_sipms),
        dbc.Col(card_pmts),
        ])
    ],fluid=True)


