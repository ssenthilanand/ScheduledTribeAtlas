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
#     html.H3('Religion'),
# ])


def get_religious_demography_all():
    data = pd.read_json(religious_demo)
    data_reldem = pd.json_normalize(data['data'])
    int_cols = ['buddhists', 'christians', 'hindus', 'jains', 'muslims', 'orp', 'rns', 'sikhs', 'total']
    for col in int_cols:
        data_reldem[col] = pd.to_numeric(data_reldem[col], errors='coerce').fillna(0).astype('int')
    float_cols = ['%buddhists', '%christians', '%hindus', '%jains', '%muslims', '%orp', '%rns', '%sikhs']
    for col in float_cols:
        data_reldem[col] = pd.to_numeric(data_reldem[col], errors='coerce').fillna(0.00).astype('float')
        data_reldem[col] = 100 * data_reldem[col]
    return data_reldem


def get_religious_demography_state(state):
    data = fetch_rel_district_demo(state)
    int_cols = ['buddhists', 'christians', 'hindus', 'jains', 'muslims', 'orp', 'rns', 'sikhs', 'total']
    for col in int_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0).astype('int')
    float_cols = ['per_buddhists', 'per_christians', 'per_hindus', 'per_jains', 'per_muslims',
                  'per_orp', 'per_rns', 'per_sikhs']
    for col in float_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0.00).astype('float')
        data[col] = 100 * data[col]
    return data


religious_demography = get_religious_demography_all()
n_states = len(state_list)


def make_all_india_religious_demography_table():
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='total', name='State', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='buddhists', name='Buddhist', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='christians', name='Christian', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='hindus', name='Hindu', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='jains', name='Jain', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='muslims', name='Muslim', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='orp', name='ORP', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='rns', name='RNS', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='sikhs', name='Sikh', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        # hidden_columns=['population_sc, population_gn'],
        data=religious_demography.to_dict('records'),
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


