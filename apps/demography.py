from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dash_table
from dash.dash_table.Format import Format, Scheme, Group, Align
import pandas as pd
# import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go


from app import app

import requests
from requests.exceptions import HTTPError

from apps.utils import *


def get_state_population_data():
    response = fetch_data('population')
    data = pd.read_json(response)
    data_population = pd.json_normalize(data['data'])
    dp = data_population[['district_name', 'state_name', 'population_gn', 'population_sc', 'population_st']]
    num_cols = ['population_gn', 'population_sc', 'population_st']
    for col in num_cols:
        dp[col] = pd.to_numeric(dp[col], errors='coerce').fillna(0).astype('int')

    dp['population_total'] = dp['population_gn'] + dp['population_sc'] + dp['population_st']

    dp_state = dp.drop('district_name', axis=1)
    dp_sg = dp_state.groupby('state_name', as_index=False)

    dp_sgf = dp_sg.sum()
    # dp_sgf['st_per'] = (dp_sgf['population_st'] / dp_sgf['population_total']) * 100
    # dp_sgf['sc_per'] = (dp_sgf['population_sc'] / dp_sgf['population_total']) * 100
    # dp_sgf['gn_per'] = (dp_sgf['population_gn'] / dp_sgf['population_total']) * 100
    return dp_sgf


def get_district_population_data():
    response = fetch_data('population')
    data = pd.read_json(response)
    data_population = pd.json_normalize(data['data'])
    dp = data_population[['district_name', 'state_name', 'population_gn', 'population_sc', 'population_st']]
    num_cols = ['population_gn', 'population_sc', 'population_st']
    for col in num_cols:
        dp[col] = pd.to_numeric(dp[col], errors='coerce').fillna(0).astype('int')

    dp['population_total'] = dp['population_gn'] + dp['population_sc'] + dp['population_st']
    return dp


state_population = get_state_population_data()
district_population = get_district_population_data()

state_list = fetch_states()
n_states = len(state_list)

districts_list = fetch_districts()
n_districts = len(districts_list)


def make_all_india_table():
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='population_total', name='State Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='population_st', name='ST Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='population_sc', name='SC Population', type='numeric', hideable=True,
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='population_gn', name='General Population', type='numeric', hideable=True,
             format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='population_total', name='State Population', type='numeric',
        #      format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='st_per', name='ST Percentage', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        hidden_columns=['population_sc, population_gn'],
        data=state_population.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'state_name'},
                'textAlign': 'left'
            },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_all_india_graph():
    state_population_d = state_population.sort_values('state_name', ascending=False)
    fig_all = go.Figure(layout=go.Layout(
        height=100 + (32 * n_states),
        xaxis_title='Population',
        yaxis_title='State',
        title_text="Population Details for India"
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        y=state_population_d['state_name'],
        x=state_population_d['population_st'],
        name='ST',
        orientation='h',
        width=0.6
        # text=sorted_all_df['ST %']
    ))
    fig_all.add_trace(go.Bar(
        y=state_population_d['state_name'],
        x=state_population_d['population_sc'],
        name='SC',
        orientation='h',
        width=0.6
        # visible='legendonly'
    ))
    fig_all.add_trace(go.Bar(
        y=state_population_d['state_name'],
        x=state_population_d['population_gn'],
        name='General',
        orientation='h',
        width=0.6
        # visible='legendonly'
    ))
    fig_all.update_layout(barmode='group')
    return fig_all


fig_india = make_all_india_graph()
# fig_all.update_layout(barmode='stack')
#
# fig_all.add_trace(go.Scatter(
#     y=sorted_all_df['State Name'],
#     x=sorted_all_df['State'],
#     name='Total',
#     orientation='h',
#     mode="markers",
#     # text=sorted_all_df['State'].apply(lambda x: '{0:1.2f}%'.format(x)),
# ))

# n_states = len(sorted_all_df['State Name'])
# fig_all_group = go.Figure(layout=go.Layout(
#     height=100 + (64 * n_states),
#     xaxis_title='Population',
#     yaxis_title='State',
#     title_text="Population Details for India"
# ))
# fig_all_group.add_trace(go.Bar(
#     y=sorted_all_df['State Name'],
#     x=sorted_all_df['ST'],
#     name='ST',
#     orientation='h',
#     text=sorted_all_df['ST %'].apply(lambda x: '{0:1.2f}%'.format(x)),
# ))
# fig_all_group.add_trace(go.Bar(
#     y=sorted_all_df['State Name'],
#     x=sorted_all_df['SC'],
#     name='SC',
#     orientation='h',
#     text=sorted_all_df['SC %'].apply(lambda x: '{0:1.2f}%'.format(x)),
#     visible='legendonly'
# ))
# fig_all_group.add_trace(go.Bar(
#     y=sorted_all_df['State Name'],
#     x=sorted_all_df['General'],
#     name='General',
#     orientation='h',
#     text=sorted_all_df['General %'].apply(lambda x: '{0:1.2f}%'.format(x)),
#     visible='legendonly'
# ))
# fig_all_group.add_trace(go.Bar(
#     y=sorted_all_df['State Name'],
#     x=sorted_all_df['State'],
#     name='Total',
#     orientation='h',
#     text="100 %",
#     visible='legendonly'
# ))
# fig_all_group.update_layout(barmode='group')
# # fig_all_group.update_layout(legend=dict(orientation='h'))
# fig_all_group.update_traces(textposition="outside")

