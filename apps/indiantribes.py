from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Group, Format, Scheme
from dash import dash_table
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

from app import app
from apps.utils import *

# layout = html.Div([
#     html.H3('About Us'),
# ])

state_list = state_list['state_name'].sort_values()

ind_state_list = [{'label': 'India', 'value': 'India'}, {'label': '-----', 'value': '-----', 'disabled': True}]
for state in state_list:
    ind_state_list.append({'label': state, 'value': state})


def make_map(state, tribe):
    state_map = dbc.Card(
        [
            dbc.CardImg(src='/assets/maps/home/STIndia2011_125.png', top=True),
            dbc.CardBody(
                [
                    html.Label(
                        "Details of " + tribe + " in " + state)
                ], style={'margin': "auto", 'text-align': "center"},
            ),

        ],
        style={"width": "30rem", "text-align": "center", 'margin': "auto"},
    )
    return state_map


def get_ind_tribe_info(tribe):
    tribe_info = html.Div(
        [
            dbc.Button(
                "About " + tribe,
                id="tribe-ind-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("This contains information about " + tribe)),
                id="tribe-ind-collapse",
                is_open=False,
            ),
        ]
    )
    return tribe_info


def get_tribe_population_for_state(state):
    data = pd.read_json(fetch_data('tribes/population/' + get_state_code(state)))
    data_pop = pd.json_normalize(data['data'])
    int_cols = ['population']
    for col in int_cols:
        data_pop[col] = pd.to_numeric(data_pop[col], errors='coerce').fillna(0).astype('int')
    return data_pop


def get_tribe_demography_for_state(state):
    data = pd.read_json(fetch_data('tribes/demography/' + get_state_code(state)))
    data_pop = pd.json_normalize(data['data'])
    int_cols = ['population', 'literate', 'literacy_male', 'literacy_female', 'literacy', 'gender_ratio']
    for col in int_cols:
        data_pop[col] = pd.to_numeric(data_pop[col], errors='coerce').fillna(0).astype('int')
    return data_pop


# def get_tribe_distribution_in_state(state, tribe):
#     data = pd.read_json(
#         fetch_data('tribes/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
#     data_dist = pd.json_normalize(data['data'])
#     int_cols = ['district_code', 'population', 'state_code', 'tribe_code']
#     for col in int_cols:
#         data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0).astype('int')
#     return data_dist


def get_tribe_distribution_in_state(state, tribe):
    data = pd.read_json(
        fetch_data(
            'tribe-atlas/demography/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
    data_dist = pd.json_normalize(data['data'])
    int_cols = ['children', 'district_code', 'gender_ratio', 'population', 'state_code', 'tribe_code']
    float_cols = ['literacy']
    for col in int_cols:
        data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0).astype('int')
    for col in float_cols:
        data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0.00).astype('float')
    return data_dist


