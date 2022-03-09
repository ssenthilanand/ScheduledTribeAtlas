from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.dash_table.Format import Group, Format, Scheme
from dash import dash_table

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


tribe_dbi_list = ['Population', 'Literacy', 'Gender Ratio']

tribe_bdi_card = dbc.Card(
    [
        dbc.CardHeader("Basic Demographic Indicators"),
        dbc.CardBody(
            [
                html.P("Select one or more of the following basic demographic indicators", className="card-text"),
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
                )
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
    [Output('tribe-viz-table', 'children'),
     Output('tribe-area-label', 'children'),
     Output("loading-output-4", "children")],
    [Input('tribe-viz-button', 'n_clicks'),
     State('tribe-dbi-select', 'value'),
     State('tribe-aoi-select', 'value'),
     State('tribe-states-select', 'value')]
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
    else:
        return None, dbc.Label("Select Population or Literacy and a State before getting data."), None
    return None, None, None
