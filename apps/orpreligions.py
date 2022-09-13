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

def get_ind_orp_info(orp):
    orp_info = html.Div(
        [
            dbc.Button(
                "About " + orp,
                id="orp-ind-collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody("This contains information about " + orp)),
                id="orp-ind-collapse",
                is_open=False,
            ),
        ]
    )
    return orp_info


def get_orp_religions_list():
    data = pd.read_json(fetch_data('orp/'))
    data_orp = pd.json_normalize(data['data'])
    data_orp['total'] = pd.to_numeric(data_orp['total'], errors='coerce').fillna(0).astype('int')
    return data_orp


orp_list = get_orp_religions_list().sort_values('religion_name')


def get_orp_code_from_name(name):
    data = get_orp_religions_list()
    orp = data.loc[data['religion_name'] == name]
    orp_code = orp['religion_code'].iloc[0]
    # print(orp_code)
    return orp_code


def get_orp_all_states():
    data = pd.read_json(fetch_data('orp/state/'))
    data_orp = pd.json_normalize(data['data'])
    int_cols = ['religion_code', 'state_code', 'total']
    for col in int_cols:
        data_orp[col] = pd.to_numeric(data_orp[col], errors='coerce').fillna(0).astype('int')
    return data_orp


orp_all_state_list = get_orp_all_states().sort_values('state_name')


def get_orp_for_state(state):
    data = pd.read_json(fetch_data('orp/state/' + get_state_code(state)))
    data_orp = pd.json_normalize(data['data'])
    int_cols = ['religion_code', 'state_code', 'total']
    for col in int_cols:
        data_orp[col] = pd.to_numeric(data_orp[col], errors='coerce').fillna(0).astype('int')
    return data_orp


def get_orp_distribution_across_states(orp):
    data = pd.read_json(fetch_data('orp-atlas/states/' + get_orp_code_from_name(orp)))
    data_orp = pd.json_normalize(data['data'])
    int_cols = ['religion_code', 'state_code', 'sum(t1.population)']
    for col in int_cols:
        data_orp[col] = pd.to_numeric(data_orp[col], errors='coerce').fillna(0).astype('int')
    return data_orp


def get_orp_distribution_across_tribes(orp):
    data = pd.read_json(fetch_data('orp-atlas/tribes/' + get_orp_code_from_name(orp)))
    data_orp = pd.json_normalize(data['data'])
    int_cols = ['population','religion_code', 'state_code', 'tribe_code']
    for col in int_cols:
        data_orp[col] = pd.to_numeric(data_orp[col], errors='coerce').fillna(0).astype('int')
    return data_orp


