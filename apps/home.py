import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

df = pd.read_csv('./data/st_population_state_india_2011.csv')
st_df_country = df[['State Name', 'ST Population', 'State Population', 'ST Percentage']]
fig = px.bar(st_df_country.sort_values('State Name'), 'State Name', 'ST Percentage')
india_st_population = df['ST Population'].sum()
india_total_population = df['State Population'].sum()
india_st_percentage = india_st_population / india_total_population * 100

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", active=True, href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", href='/apps/religion')),
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
    html.H3(['An Atlas of Scheduled Tribes of India'], style={'text-align': 'center'}),
    html.Br(),

    dbc.Card(
        [
            dbc.CardImg(src='/assets/ST2011.png', top=True),
            dbc.CardBody(
                [
                    html.Label(f'Share of Scheduled Tribes population among India\'s overall population in 2011: {india_st_percentage:.2f}%')
                ], style={'margin': "auto", 'text-align': "center"},
            )
        ]
    ),

    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(
                        ['State wide Scheduled Tribe population percentage in 2011'],
                        style={'text-align': 'center'}
                    ),
                    dcc.Graph(
                        figure=fig
                    )
                ]
            )
        ]
    ),

    ], style={'margin': "auto", 'width': "80%"}
)