# fig_all.update_traces(texttemplate='%{text:.2s}', textposition='outside')

dbi_list = ['Population', 'Literacy', 'Gender Ratio', 'Fertility Rate']

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
    ]
)

bdi_card = dbc.Card(
    [
        dbc.CardHeader("Basic Demographic Indicators"),
        dbc.CardBody(
            [
                html.P("Select one or more of the following basic demographic indicators", className="card-text"),
                dbc.RadioItems(
                    id='dbi-checklist',
                    options=[
                        {"label": name, "value": name} for name in dbi_list
                    ],
                    value='Population',
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
                        {'label': 'General', 'value': 'General'},
                        # {'label': 'Total', 'value': 'Total'}
                    ],
                    value=['ST'],
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
                dbc.Checklist(
                    id='viz-selector',
                    options=[
                        {'label': 'Graph', "value": 'graph'},
                        # {'label': 'Map', 'value': 'map'},
                    ],
                    value=['']
                )
            ]
        )
    ]
)

visualization_graph = dcc.Graph(
    id='graph',
    # figure=fig_country
    # figure=fig_all
    figure=fig_india,
)

# visualization_graph1 = dcc.Graph(
#     id='graph',
#     # figure=fig_country
#     figure=fig_all
#
# )
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
    html.Br(),

    dbc.CardDeck(
        [
            bdi_card, aoi_card
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
    # html.H4(
    #     id='area-label',
    #     children=[],
    # ),
    html.Br(),
    html.Div(
        id='demography-visualization',
        children=[
            html.Br(),
        ],  # style={'display': 'None'}
    ),
    # html.Div(
    #     id='demography-visualization1',
    #     children=[
    #         html.Br(),
    #     ],  # style={'display': 'None'}
    # ),
    html.Div(
        id='viz-table',
        children=[
            # all_country_table,
        ],
    ),
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


@app.callback(
    [Output('viz-table', 'children'),
     Output('demography-visualization', 'children')],
    # Output('demography-visualization1', 'children')],
    # Output('area-label', 'children')],
    [Input('viz-button', 'n_clicks'),
     Input('aoi-select', 'value'),
     Input('cat-selector', 'value'),
     Input('states-select', 'value'),
     Input('viz-selector', 'value')]
)
def get_partial_data(n, aoi, cats, states, viz):
    if states is None:
        states = ''
    if n == 0:
        return None, None
    elif aoi == 'India':
        if viz[-1] == 'graph':
            fig_india.for_each_trace(
                lambda trace: trace.update(visible=True) if trace.name in cats else (),
            )
            fig_india.for_each_trace(
                lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
            )

            return make_all_india_table(), visualization_graph
        else:
            return make_all_india_table(), []
    else:
        filtered_table = make_filtered_state_population_table(district_population[
                                                 district_population['state_name'] == states], states)

        filtered_visualization = dcc.Graph(
            id='graph',
            # figure=fig_filtered_state
            figure=make_filtered_state_population_graph(district_population[
                                                            district_population['state_name'] == states], states)
        )
        filtered_visualization.figure.for_each_trace(
            lambda trace: trace.update(visible=True) if trace.name in cats else (),
        )
        filtered_visualization.figure.for_each_trace(
            lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
        )

        if viz[-1] == 'graph':
            return filtered_table, filtered_visualization
        else:
            return filtered_table, []


def make_filtered_state_population_table(districts, states):
    districts = districts.sort_values('district_name')
    district_columns = [
        dict(id='district_name', name='District Name'),
        dict(id='population_total', name='State Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='population_st', name='ST Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='population_sc', name='SC Population', type='numeric', hideable=True,
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='population_gn', name='General Population', type='numeric', hideable=True,
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    filtered_state_table = dash_table.DataTable(
        id='all_country_table',
        columns=district_columns,
        hidden_columns=['population_sc, population_gn'],
        data=districts.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'district_name'},
                'textAlign': 'left'
            },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return filtered_state_table


def make_filtered_state_population_graph(districts, states):
    districts = districts.sort_values('district_name', ascending=False)
    n_district = len(districts['district_name'])

    fig_districts = go.Figure(layout=go.Layout(
        height=200 + (32 * n_district),
        xaxis_title='Population',
        yaxis_title='Districts',
        title_text="Population Details for " + states
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['district_name'],
        x=districts['population_st'],
        name='ST',
        orientation='h',
        text=districts['population_st'] # .apply(lambda x: '{0:1.2f}%'.format(x)),
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['district_name'],
        x=districts['population_sc'],
        name='SC',
        orientation='h',
        text=districts['population_sc'], # .apply(lambda x: '{0:1.2f}%'.format(x)),
        visible='legendonly'
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['district_name'],
        x=districts['population_gn'],
        name='General',
        orientation='h',
        text=districts['population_gn'], # .apply(lambda x: '{0:1.2f}%'.format(x)),
        visible='legendonly'
    ))
    fig_districts.update_layout(barmode='group')
    fig_districts.update_traces(textposition="outside")
    # fig_districts.add_trace(go.Scatter(
    #     y=districts['district_name'],
    #     x=districts['population_total'],
    #     name='Total',
    #     orientation='h',
    #     mode="markers",
    #     # text=sorted_all_df['State'].apply(lambda x: '{0:1.2f}%'.format(x)),
    # ))
    return fig_districts