def get_tribe_distribution_across_religions_in_state(state, tribe):
    data = pd.read_json(fetch_data(
        'tribe-atlas/major-religion/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
    data_dist = pd.json_normalize(data['data'])
    int_cols = ['religion_code', 'population', 'state_code', 'tribe_code']
    for col in int_cols:
        data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0).astype('int')
    return data_dist


def get_tribe_distribution_across_orp_in_state(state, tribe):
    data = pd.read_json(fetch_data(
        'tribe-atlas/orp/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
    data_dist = pd.json_normalize(data['data'])
    if data_dist.empty:
        return data_dist
    int_cols = ['religion_code', 'population', 'state_code', 'tribe_code']
    for col in int_cols:
        data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0).astype('int')
    return data_dist


def get_tribe_list_for_state(state):
    data = pd.read_json(fetch_data('tribelist/' + get_state_code(state)))
    data_list = pd.json_normalize(data['data'])
    data_list = data_list.drop('state_name', axis=1)
    data_list = data_list.drop('state_code', axis=1)
    int_cols = ['tribe_code']
    for col in int_cols:
        data_list[col] = pd.to_numeric(data_list[col], errors='coerce').fillna(0).astype('int')
    return data_list


def get_tribe_code_from_name(state, name):
    data = get_tribe_list_for_state(state)
    tribe = data.loc[data['tribe_name'] == name]
    tribe_code = tribe['tribe_code'].iloc[0]
    # print(tribe_code)
    return tribe_code


#
# get_tribe_code_from_name('Rajasthan', 'Bhil Mina')


def make_state_tribe_population_table(state):
    tribe_state_list = get_tribe_population_for_state(state)
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='tribe_name', name='Tribe Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=tribe_state_list.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'tribe_name'},
                'textAlign': 'left'
            },
            # {
            #     'if': {'column_id': 'state_name'},
            #     'textAlign': 'left'
            # },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_state_tribe_literacy_table(state):
    tribe_state_list = get_tribe_demography_for_state(state)
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='tribe_name', name='Tribe Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='literate', name='Literate', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='literacy', name='Literacy', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_male', name='Male Literacy', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_female', name='Female Literacy', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=tribe_state_list.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'tribe_name'},
                'textAlign': 'left'
            },
            # {
            #     'if': {'column_id': 'state_name'},
            #     'textAlign': 'left'
            # },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_state_tribe_gender_ratio_table(state):
    tribe_state_list = get_tribe_demography_for_state(state)
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='tribe_name', name='Tribe Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='gender_ratio', name='Gender Ratio', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=tribe_state_list.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'tribe_name'},
                'textAlign': 'left'
            },
            # {
            #     'if': {'column_id': 'state_name'},
            #     'textAlign': 'left'
            # },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_state_tribe_distribution(state, tribe):
    tribe_state_list = get_tribe_distribution_in_state(state, tribe).sort_values('district_name')
    # tribe_code = get_tribe_code_from_name(state, tribe)
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='district_name', name='District Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='children', name='Children', type='numeric'),
        dict(id='gender_ratio', name='Gender Ratio', type='numeric'),
        dict(id='literacy', name='Literacy %', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=tribe_state_list.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'district_name'},
                'textAlign': 'left'
            },
            # {
            #     'if': {'column_id': 'state_name'},
            #     'textAlign': 'left'
            # },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_state_tribe_distribution_graph(state, tribe):
    tribe_state_list = get_tribe_distribution_in_state(state, tribe)
    if tribe_state_list.empty:
        return None
    tribe_state_list = tribe_state_list.sort_values('district_name', ascending=False)
    fig_all = go.Figure(layout=go.Layout(
        height=100 + (32 * len(tribe_state_list)),
        xaxis=dict(title='Population'),
        yaxis=dict(title='District Name'),
        title=dict(text=tribe + " population details for " + state)
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        y=tribe_state_list['district_name'],
        x=tribe_state_list['population'],
        name='Population',
        orientation='h',
        text=tribe_state_list['population']
    ))
    fig_all.update_layout(barmode='group')
    return fig_all


def make_state_tribe_distribution_across_religions(state, tribe):
    tribe_state_list = get_tribe_distribution_across_religions_in_state(state, tribe)
    tribe_state_list.sort_values('religion_code')
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='religion_name', name='Religion Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=tribe_state_list.sort_values('religion_code', ascending=True).to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'religion_name'},
                'textAlign': 'left'
            },
            # {
            #     'if': {'column_id': 'state_name'},
            #     'textAlign': 'left'
            # },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_state_tribe_distribution_across_religion_graph(state, tribe):
    tribe_state_list = get_tribe_distribution_across_religions_in_state(state, tribe)
    if tribe_state_list.empty:
        return None
    tribe_state_list = tribe_state_list.sort_values('population', ascending=True)
    fig_all = go.Figure(layout=go.Layout(
        # height=100 + (32 * len(tribe_state_list)),
        yaxis=dict(title='Population'),
        xaxis=dict(title='Religion Name'),
        title=dict(text=tribe + " population details for " + state)
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        x=tribe_state_list['religion_name'],
        y=tribe_state_list['population'],
        name='Population',
        # orientation='h',
        text=tribe_state_list['population']
    ))
    # fig_all.update_layout(barmode='group')
    return fig_all