def make_state_orp_table(orp):
    orp_state_list = get_orp_distribution_across_states(orp)
    orp_state_list = orp_state_list.sort_values('state_name')
    columns = [
        # dict(id='religion_code', name='Religion Code'),  # , type='numeric',
        # format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='state_name', name='State Name'),
        dict(id='sum(t1.population)', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=orp_state_list.to_dict('records'),
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


def make_state_orp_graph(orp):
    orp_state_list = get_orp_distribution_across_states(orp)
    orp_state_list = orp_state_list.sort_values('state_name')
    if orp_state_list.empty:
        return None
    fig_all = go.Figure(layout=go.Layout(
        # height=100 + (32 * len(orp_state_list)),
        yaxis=dict(title='Population'),
        xaxis=dict(title='State Name'),
        title=dict(text=orp + " population across states")
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        x=orp_state_list['state_name'],
        y=orp_state_list['sum(t1.population)'],
        name='Population',
        # orientation='h',
        text=orp_state_list['sum(t1.population)']
    ))
    fig_all.update_layout(barmode='group')
    return fig_all


def make_state_tribe_orp_graph(orp):
    orp_state_tribe_list = get_orp_distribution_across_tribes(orp)
    orp_state_tribe_list = orp_state_tribe_list.sort_values('state_name')
    if orp_state_tribe_list.empty:
        return None
    fig_all = go.Figure(layout=go.Layout(
        # height=100 + (32 * len(orp_state_tribe_list)),
        yaxis=dict(title='Population'),
        xaxis=dict(title='Tribe Name'),
        title=dict(text=orp + " population across tribes")
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        x=orp_state_tribe_list['tribe_name'],
        y=orp_state_tribe_list['population'],
        name='Population',
        # orientation='h',
        text=orp_state_tribe_list['population']
    ))
    fig_all.update_layout(barmode='group')
    return fig_all


def make_state_orp_tribe_table(orp):
    orp_state_tribe_list = get_orp_distribution_across_tribes(orp)
    orp_state_tribe_list = orp_state_tribe_list.sort_values('state_name')
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='tribe_name', name='Tribe Name'),  # , type='numeric',
        # format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='religion_name', name='ORP Name'),
        dict(id='population', name='Population', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        data=orp_state_tribe_list.to_dict('records'),
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
                'if': {'column_id': 'tribe_name'},
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
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        css=[{"selector": ".show-hide", "rule": "display: none"}]
    )
    return all_country_table


orp_card = dbc.Card(
    [
        # dbc.CardHeader("ORP"),
        dbc.CardBody(
            [
                html.P("Select one of the ORP from the list", className="card-text"),
                # dbc.RadioItems(
                #     id='orp-val-select',
                #     options=[
                #         {'label': 'All ORP', 'value': 'all'},
                #         {'label': 'Select from list', 'value': 'selection'}
                #     ],
                #     value='all',
                #     inline=True
                # ),

                dcc.Dropdown(
                    id='orp-select',
                    options=[
                        {'label': name, 'value': name} for name in list(orp_list['religion_name'].sort_values())
                    ],
                    placeholder='Select the name of ORP you are interested.',
                    # disabled=True,
                    value="All"
                )
            ],
        )
    ],
)

# aoi_card = dbc.Card(
#     [
#         dbc.CardHeader("Areas of Interest"),
#         dbc.CardBody(
#             [
#                 html.P("Select Either India or one of the States or UTs", className="card-text"),
#                 dbc.RadioItems(
#                     id='orp-aoi-select',
#                     options=[
#                         {'label': 'All of India', 'value': 'India'},
#                         {'label': 'A State or UT', 'value': 'States'}
#                     ],
#                     value='India',
#                     inline=True
#                 ),
#
#                 # dbc.Card(
#                 #     dbc.CardHeader("State and District"),
#                 #     dbc.CardBody([
#                 #         dbc.Label("Testing Nested cards")
#                 #         ]
#                 #     ),
#                 # ),
#                 dcc.Dropdown(
#                     id='orp-states-select',
#                     options=[
#                         {'label': name, 'value': name} for name in list(state_list['state_name'].sort_values())
#                     ],
#                     placeholder='Select the District you are interested.',
#                     disabled=True,
#                     value=None
#                 ),
#
#                 dcc.Dropdown(
#                     id='orp-districts-select',
#                     options=[
#                         {'label': name, 'value': name} for name in list(districts_list['district_name'].sort_values())
#                     ],
#                     placeholder='Select the States or UT you are interested.',
#                     disabled=True,
#                     value=None
#                 ),
#             ],
#         )
#     ],
# )

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    html.Div(html.Img(src=app.get_asset_url('cps_logo.png'),
                      style={'margin': "auto", 'width': "100%", 'text-align': "center"}, )),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Atlas", active=True, href='/apps/orpreligions')),
            dbc.NavItem(dbc.NavLink("Tribe Atlas", href='/apps/indiantribes')),
            dbc.NavItem(dbc.NavLink("About Us", href='/apps/aboutus')),
            dbc.NavItem(dbc.NavLink("Contact Us", href='/apps/contactus')),
        ],
        # fixed="top",
        justified="true",
        style={'margin': "auto", 'width': "80%", 'text-align': "center"},
        pills=True
    ),
    html.Br(),
    html.H3('ORP Atlas'),
    html.Br(),
    dbc.CardGroup(
        [
            orp_card,
            # aoi_card
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
    html.Div(
        id='orp-ind-info',
        children=[
        ],
    ),
    html.Br(),
    html.H4(
        id='orp-area-label1',
        children=[],
        style={'textAlign': 'center'}
    ),
    html.Br(),
    html.Div(
        id='orp-viz-table1',
        children=[
        ],
    ),
    html.Br(),
    html.Div(
        id='orp-viz-graph1',
        children=[
        ],
    ),
    html.Br(),
    html.Br(),
    html.H4(
        id='orp-area-label2',
        children=[],
        style={'textAlign': 'center'}
    ),
    html.Br(),
    html.Div(
        id='orp-viz-table2',
        children=[
        ],
    ),
    html.Br(),
    html.Div(
        id='orp-viz-graph2',
        children=[
        ],
    ),
    html.Br(),
], style={'margin': "auto", 'width': "80%"}
)


