from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group, Format
from dash.dependencies import Input, Output
from dash import dash_table
import plotly.graph_objects as go

from app import app
from apps.utils import *

# layout = html.Div([
#     html.H3('Religion'),
# ])


def get_religious_demography():
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


religious_demography = get_religious_demography()
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


religions = ['All', 'Hindu', 'Muslim', 'Christian']
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
    html.H4("ST Religious Population Data for India from 2011"),
    html.Div(
        id='viz-table',
        children=[
            make_all_india_religious_demography_table(),
        ],
    ),
    html.Br(),
    html.Div(
        id='religion-visualization',
        children=[
            dcc.Graph(
                id='graph',
                figure=make_all_india_religious_demography_graph()
            )

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