def make_state_tribe_distribution_across_orp(state, tribe):
    tribe_state_list = get_tribe_distribution_across_orp_in_state(state, tribe)
    if tribe_state_list.empty:
        return dbc.Label("Requested data is not available.")
    tribe_state_list.sort_values('religion_name')
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='religion_name', name='Religion Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=tribe_state_list.sort_values('religion_name').to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'religion_name'},
                'textAlign': 'left'
            },
            # {
            #     'if': {'column_id': 'state_name'},
            #     'textAlign': 'left'
            # },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_state_tribe_distribution_across_orp_graph(state, tribe):
    tribe_state_list = get_tribe_distribution_across_orp_in_state(state, tribe)
    if tribe_state_list.empty:
        return None
    tribe_state_list = tribe_state_list.sort_values('population', ascending=True)
    fig_all = go.Figure(layout=go.Layout(
        # height=100 + (32 * len(tribe_state_list)),
        yaxis=dict(title='Population'),
        xaxis=dict(title='Religion Name'),
        title=dict(text=tribe + " population details for " + state)
    ))
    fig_all.update_layout(legend=dict(orientation='h'))

    fig_all.add_trace(go.Bar(
        x=tribe_state_list['religion_name'],
        y=tribe_state_list['population'],
        name='Population',
        # orientation='h',
        text=tribe_state_list['population']
    ))
    # fig_all.update_layout(barmode='group')
    return fig_all


tribe_dbi_list = ['Population', 'Literacy', 'Gender Ratio']
tribe_ind_dbi_list = ['Population', 'Literacy', 'Gender Ratio', 'Children per Hundred']

tribe_bdi_card = dbc.Card(
    [
        dbc.CardHeader("Basic Demographic Indicators"),
        dbc.CardBody(
            [
                html.P("Select one of the following basic demographic indicators", className="card-text"),
                dbc.RadioItems(
                    id='tribe-dbi-select',
                    options=[
                        {"label": name, "value": name} for name in tribe_dbi_list
                    ],
                    value='Population',
                    inline=True
                )
            ]
        )
    ]
)

tribe_ind_bdi_card = dbc.Card(
    [
        dbc.CardHeader("Basic Demographic Indicators"),
        dbc.CardBody(
            [
                html.P("Select one of the following basic demographic indicators", className="card-text"),
                dbc.RadioItems(
                    id='tribe-ind-dbi-select',
                    options=[
                        {"label": name, "value": name} for name in tribe_ind_dbi_list
                    ],
                    value='Population',
                    inline=True
                )
            ]
        )
    ]
)

tribe_ind_distribution_list = ['District', 'Major Religion', 'ORP']
tribe_ind_distribution_card = dbc.Card(
    [
        dbc.CardHeader("Distribution"),
        dbc.CardBody(
            [
                html.P("Select one of the following distributions", className="card-text"),
                dbc.RadioItems(
                    id='tribe-ind-distribution-select',
                    options=[
                        {"label": name, "value": name} for name in tribe_ind_distribution_list
                    ],
                    value='District',
                    inline=True
                )
            ]
        )
    ]
)

tribe_aoi_card = dbc.Card(
    [
        dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                html.P("Select Either India or one of the States or UTs", className="card-text"),
                # dbc.RadioItems(
                #     id='tribe-aoi-select',
                #     options=[
                #         {'label': 'All of India', 'value': 'India'},
                #         {'label': 'A State or UT', 'value': 'States'}
                #     ],
                #     value='India',
                #     inline=True,
                #     hidden=True,
                # ),

                dcc.Dropdown(
                    id='tribe-states-select',
                    options=ind_state_list,
                    placeholder='Select the States or UT you are interested.',
                    disabled=False
                ),

                # dcc.Dropdown(
                #     id='tribe-list-states-select',
                #     placeholder='Select the Tribe you are interested.',
                #     # value='None',
                #     disabled=True
                # ),
            ],
        )
    ],
)

