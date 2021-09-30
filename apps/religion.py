from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

# layout = html.Div([
#     html.H3('Religion'),
# ])

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", active=True, href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Religions", href='/apps/orpreligions')),
            dbc.NavItem(dbc.NavLink("Indian Tribes", href='/apps/indiantribes')),
            dbc.NavItem(dbc.NavLink("About Us", href='/apps/aboutus')),
            dbc.NavItem(dbc.NavLink("Contact Us", href='/apps/contactus')),
        ],
        # fixed="top",
        justified="true",
        style={'margin': "auto", 'width': "80%", 'text-align': "center"},
        pills=True
    ),
    html.Br(),
    html.H3('Religious Profile'),
    html.Br(),
    html.Strong('Religion Map:'),
    html.P('Map/Table of Total Population, ST Population, Hindu ST Population'),
    html.P('Similarly for all religion – Hindu, Christian, Muslim, Sikh, Jain, Buddhist, ORP'),
    html.Br(),html.Br(),
    html.Strong('Custom Table:'),
    html.P('Religious Distribution'),
    html.P('Total Population'),
    html.P('Total ST poulation'),
    html.P('Hindu, Christian, Muslim, Sikh, Jain, Buddhist, ORP')
    ], style={'margin': "auto", 'width': "80%"}
)