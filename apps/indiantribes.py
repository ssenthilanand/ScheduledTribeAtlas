from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Group, Format, Scheme
from dash import dash_table
from dash.exceptions import PreventUpdate

from app import app
from apps.utils import *


# layout = html.Div([
#     html.H3('About Us'),
# ])


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


def get_tribe_distribution_in_state(state, tribe):
    data = pd.read_json(
        fetch_data('tribes/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
    data_dist = pd.json_normalize(data['data'])
    int_cols = ['district_code', 'population', 'state_code', 'tribe_code']
    for col in int_cols:
        data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0).astype('int')
    return data_dist


def get_tribe_distribution_across_religions_in_state(state, tribe):
    data = pd.read_json(fetch_data(
        'tribes/majorreligion/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
    data_dist = pd.json_normalize(data['data'])
    int_cols = ['religion_code', 'population', 'state_code', 'tribe_code']
    for col in int_cols:
        data_dist[col] = pd.to_numeric(data_dist[col], errors='coerce').fillna(0).astype('int')
    return data_dist


def get_tribe_distribution_across_orp_in_state(state, tribe):
    data = pd.read_json(fetch_data(
        'tribes/orpreligion/' + str(get_state_code(state)) + '/' + str(get_tribe_code_from_name(state, tribe))))
    data_dist = pd.json_normalize(data['data'])
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
    tribe_state_list = get_tribe_distribution_in_state(state, tribe)
    tribe_code = get_tribe_code_from_name(state, tribe)
    columns = [
        # dict(id='state_name', name='State Name'),
        dict(id='district_name', name='District Name'),
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


def make_state_tribe_distribution_across_religions(state, tribe):
    tribe_state_list = get_tribe_distribution_across_religions_in_state(state, tribe)
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


def make_state_tribe_distribution_across_orp(state, tribe):
    tribe_state_list = get_tribe_distribution_across_orp_in_state(state, tribe)
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
                dbc.RadioItems(
                    id='tribe-aoi-select',
                    options=[
                        {'label': 'All of India', 'value': 'India'},
                        {'label': 'A State or UT', 'value': 'States'}
                    ],
                    value='India',
                    inline=True
                ),

                dcc.Dropdown(
                    id='tribe-states-select',
                    options=[
                        {'label': name, 'value': name} for name in list(state_list['state_name'].sort_values())
                    ],
                    placeholder='Select the States or UT you are interested.',
                    disabled=True
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
        dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                # html.P("Select Either India or one of the States or UTs", className="card-text"),
                # dbc.RadioItems(
                #     id='tribe-aoi-select',
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
                        {'label': name, 'value': name} for name in list(state_list['state_name'].sort_values())
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
    dbc.Tabs(id="tabs-tribes", children=[
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
        dbc.Tab(label='Individual Tribes', activeTabClassName="fw-bold", children=[
            dbc.CardGroup(
                [
                    tribe_ind_bdi_card,
                ],
            ),
            dbc.CardGroup(
                [
                    tribe_ind_aoi_card
                ],
            ),
            dbc.CardGroup(
                [
                    tribe_ind_distribution_card,
                ],
            ),
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
            html.H4(
                id='tribe-ind-area-label',
                children=[],
                style={'textAlign': 'center'}
            ),
            html.Br(),
            html.Div(
                id='tribe-ind-viz-table',
                children=[
                ],
            ),
            html.Br(),
        ]),
    ]),

], style={'margin': "auto", 'width': "80%"}
)


@app.callback(
    Output("tribe-states-select", "disabled"),
    [Input("tribe-aoi-select", "value")]
)
def update_aoi_states_select_status(selected):
    if selected == 'India':
        return True
    else:
        return False


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
        # print(get_tribe_code_from_name(selected))
        return False, [{'label': i, 'value': i} for i in (list(tribes['tribe_name']))]
    else:
        return True, None


@app.callback(
    [Output('tribe-viz-table', 'children'),
     Output('tribe-area-label', 'children'),
     Output("loading-output-4", "children")],
    [Input('tribe-viz-button', 'n_clicks'),
     State('tribe-dbi-select', 'value'),
     State('tribe-aoi-select', 'value'),
     State('tribe-states-select', 'value'), ]
    # State('tribe-list-states-select', 'value')]
)
def get_tribe_data(n, dbi, aoi, states):
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
    [Output('tribe-ind-viz-table', 'children'),
     Output('tribe-ind-area-label', 'children'),
     Output("loading-output-5", "children")],
    [Input('tribe-ind-viz-button', 'n_clicks'),
     State('tribe-ind-dbi-select', 'value'),
     # State('tribe-ind-aoi-select', 'value'),
     State('tribe-ind-state-select', 'value'),
     State('tribe-ind-list-states-select', 'value'),
     State('tribe-ind-distribution-select', 'value')]
)
def get_individual_tribe_data(n, dbi, states, tribe, distrib):
    if n == 0:
        return None, dbc.Label("Select a demographic indicator, State and a Tribe before getting data."), None
    if dbi == 'Population':
        if distrib == 'District':
            return make_state_tribe_distribution(states, tribe), dbc.Label(
                "State wise Tribe distribution for " + tribe + " in the state of " + states + " from 2011"), None
        elif distrib == 'Major Religion':
            return make_state_tribe_distribution_across_religions(states, tribe), dbc.Label(
                "State wise Tribe distribution across religions for " + tribe + " in the state of " + states + " from 2011"), None
        elif distrib == 'ORP':
            return make_state_tribe_distribution_across_orp(states, tribe), dbc.Label(
                "State wise Tribe distribution across ORP for " + tribe + " in the state of " + states + " from 2011"), None
    else:
        return None, dbc.Label("Select a demographic indicator, State and a Tribe before getting data."), None
    return None, None, None
