from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group, Format
from dash.dependencies import Input, Output, State
from dash import dash_table
import plotly.graph_objects as go

from app import app
from apps.utils import *


# layout = html.Div([
#     html.H3('About Us'),
# ])


def get_orp_religions_list():
    data = pd.read_json(fetch_data('orp/'))
    data_orp = pd.json_normalize(data['data'])
    data_orp['total'] = pd.to_numeric(data_orp['total'], errors='coerce').fillna(0).astype('int')
    return data_orp


orp_list = get_orp_religions_list().sort_values('religion_name')


def get_orp_all_states():
    data = pd.read_json(fetch_data('orp/state/'))
    data_orp = pd.json_normalize(data['data'])
    int_cols = ['religion_code', 'state_code', 'total']
    for col in int_cols:
        data_orp[col] = pd.to_numeric(data_orp[col], errors='coerce').fillna(0).astype('int')
    return data_orp


orp_all_state_list = get_orp_all_states().sort_values('state_name')


def make_all_india_orp_table():
    columns = [
        dict(id='religion_code', name='Religion Code'),  # , type='numeric',
        # format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='religion_name', name='Religion Name'),
        dict(id='total', name='Total', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=orp_list.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'religion_name'},
                'textAlign': 'left'
            },
            {
                'if': {'column_id': 'religion_code'},
                'textAlign': 'left'
            },
        ],
        style_header={
            'fontWeight': 'bold'
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


def make_all_state_orp_table():
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='religion_code', name='ORP Code'),  # , type='numeric',
        # format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='religion_name', name='ORP Name'),
        dict(id='total', name='Total', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=orp_all_state_list.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': 'religion_name'},
                'textAlign': 'left'
            },
            {
                'if': {'column_id': 'religion_code'},
                'textAlign': 'left'
            },
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


orp_card = dbc.Card(
    [
        dbc.CardHeader("ORP"),
        dbc.CardBody(
            [
                html.P("Select either All or one of the ORP from the list", className="card-text"),
                dbc.RadioItems(
                    id='orp-val-select',
                    options=[
                        {'label': 'All ORP', 'value': 'all'},
                        {'label': 'Select from list', 'value': 'selection'}
                    ],
                    value='all',
                    inline=True
                ),

                dcc.Dropdown(
                    id='orp-select',
                    options=[
                        {'label': name, 'value': name} for name in list(orp_list['religion_name'].sort_values())
                    ],
                    placeholder='Select the name of ORP you are interested.',
                    disabled=True,
                    value="All"
                )
            ],
        )
    ],
)

aoi_card = dbc.Card(
    [
        dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                html.P("Select Either India or one of the States or UTs", className="card-text"),
                dbc.RadioItems(
                    id='orp-aoi-select',
                    options=[
                        {'label': 'All of India', 'value': 'India'},
                        {'label': 'A State or UT', 'value': 'States'}
                    ],
                    value='India',
                    inline=True
                ),

                dcc.Dropdown(
                    id='orp-states-select',
                    options=[
                        {'label': name, 'value': name} for name in list(state_list['state_name'].sort_values())
                    ],
                    placeholder='Select the District you are interested.',
                    disabled=True,
                    value=None
                ),

                dcc.Dropdown(
                    id='orp-districts-select',
                    options=[
                        {'label': name, 'value': name} for name in list(districts_list['district_name'].sort_values())
                    ],
                    placeholder='Select the States or UT you are interested.',
                    disabled=True,
                    value=None
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
            dbc.NavItem(dbc.NavLink("Religion", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Religions", active=True, href='/apps/orpreligions')),
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
    html.H3('ORP Religions'),
    html.Br(),
    dbc.CardGroup(
        [
            orp_card,
            aoi_card
        ],
    ),
    html.Br(),
    html.Div(
        [
            dbc.Button("Get Data", id='orp-viz-button', color="primary", n_clicks=0),
        ],
        className="d-grid gap-2",
    ),
    html.Br(),
    dcc.Loading(
        id="loading-3",
        type="circle",
        children=html.Div(id="loading-output-3", style={'display': 'none'}),
    ),
    html.Br(),
    html.H4(
        id='orp-area-label',
        children=[],
        style={'textAlign': 'center'}
    ),
    html.Br(),
    html.Div(
        id='orp-viz-table',
        children=[
        ],
    ),
    html.Br(),
], style={'margin': "auto", 'width': "80%"}
)


@app.callback(
    Output("orp-select", "disabled"),
    [Input("orp-val-select", "value")],
)
def update_religion_states_select_status(selected):
    if selected == 'all':
        return True
    else:
        return False


@app.callback(
    Output("orp-states-select", "disabled"),
    [Input("orp-aoi-select", "value")]
)
def update_aoi_states_select_status(selected):
    if selected == 'India':
        return True
    else:
        return False


@app.callback(
    Output("orp-districts-select", "disabled"),
    [Input("orp-states-select", "value")]
)
def update_religion_districts_select_status(selected):
    if selected is None:
        return True
    else:
        return False


@app.callback(
    [Output('orp-viz-table', 'children'),
     Output('orp-area-label', 'children'),
     Output("loading-output-3", "children")],
    [Input('orp-viz-button', 'n_clicks'),
     State('orp-select', 'value'),
     State('orp-aoi-select', 'value'),
     State('orp-states-select', 'value')]
)
def get_orp_data(n, orp, aoi, states):
    if n == 0:
        return make_all_india_orp_table(), dbc.Label("ORP Data for India from 2011"), None
    if orp == 'All' and aoi == 'India':
        return make_all_state_orp_table(), dbc.Label("State wise ORP Data for India from 2011"), None
    return make_all_india_orp_table(), dbc.Label("ORP Data for India from 2011"), None