tribe_ind_aoi_card = dbc.Card(
    [
        # dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                # html.P("Select Either India or one of the States or UTs", className="card-text"),
                html.P("Select one of the States or UTs and their district", className="card-text"),
                # dbc.RadioItems(
                #     id='tribe-ind-aoi-select',
                #     options=[
                #         {'label': 'All of India', 'value': 'India'},
                #         {'label': 'A State or UT', 'value': 'States'}
                #     ],
                #     value='India',
                #     inline=True
                # ),

                dcc.Dropdown(
                    id='tribe-ind-state-select',
                    options=[
                        {'label': name, 'value': name} for name in list(state_list)
                    ],
                    placeholder='Select the States or UT you are interested.',
                    disabled=False
                ),

                dcc.Dropdown(
                    id='tribe-ind-list-states-select',
                    placeholder='Select the Tribe you are interested.',
                    # value='None',
                    disabled=True
                ),
            ],
        )
    ],
)

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    html.Div(html.Img(src=app.get_asset_url('cps_logo.png'),
                      style={'margin': "auto", 'width': "100%", 'text-align': "center"}, )),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religious Profile", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Religions", href='/apps/orpreligions')),
            dbc.NavItem(dbc.NavLink("Tribe Atlas", active=True, href='/apps/indiantribes')),
            dbc.NavItem(dbc.NavLink("About Us", href='/apps/aboutus')),
            dbc.NavItem(dbc.NavLink("Contact Us", href='/apps/contactus')),
        ],
        # fixed="top",
        justified="true",
        style={'margin': "auto", 'width': "80%", 'text-align': "center"},
        pills=True
    ),
    html.Br(),
    html.H3('Tribe Atlas'),
    html.Br(),
    dbc.Tabs(id="tabs-tribes", children=[
        dbc.Tab(label='Individual Tribes', activeTabClassName="fw-bold", children=[
            # dbc.CardGroup(
            #     [
            #         tribe_ind_bdi_card,
            #     ],
            # ),
            dbc.CardGroup(
                [
                    tribe_ind_aoi_card
                ],
            ),
            # dbc.CardGroup(
            #     [
            #         tribe_ind_distribution_card,
            #     ],
            # ),
            html.Br(),
            html.Div(
                [
                    dbc.Button("Get Data", id='tribe-ind-viz-button', color="primary", n_clicks=0),
                ],
                className="d-grid gap-2",
            ),
            html.Br(),
            dcc.Loading(
                id="loading-5",
                type="circle",
                children=html.Div(id="loading-output-5", style={'display': 'none'}),
            ),
            html.Div(
                id='tribe-ind-info',
                children=[
                ],
            ),
            html.Br(),
            html.Div(
                id='tribe-ind-viz-map',
                children=[
                ],
            ),
            html.Br(),
            html.H4(
                id='tribe-ind-area-label1',
                children=[],
                style={'textAlign': 'center'}
            ),
            html.Br(),
            html.Div(
                id='tribe-ind-viz-table1',
                children=[
                ],
            ),
            html.Div(
                id='tribe-ind-viz-graph1',
                children=[
                ],
            ),
            html.Br(),
            html.H4(
                id='tribe-ind-area-label2',
                children=[],
                style={'textAlign': 'center'}
            ),
            html.Div(
                id='tribe-ind-viz-table2',
                children=[
                ],
            ),
            html.Div(
                id='tribe-ind-viz-graph2',
                children=[
                ],
            ),
            html.Br(),
            html.H4(
                id='tribe-ind-area-label3',
                children=[],
                style={'textAlign': 'center'}
            ),
            html.Div(
                id='tribe-ind-viz-table3',
                children=[
                ],
            ),
            html.Div(
                id='tribe-ind-viz-graph3',
                children=[
                ],
            ),
            html.Br(),
        ]),
        dbc.Tab(label='Summary', activeTabClassName="fw-bold", children=[
            dbc.CardGroup(
                [
                    tribe_bdi_card,
                    tribe_aoi_card
                ],
            ),
            html.Br(),
            html.Div(
                [
                    dbc.Button("Get Data", id='tribe-viz-button', color="primary", n_clicks=0),
                ],
                className="d-grid gap-2",
            ),
            html.Br(),
            dcc.Loading(
                id="loading-4",
                type="circle",
                children=html.Div(id="loading-output-4", style={'display': 'none'}),
            ),
            html.H4(
                id='tribe-area-label',
                children=[],
                style={'textAlign': 'center'}
            ),
            html.Br(),
            html.Div(
                id='tribe-viz-table',
                children=[
                ],
            ),
            html.Br(),
        ]),
    ]),
    html.Footer(
        children=[
            dbc.Label("Copyright © 2022. Centre for Policy Studies.")
        ],
        style={'textAlign': 'center'}
    ),
], style={'margin': "auto", 'width': "80%"}
)


