from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

# layout = html.Div([
#     html.H3('Contact Us'),
# ])

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    html.Div(html.Img(src=app.get_asset_url('cps_logo.png'),
                      style={'margin': "auto", 'width': "100%", 'text-align': "center"}, )),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Religions", href='/apps/orpreligions')),
            dbc.NavItem(dbc.NavLink("Indian Tribes", href='/apps/indiantribes')),
            dbc.NavItem(dbc.NavLink("About Us", href='/apps/aboutus')),
            dbc.NavItem(dbc.NavLink("Contact Us", active=True, href='/apps/contactus')),
        ],
        # fixed="top",
        justified="true",
        style={'margin': "auto", 'width': "80%", 'text-align': "center"},
        pills=True
    ),
    html.Br(),
    html.H3('Contact Us'),
    ], style={'margin': "auto", 'width': "80%"}
)