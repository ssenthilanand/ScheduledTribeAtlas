from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

# layout = html.Div([
#     html.H3('About Us'),
# ])

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religious Profile", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Religions", active=True, href='/apps/orpreligions')),
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
    html.H3('ORP Religions'),
    html.Br(),
    html.Strong('ORP Religions:'),
    html.P('Population Distribution of ST-ORPs'),
    html.P('Table of ORPs sorted on descending population.'),
    html.P('Link to the ORP Distribution Table and Map.'),
    html.P('Map of the distribution of 20 major ORPs across India.'),
    ], style={'margin': "auto", 'width': "80%"}
)