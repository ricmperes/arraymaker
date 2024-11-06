import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from arraymaker.pages.common import make_footer, make_navbar

dash.register_page(__name__, path='/about/', title='ArrayMaker')

navbar = make_navbar()
footer = make_footer()

height_of_page = '40rem'
width_picture = '27rem'

picture_carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": "/arraymaker/assets/xenoscope1.jpg",
         "img_style": {'height': height_of_page, 'width': width_picture,
                       "object-fit": "cover", 'align-items': 'center'}},
        {"key": "2", "src": "/arraymaker/assets/xenoscope2.jpg",
         "img_style": {'height': height_of_page, 'width': width_picture,
                       "object-fit": "cover"}},
        {"key": "3", "src": "/arraymaker/assets/lars1.jpg",
         "img_style": {'height': height_of_page, 'width': width_picture,
                       "object-fit": "cover"}},
        {"key": "4", "src": "/arraymaker/assets/lars2.jpg",
         "img_style": {'height': height_of_page, 'width': width_picture,
                       "object-fit": "cover"}},
    ],
    controls=True,
    indicators=True,

    className="carousel-slide"
)

about_text = dcc.Markdown('''**ArrayMaker** was developed in the context of 
the [DARWIN](https://darwin.physik.uzh.ch/) and [XLZD](https://xlzd.org/) 
projects. Both of these aim to design, construct and operate the 
next-generation dark matter detector and neutrino observatory using liquid 
xenon as target material. The core of the detector a dual-phase time
projection chamber (TPC) instrumented with two array os photosensors, on
the top and bottom of the active volume. The photosensors are used to
detect the scintillation light produced by the interaction of particles
with the liquid xenon target. 

As we reach a critical design phase of the next-generation LXe TPCs, 
several candidate photosensor units are being tested and characterised. 
**ArrayMaker** is a tool to help quickly get information on the different
sensor types and get an estimate design of the resulting photosensor 
array at the click of a few buttons.
                          
In the pictures on the left we see 
[Xenoscope](https://www.physik.uzh.ch/en/groups/baudis/Research/Xenoscope.html), 
the 2.6 m-high DARWIN demonstrator built at the University of Zürich, and its
SiPM top array (both installed and during characterisation).


Picture credits: 
  * SiPM in Home page: F. Girard
  * PMTs in Home page: XENON collaboration
  * Xenoscope: LBG
  * SiPM array of Xenoscope: LBG
                          
ArrayMaker code and layout by [Ricardo Peres](https://ricmperes.github.io/). 
Available open-source on [GitHub](https://github.com/ricmperes/arraymaker).
''',
                          style={'margin-top': '2rem'})

layout = dbc.Container([
    navbar,
    dbc.Row([dbc.Col([picture_carousel
                      ], width={'offset': 1, 'size': 3}),
             dbc.Col([html.H1('About', style={'margin-top': '1rem',
                                              'text-align': 'center',
                                              }),
                      html.Hr(),
                      about_text], width={'offset': 1, 'size': 6}),
             ], style={'margin-top': '2rem',
                       'margin-bottom': '2rem',
                       'height': height_of_page}),
    footer
], fluid=True)
