import dash
from dash import html
import dash_bootstrap_components as dbc

def make_navbar():
    return dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/arraymaker/")),
            dbc.NavItem(dbc.NavLink("Sensor types", href="/arraymaker/sensors")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("SiPM array", href="/arraymaker/sipmarray"),
                    dbc.DropdownMenuItem("PMT array", href="/arraymaker/pmtarray"),
                    ],
                nav=True,
                label="Build array",
                ),
            dbc.NavItem(dbc.NavLink("About", href="/arraymaker/about")),
        ],
        brand="ArrayMaker",
        brand_href="/arraymaker/",
        sticky="top",
        color="primary",
        dark=True,
        fluid=True
    )

def make_footer():
    return html.Footer(html.Small([
        'by Ricardo Peres for DARWIN/XLZD - 2024']), 
        style={'margin-top': '2rem', 'margin-bottom': '1rem',
               'background-color': '#95a5a6', 'color' : 'white',
               'text-align': 'center', 'padding': '0.3rem',
        })
            #    "position": "fixed",
            #     "bottom": "0","width": "100%",})