def make_religious_demography_state_table(state):
    religious_demography_state = fetch_rel_district_demo(state)
    columns = [
        dict(id='district_name', name='District Name'),
        dict(id='total', name='State', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='buddhists', name='Buddhist', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='christians', name='Christian', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='hindus', name='Hindu', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='jains', name='Jain', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='muslims', name='Muslim', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='orp', name='ORP', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='rns', name='RNS', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
        dict(id='sikhs', name='Sikh', type='numeric',
             format=Format(group=Group.yes).groups([3, 2, 2])),
    ]
    state_table = dash_table.DataTable(
        id='rel_state_table',
        columns=columns,
        # hidden_columns=['population_sc, population_gn'],
        data=religious_demography_state.to_dict('records'),
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
    return state_table


def make_all_india_religious_demography_graph():
    religious_demography_d = religious_demography.sort_values('state_name', ascending=False)
    fig_all = go.Figure(layout=go.Layout(
        height=100 + (64 * n_states),
        xaxis=dict(title='ST Population %'),
        yaxis=dict(title='State'),
        title=dict(text="ST Religious Population Data for India")
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    # fig_all.add_trace(go.Bar(
    #     y=religious_demography_d['state_name'],
    #     x=religious_demography_d['total'],
    #     name='ST Population',
    #     orientation='h',
    # ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%buddhists'],
        name='Buddhist Population',
        orientation='h',
        text=religious_demography_d['buddhists']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%christians'],
        name='Christian Population',
        orientation='h',
        text=religious_demography_d['christians']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%hindus'],
        name='Hindu Population',
        orientation='h',
        text=religious_demography_d['hindus']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%jains'],
        name='Jain Population',
        orientation='h',
        text=religious_demography_d['jains']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%muslims'],
        name='Muslim Population',
        orientation='h',
        text=religious_demography_d['muslims']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%orp'],
        name='ORP Population',
        orientation='h',
        text=religious_demography_d['orp']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%rns'],
        name='RNS Population',
        orientation='h',
        text=religious_demography_d['rns']
    ))
    fig_all.add_trace(go.Bar(
        y=religious_demography_d['state_name'],
        x=religious_demography_d['%sikhs'],
        name='Sikh Population',
        orientation='h',
        text=religious_demography_d['sikhs']
    ))
    fig_all.update_layout(barmode='group')
    return fig_all


religions = ['All', 'Hindus', 'Muslims', 'Christians']
aoi_card = dbc.Card(
    [
        dbc.CardHeader("Areas of Interest"),
        dbc.CardBody(
            [
                html.P("Select Either India or one of the States or UTs", className="card-text"),
                dbc.RadioItems(
                    id='rel-aoi-select',
                    options=[
                        {'label': 'All of India', 'value': 'India'},
                        {'label': 'A State or UT', 'value': 'States'}
                    ],
                    value='India',
                    inline=True
                ),

                dcc.Dropdown(
                    id='rel-states-select',
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

rel_card = dbc.Card(
    [
        dbc.CardHeader("Religions"),
        dbc.CardBody(
            [
                html.P("Select one or more of the following religions", className="card-text"),
                dbc.RadioItems(
                    id='rel-select',
                    options=[
                        {"label": name, "value": name} for name in religions
                        # {'label': 'Population', 'value': 'Population'},
                        # {'label': 'Literacy', 'value': 'Literacy'},
                        # {'label': 'Gender Ratio', 'value': 'Gender Ratio'},
                        # {'label': 'Fertility Rate', 'value': 'Fertility Rate'},
                    ],
                    value='All',
                    inline=True
                )
            ]
        )
    ]
)

layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", active=True, href='/apps/religion')),
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
    html.H3('Religious Profile'),
    html.Br(),
    dbc.CardGroup(
        [
            rel_card,
            aoi_card
        ],
    ),
    html.Br(),
    html.Div(
        [
            dbc.Button("Get Data", id='rel-viz-button', color="primary", n_clicks=0),
        ],
        className="d-grid gap-2",
    ),
    html.Br(),
    dcc.Loading(
        id="loading-2",
        type="circle",
        children=html.Div(id="loading-output-2", style={'display': 'none'}),
    ),
    html.H4(
        id='rel-area-label',
        children=[],
        style={'textAlign': 'center'}
    ),
    html.Br(),
    # html.H4("ST Religious Population Data for India from 2011"),
    html.Div(
        id='rel-viz-table',
        children=[
            # make_all_india_religious_demography_table(),
        ],
    ),
    html.Br(),
    html.Div(
        id='religion-visualization',
        children=[
            # dcc.Graph(
            #     id='graph',
            #     # figure=make_all_india_religious_demography_graph()
            # )

        ],  # style={'display': 'None'}
    ),

    # html.Strong('Religion Map:'),
    # html.P('Map/Table of Total Population, ST Population, Hindu ST Population'),
    # html.P('Similarly for all religion – Hindu, Christian, Muslim, Sikh, Jain, Buddhist, ORP'),
    # html.Br(),html.Br(),
    # html.Strong('Custom Table:'),
    # html.P('Religious Distribution'),
    # html.P('Total Population'),
    # html.P('Total ST poulation'),
    # html.P('Hindu, Christian, Muslim, Sikh, Jain, Buddhist, ORP')
], style={'margin': "auto", 'width': "80%"}
)


@app.callback(
    Output("rel-states-select", "disabled"),
    [Input("rel-aoi-select", "value")],
)
def update_religion_states_select_status(selected):
    if selected == 'India':
        return True
    else:
        return False


@app.callback(
    [Output('rel-viz-table', 'children'),
     Output('religion-visualization', 'children'),
     # Output('demography-visualization1', 'children')],
     Output('rel-area-label', 'children'),
     Output("loading-output-2", "children")],
    [Input('rel-viz-button', 'n_clicks'),
     State('rel-select', 'value'),
     State('rel-aoi-select', 'value'),
     State('rel-states-select', 'value')]
)
def get_religions_data(n, rel, aoi, states):
    if n == 0:
        return None, None, None, None
    if rel == 'All':
        if aoi == 'India':
            fig_rel_demo = make_all_india_religious_demography_graph()
            rel_demo_visualization = dcc.Graph(
                id='graph',
                figure=fig_rel_demo
            )
            return make_all_india_religious_demography_table(), rel_demo_visualization, \
                   dbc.Label("ST Religious Population Data for India in 2011"), n
        elif aoi == 'States':
            if states != '':
                return make_religious_demography_state_table(states), [], \
                    dbc.Label("ST Religious population for " + states + " in 2011"), n
    return None, None, dbc.Label("ST Religious Population Data for India from 2011"), None
