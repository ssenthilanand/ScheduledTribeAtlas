import dash_core_components as dcc
import dash_html_components as html
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
            dbc.NavItem(dbc.NavLink("ORP Religions", href='/apps/orpreligions')),
            dbc.NavItem(dbc.NavLink("Indian Tribes", active=True, href='/apps/indiantribes')),
            dbc.NavItem(dbc.NavLink("About Us", href='/apps/aboutus')),
            dbc.NavItem(dbc.NavLink("Contact Us", href='/apps/contactus')),
        ],
        # fixed="top",
        justified="true",
        style={'margin': "auto", 'width': "80%", 'text-align': "center"},
        pills=True
    ),
    html.Br(),
    html.H3('Indian Tribes'),
    html.Br(),
    html.Strong('Tribes of India'),
    html.P('Form to choose – indicator, state.'),
    html.P('Name of the Tribe, Total ST Population, Tribe Population'),
    html.P('Bar Graph of Population of Individual STs'),
    html.Strong('Individual Tribes:'),
    html.P('Clicking on the individual Tribe'),
    html.P('Distribution of this tribe across the districts'),
    html.P('Bar chart of this distribution'),
    html.Br(),
    html.P('Similar distribution for scheduled tribes for other Indicators'),
    html.Li('Literacy'),
    html.Li('Children per 100'),
    html.Li('Comparative Fertility'),
    html.Li('Comparative Literacy Male/Female/Total'),
    html.Li('Graduates per 1000'),
    html.Li('Fertility'),
    html.Br(),
    ], style={'margin': "auto", 'width': "80%"}
)