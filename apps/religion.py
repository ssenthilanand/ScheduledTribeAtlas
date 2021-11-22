from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from apps.utils import *

# layout = html.Div([
#     html.H3('Religion'),
# ])

religions = ['All', 'Hindu', 'Muslim', 'Christian']
aoi_card = dbc.Card(
    [
        dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                html.P("Select Either India or one of the States or UTs", className="card-text"),
                dbc.RadioItems(
                    id='aoi-select',
                    options=[
                        {'label': 'All of India', 'value': 'India'},
                        {'label': 'A State or UT', 'value': 'States'}
                    ],
                    value='India',
                    inline=True
                ),

                dcc.Dropdown(
                    id='states-select',
                    options=[
                        {'label': name, 'value': name} for name in list(state_list['state_name'].sort_values())
                    ],
                    placeholder='Select the States or UT you are interested.',
                    disabled=True
                )
            ],
        )
    ],
)

rel_card = dbc.Card(
    [
        dbc.CardHeader("Religions"),
        dbc.CardBody(
            [
                html.P("Select one or more of the following religions", className="card-text"),
                dbc.RadioItems(
                    id='rel-select',
                    options=[
                        {"label": name, "value": name} for name in religions
                        # {'label': 'Population', 'value': 'Population'},
                        # {'label': 'Literacy', 'value': 'Literacy'},
                        # {'label': 'Gender Ratio', 'value': 'Gender Ratio'},
                        # {'label': 'Fertility Rate', 'value': 'Fertility Rate'},
                    ],
                    value='All',
                    inline=True
                )
            ]
        )
    ]
)

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
    dbc.CardGroup(
        [
            rel_card,
            aoi_card
        ],
    ),
    html.Br()
    # html.Strong('Religion Map:'),
    # html.P('Map/Table of Total Population, ST Population, Hindu ST Population'),
    # html.P('Similarly for all religion – Hindu, Christian, Muslim, Sikh, Jain, Buddhist, ORP'),
    # html.Br(),html.Br(),
    # html.Strong('Custom Table:'),
    # html.P('Religious Distribution'),
    # html.P('Total Population'),
    # html.P('Total ST poulation'),
    # html.P('Hindu, Christian, Muslim, Sikh, Jain, Buddhist, ORP')
    ], style={'margin': "auto", 'width': "80%"}
)