import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from app import app

# layout = html.Div([
#     html.H3('Demography'),
# ])

df = pd.read_csv('data/st_population_state_india_2011.csv')
state_list = sorted(df['State Name'])
# st_df_country = df[['State Name', 'ST Population', 'State Population', 'ST Percentage']]
# fig_country = px.bar(st_df_country.sort_values('State Name'), 'State Name', 'ST Percentage')


df = pd.read_csv('data/st_population_district_india_2011.csv')
st_df = df[['State Name', 'District Name', 'ST Population', 'District Population', 'ST Percentage']]
fig_state = px.bar(st_df, 'District Name', 'ST Percentage')

dbi_list = ['Population', 'Literacy', 'Gender Ratio', 'Fertility Rate']

aoi_card = dbc.Card(
    [
        dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                html.P("Select Either India or one or more States or UTs", className="card-text"),
                dbc.RadioItems(
                    id='aoi-select',
                    options=[
                        {'label': 'All of India', 'value': 'India'},
                        {'label': 'One or more States', 'value': 'States'}
                    ],
                    value='India',
                    inline=True
                ),

                dcc.Dropdown(
                    id='states-select',
                    options=[
                        {'label': name, 'value': name} for name in state_list
                    ],
                    placeholder='Select the states or UTs you are interested.',
                    multi=True,
                    disabled=True
                )
            ],
        )
    ]
)

bdi_card = dbc.Card(
    [
        dbc.CardHeader("Basic Demographic Indicators"),
        dbc.CardBody(
            [
                # html.H5("Basic Demographic Indicators", className="card-subtitle"),
                # html.Br(),
                html.P("Select one or more of the following basic demographic indicators", className="card-text"),
                dbc.Checklist(
                    id='dbi-checklist',
                    options=[
                        {"label": name, "value": name} for name in dbi_list
                    ],
                    value=['Population'],
                    inline=True
                )
            ]
        )
    ]
)

cat_card = dbc.Card(
    [
        dbc.CardHeader("Category"),
        dbc.CardBody(
            [
                # html.H5("Category", className="card-subtitle"),
                # html.Br(),
                dbc.RadioItems(
                    id='cat-st-selector',
                    options=[
                        {'label': 'Scheduled Tribe', 'value': 'ST'},
                    ],
                    value='ST',
                ),
                html.Br(),
                html.P("Select any other optional category of the population", className="card-text"),
                dbc.Checklist(
                    id='cat-selector',
                    options=[
                        {'label': 'Scheduled Caste', "value": 'SC'},
                        {'label': 'General', 'value': 'gen'},
                        {'label': 'Total', 'value': 'total'}
                    ],
                    inline=True
                )
            ]
        )
    ]
)

viz_card = dbc.Card(
    [
        dbc.CardHeader("Visualize"),
        dbc.CardBody(
            [
                # html.H5("Visualize", className="card-subtitle"),
                # html.Br(),
                dbc.RadioItems(
                    id='viz-table-selector',
                    options=[
                        {'label': 'Table', 'value': 'table'},
                    ],
                    value='table',
                ),
                html.Br(),
                html.P("Select any other optional type of visualization", className="card-text"),
                dbc.RadioItems(
                    id='viz-selector',
                    options=[
                        {'label': 'Graph', "value": 'graph'},
                        {'label': 'Map', 'value': 'map'},
                    ],
                )
            ]
        )
    ]
)
layout = html.Div(children=[

    # html.Title('An Atlas of Scheduled Tribes of India'),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", active=True, href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("About Us", href='/apps/aboutus')),
            dbc.NavItem(dbc.NavLink("Contact Us", href='/apps/contactus')),
        ],
        # fixed="top",
        justified="true",
        style={'margin': "auto", 'width': "80%", 'text-align': "center"},
        pills=True
    ),
    html.Br(),
    html.H3('Demography information of Scheduled Tribes of India', style={'text-align': 'center'}),

    # dbc.Row(
    #     [
    #         dbc.Col(aoi_card, width=6),
    #         dbc.Col(bdi_card, width=6)
    #     ],
    #     align='start'
    # ),
    # dbc.Row(
    #     [
    #         dbc.Col(cat_card, width=6),
    #         dbc.Col(viz_card, width=6)
    #     ],
    #     align='start'
    # ),
    # html.Label('Area of Interest'),

    dbc.CardDeck(
        [
            aoi_card, bdi_card
        ]
    ),
    dbc.CardDeck(
        [
            cat_card, viz_card
        ]
    ),
    html.Br(),
    html.Br(),
    dbc.Button("Get Data", color="primary", block=True),
    html.Br(),
    html.Br(),
    ], style={'margin': "auto", 'width': "80%"}
)


@app.callback(
    Output("states-select", "disabled"),
    [Input("aoi-select", "value")],
)
def update_states_select_status(selected):
    if selected == 'India':
        return True
    else:
        return False