# @app.callback(
#     Output("orp-select", "disabled"),
#     [Input("orp-val-select", "value")],
# )
# def update_religion_states_select_status(selected):
#     if selected == 'all':
#         return True
#     else:
#         return False


# @app.callback(
#     Output("orp-states-select", "disabled"),
#     Output("orp-districts-select", "disabled"),
#     [Input("orp-aoi-select", "value")]
# )
# def update_aoi_states_select_status(selected):
#     if selected == 'India':
#         return True, True
#     else:
#         return False, False


# @app.callback(
#     Output("orp-districts-select", "disabled"),
#     [Input("orp-states-select", "value"),
#      State("orp-states-select", "disabled")]
# )
# def update_religion_districts_select_status(selected, status):
#     if selected is None and status is True:
#         return True
#     else:
#         return False


@app.callback(
    Output("orp-ind-collapse", "is_open"),
    [Input("orp-ind-collapse-button", "n_clicks")],
    [State("orp-ind-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output('orp-ind-info', 'children'),
     Output('orp-viz-table1', 'children'),
     Output('orp-viz-graph1', 'children'),
     Output('orp-area-label1', 'children'),
     Output('orp-viz-table2', 'children'),
     Output('orp-viz-graph2', 'children'),
     Output('orp-area-label2', 'children'),
     Output("loading-output-3", "children")],
    [Input('orp-viz-button', 'n_clicks'),
     State('orp-select', 'value'), ]
    # State('orp-aoi-select', 'value'),
    # State('orp-states-select', 'value')]
)
def get_orp_data(n, orp):
    if n == 0:
        ind_label = dbc.Label("Select an ORP from the list and get data")
        return None, None, None, ind_label, None, None, None, None
    # if orp == 'All' and aoi == 'India':
    #     return ind_orp_info, make_all_state_orp_table(), dbc.Label("State wise ORP Data for India from 2011"), None
    # if orp == 'All' and aoi != 'India':
    #     return make_state_orp_table(states), dbc.Label("State wise ORP Data for " + states + " from 2011"), None
    else:
        ind_orp_info = get_ind_orp_info(orp)
        ind_table1 = make_state_orp_table(orp)
        ind_graph1 = None
        fig_dist = make_state_orp_graph(orp)
        if fig_dist is not None:
            ind_graph1 = dcc.Graph(
                id='graph',
                figure=fig_dist
            )
        ind_label1 = dbc.Label("Population distribution along states for " + orp)
        ind_table2 = make_state_orp_tribe_table(orp)
        ind_graph2 = None
        fig_tribe = make_state_tribe_orp_graph(orp)
        if fig_tribe is not None:
            ind_graph2 = dcc.Graph(
                id='graph',
                figure=fig_tribe
            )
        ind_label2 = dbc.Label("Population distribution among tribes for " + orp)
        return ind_orp_info, ind_table1, ind_graph1, ind_label1, ind_table2, ind_graph2, ind_label2, None
