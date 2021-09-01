import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from app import app

df = pd.read_csv('./data/st_population_state_india_2011.csv')
state_list = sorted(df['State Name'])
st_df_country = df[['State Name', 'ST Population', 'State Population', 'ST Percentage']]
sorted_st_df_country = st_df_country.sort_values('State Name')
fig_country = px.bar(st_df_country.sort_values('State Name'), 'State Name', 'ST Percentage')

all_country_table = dbc.Table.from_dataframe(sorted_st_df_country, striped=True, bordered=True, hover=True)
df = pd.read_csv('./data/st_population_district_india_2011.csv')
st_df = df[['State Name', 'District Name', 'ST Population', 'District Population', 'ST Percentage']]
sorted_st_df = st_df.sort_values('State Name')
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

visualization_graph = dcc.Graph(
    id='graph',
    figure=fig_country
)


layout = html.Div(children=[

    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", active=True, href='/apps/demography')),
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
    html.H3('Demography information of Scheduled Tribes of India', style={'text-align': 'center'}),

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
    dbc.Button("Get Data", id='viz-button', color="primary", block=True, n_clicks=0),
    html.Br(),
    html.Br(),


    html.Br(),
    html.Div(
        id='demography-visualization',
        children=[
            html.Br(),
        ],  # style={'display': 'None'}
    ),

    html.Div(
        id='viz-table',
        children=[
            # all_country_table,
        ],
    ),

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


@app.callback(
    [Output('viz-table', 'children'),
     Output('demography-visualization', 'children')],
    [Input('viz-button', 'n_clicks'),
     Input('aoi-select', 'value'),
     Input('states-select', 'value'),
     Input('viz-selector', 'value')]
)
def get_partial_data(n, aoi, states, viz):
    if states is None:
        states = []
    if n == 0:
        return None, None
    elif aoi == 'India':
        if viz == 'graph':
            return all_country_table, visualization_graph
        else:
            return all_country_table, []
    else:
        # filtered_sorted_df_country = sorted_st_df_country[sorted_st_df_country['State Name'].isin(states)]
        # fig_filtered_country = px.bar(filtered_sorted_df_country.sort_values('State Name'), 'State Name',
        # 'ST Percentage') filtered_table = dbc.Table.from_dataframe(filtered_sorted_df_country, striped=True,
        # bordered=True, hover=True) filtered_visualization = dcc.Graph( id='graph', figure=fig_filtered_country )
        filtered_sorted_df_districts = sorted_st_df[sorted_st_df['State Name'].isin(states)]
        fig_filtered_state = px.bar(filtered_sorted_df_districts.sort_values('District Name'), x='District Name',
                                    y='ST Percentage', color='State Name')
        filtered_table = dbc.Table.from_dataframe(filtered_sorted_df_districts, striped=True, bordered=True, hover=True)
        filtered_visualization = dcc.Graph(
                                    id='graph',
                                    figure=fig_filtered_state
                                )
        if viz == 'graph':
            return filtered_table, filtered_visualization
        else:
            return filtered_table, []
