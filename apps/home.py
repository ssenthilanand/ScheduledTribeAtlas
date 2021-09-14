import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash_table
from dash_table.Format import Format, Scheme, Group, Align

from dash.dependencies import Input, Output

df = pd.read_csv('./data/st_population_state_india_2011.csv')
st_df_country = df[['State Name', 'ST Population', 'State Population', 'ST Percentage']]
sorted_st_df_country = st_df_country.sort_values('State Name')
# print(sorted_st_df_country.to_dict('records'))
# print(sorted_st_df_country)
fig = px.bar(sorted_st_df_country, 'State Name', 'ST Percentage')
india_st_population = df['ST Population'].sum()
india_total_population = df['State Population'].sum()
india_st_percentage = india_st_population / india_total_population * 100

# all_country_table = dbc.Table.from_dataframe(sorted_st_df_country, striped=True, bordered=True, hover=True)


columns = [
    dict(id='State Name', name='State Name'),
    dict(id='ST Population', name='ST Population', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='State Population', name='State Population', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='ST Percentage', name='ST Percentage', type='numeric',
         format=Format(precision=2, scheme=Scheme.fixed)),
]

# columns = [
#               dict(id='a', name='State Name'),
#               dict(id='a', name='ST Population', type='numeric'),
#               dict(id='a', name='State Population', type='numeric'),
#               dict(id='a', name='ST Percentage', type='numeric'),
#           ]

all_country_table = dash_table.DataTable(
    id='all_country_table',
    columns=columns,
    data=sorted_st_df_country.to_dict('records'),
    sort_action="native",
    sort_mode="single",
    column_selectable="single",
    style_as_list_view=True,
    style_cell_conditional=[
        {
            'if': {'column_id': 'State Name'},
            'textAlign': 'left'
        }
    ],
    style_header={
        'fontWeight': 'bold'
    },
)
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
                    html.Label(
                        f'Share of Scheduled Tribes population among India\'s overall population in 2011: {india_st_percentage:.2f}%')
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
                    html.Br(),
                    all_country_table,
                    dcc.Graph(
                        figure=fig
                    )
                ]
            )
        ]
    ),

], style={'margin': "auto", 'width': "80%"}
)