# @app.callback(
#     Output("tribe-ind-state-select", "disabled"),
#     [Input("tribe-ind-aoi-select", "value")]
# )
# def update_aoi_states_select_status(selected):
#     if selected == 'India':
#         return True
#     else:
#         return False

@app.callback(
    Output("tribe-ind-collapse", "is_open"),
    [Input("tribe-ind-collapse-button", "n_clicks")],
    [State("tribe-ind-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("tribe-ind-list-states-select", "disabled"),
    Output("tribe-ind-list-states-select", "options"),
    [Input("tribe-ind-state-select", "value")]
)
def update_tribe_states_select_status(selected):
    if not selected:
        raise PreventUpdate
    if selected != 'None':
        tribes = get_tribe_list_for_state(selected)
        return False, [{'label': i, 'value': i} for i in (list(tribes['tribe_name']))]
    else:
        return True, None


@app.callback(
    [Output('tribe-viz-table', 'children'),
     Output('tribe-area-label', 'children'),
     Output("loading-output-4", "children")],
    [Input('tribe-viz-button', 'n_clicks'),
     State('tribe-dbi-select', 'value'),
     # State('tribe-aoi-select', 'value'),
     State('tribe-states-select', 'value'), ]
    # State('tribe-list-states-select', 'value')]
)
def get_tribe_data(n, dbi, states):
    # aoi = 'India'
    if states == 'India':
        aoi = 'India'
    else:
        aoi = ''
    if n == 0:
        return None, dbc.Label("Select Population and a State before getting data."), None
    if aoi != 'India':
        if dbi == 'Population':
            return make_state_tribe_population_table(states), dbc.Label(
                "State wise Tribe Population Data for " + states + " from 2011"), None
        elif dbi == 'Literacy':
            return make_state_tribe_literacy_table(states), dbc.Label(
                "State wise Tribe Literacy Data for " + states + " from 2011"), None
        elif dbi == 'Gender Ratio':
            return make_state_tribe_gender_ratio_table(states), dbc.Label(
                "State wise Gender Ratio Data for " + states + " from 2011"), None
    else:
        return None, dbc.Label("Select a demographic indicator and a State before getting data."), None
    return None, None, None


@app.callback(
    [Output('tribe-ind-info', 'children'),
     Output('tribe-ind-viz-table1', 'children'),
     Output('tribe-ind-viz-graph1', 'children'),
     Output('tribe-ind-area-label1', 'children'),
     Output('tribe-ind-viz-table2', 'children'),
     Output('tribe-ind-viz-graph2', 'children'),
     Output('tribe-ind-area-label2', 'children'),
     Output('tribe-ind-viz-table3', 'children'),
     Output('tribe-ind-viz-graph3', 'children'),
     Output('tribe-ind-area-label3', 'children'),
     Output('tribe-ind-viz-map', 'children'),
     Output("loading-output-5", "children")],
    [Input('tribe-ind-viz-button', 'n_clicks'),
     # State('tribe-ind-dbi-select', 'value'),
     # State('tribe-ind-aoi-select', 'value'),
     State('tribe-ind-state-select', 'value'),
     State('tribe-ind-list-states-select', 'value')]
    # State('tribe-ind-distribution-select', 'value')]
)
def get_individual_tribe_data(n, states, tribe):
    if n == 0:
        return None, None, None, dbc.Label("Select a State and a Tribe before getting data."), None, None, None, None, None, None, None, None
    if tribe is None:
        return None, None, None, dbc.Label("Select a State and a Tribe before getting data."), None, None, None, None, None, None, None, None
    # if dbi == 'Population':
    #     if distrib == 'District':
    #         # fig_dist = make_state_tribe_distribution_graph(states, tribe)
    #         # if fig_dist is not None:
    #         #     district_visualization = dcc.Graph(
    #         #         id='graph',
    #         #         figure=fig_dist
    #         #     )
    #         # else:
    #         district_visualization = None
    #         # print(states + " : " + tribe)
    #         # print(get_state_code(states))
    #         # print(get_tribe_code_from_name(states, tribe))
    #         return make_state_tribe_distribution(states, tribe), dbc.Label(
    #             "State wise Tribe distribution for " + tribe + " in the state of " + states + " from 2011"), None
    #     elif distrib == 'Major Religion':
    #         # fig_religion = make_state_tribe_distribution_across_religion_graph(states, tribe)
    #         # if fig_religion is not None:
    #         #     district_visualization = dcc.Graph(
    #         #         id='graph',
    #         #         figure=fig_religion
    #         #     )
    #         # else:
    #         district_visualization = None
    #         return make_state_tribe_distribution_across_religions(states, tribe), dbc.Label(
    #             "State wise Tribe distribution across religions for " + tribe + " in the state of " + states + " from 2011"), None
    #     elif distrib == 'ORP':
    #         # fig_orp = make_state_tribe_distribution_across_orp_graph(states, tribe)
    #         # if fig_orp is not None:
    #         #     district_visualization = dcc.Graph(
    #         #         id='graph',
    #         #         figure=fig_orp
    #         #     )
    #         # else:
    #         district_visualization = None
    #         return make_state_tribe_distribution_across_orp(states, tribe), dbc.Label(
    #             "State wise Tribe distribution across ORP for " + tribe + " in the state of " + states + " from 2011"), None
    # else:
    #     return None, dbc.Label("Select a State and a Tribe before getting data."), None
    ind_info = get_ind_tribe_info(tribe)
    ind_table1 = make_state_tribe_distribution(states, tribe)
    ind_label1 = dbc.Label("District wise demography of " + tribe)
    ind_graph1 = None
    fig_dist = make_state_tribe_distribution_graph(states, tribe)
    if fig_dist is not None:
        ind_graph1 = dcc.Graph(
            id='graph',
            figure=fig_dist
        )
    ind_table2 = make_state_tribe_distribution_across_religions(states, tribe)
    ind_label2 = dbc.Label("Distribution of " + tribe + " among major religions")
    ind_graph2 = None
    fig_religion = make_state_tribe_distribution_across_religion_graph(states, tribe)
    if fig_religion is not None:
        ind_graph2 = dcc.Graph(
            id='graph',
            figure=fig_religion
        )
    ind_table3 = make_state_tribe_distribution_across_orp(states, tribe)
    ind_label3 = dbc.Label("Distribution of " + tribe + " among ORP")
    ind_graph3 = None
    fig_orp = make_state_tribe_distribution_across_orp_graph(states, tribe)
    if fig_orp is not None:
        ind_graph3 = dcc.Graph(
            id='graph',
            figure=fig_orp
        )
    ind_map = make_map(states, tribe)
    return ind_info, ind_table1, ind_graph1, ind_label1, ind_table2, ind_graph2, ind_label2, ind_table3, ind_graph3, ind_label3, ind_map, None
    # return make_state_tribe_distribution(states, tribe), dbc.Label(
    #             "State wise Tribe distribution for " + tribe + " in the state of " + states + " from 2011"), make_state_tribe_distribution_across_religions(states, tribe), dbc.Label(
    #             "State wise Tribe distribution across religions for " + tribe + " in the state of " + states + " from 2011"), make_state_tribe_distribution_across_orp(states, tribe), dbc.Label(
    #             "State wise Tribe distribution across ORP for " + tribe + " in the state of " + states + " from 2011"), None
