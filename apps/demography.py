import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dash_table.Format import Format, Group, Scheme
# import plotly.express as px
from dash.dependencies import Input, Output, State
import timeit

from dash.exceptions import PreventUpdate

from app import app
from apps.utils import *
from babel.numbers import format_number, format_decimal, format_percent

state_literacy = None
state_pop = fetch_data('population')
state_gratio = fetch_data('genderratio')
state_lit = fetch_local_data('data/literacy.json')


def get_state_population_data():
    # response = fetch_data('population')
    data = pd.read_json(state_pop)
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


def get_state_literacy_data():
    # response = fetch_data('literacy')
    data = pd.read_json(state_lit)
    data_literacy = pd.json_normalize(data['data'])
    int_cols = ['population_gn', 'population_sc', 'population_st', 'literate_gn', 'literate_sc', 'literate_st']
    float_cols = ['literacy_gn', 'literacy_sc', 'literacy_st']
    for col in int_cols:
        data_literacy[col] = pd.to_numeric(data_literacy[col], errors='coerce').fillna(0).astype('int')
    for col in float_cols:
        data_literacy[col] = pd.to_numeric(data_literacy[col], errors='coerce').fillna(0.00).astype('float')
    data_literacy_pop = data_literacy.copy(deep=True)
    data_literacy_pop = data_literacy_pop.drop(['literacy_gn', 'literacy_sc', 'literacy_st'], axis=1)
    # data_literacy_per = data_literacy.copy(deep=True)
    # data_literacy_per = data_literacy_per.drop(
    #     ['literate_gn', 'literate_sc', 'literate_st', 'population_gn', 'population_sc', 'population_st'], axis=1)
    data_literacy_pop_states = data_literacy_pop.groupby('state_name', as_index=False)
    # data_literacy_per_states = data_literacy_per.groupby('state_name', as_index=False)
    dlps = data_literacy_pop_states.sum()
    dlps['literate_tot'] = dlps['literate_gn'] + dlps['literate_sc'] + dlps['literate_st']
    dlps['population_tot'] = dlps['population_gn'] + dlps['population_sc'] + dlps['population_st']
    dlps['literacy_gn'] = dlps['literate_gn'] / dlps['population_gn'] * 100
    dlps['literacy_sc'] = dlps['literate_sc'] / dlps['population_sc'] * 100
    dlps['literacy_st'] = dlps['literate_st'] / dlps['population_st'] * 100
    dlps['literacy_tot'] = dlps['literate_tot'] / dlps['population_tot'] * 100
    return dlps


def get_state_gender_ratio_data():
    # response = fetch_data('population')
    data = pd.read_json(state_gratio)
    data_gratio = pd.json_normalize(data['data'])
    dgratio = data_gratio[['district_name', 'state_name', 'gender_ratio', 'gn_gr', 'sc_gr', 'st_gr']]
    num_cols = ['gender_ratio', 'gn_gr', 'sc_gr', 'st_gr']
    for col in num_cols:
        dgratio[col] = pd.to_numeric(dgratio[col], errors='coerce').fillna(0).astype('int')

    d_gratio = dgratio.drop('district_name', axis=1)
    dp_sg = d_gratio.groupby('state_name', as_index=False)

    dp_sgf = dp_sg.mean()

    return dp_sgf


def get_district_population_data(state):
    # response = fetch_data('population')
    # data = pd.read_json(state_pop)
    # data_population = pd.json_normalize(data['data'])
    data_population = fetch_district_pop(state)
    dp = data_population[['district_name', 'state_name', 'population_gn', 'population_sc', 'population_st']]
    num_cols = ['population_gn', 'population_sc', 'population_st']
    for col in num_cols:
        dp[col] = pd.to_numeric(dp[col], errors='coerce').fillna(0).astype('int')

    dp['population_total'] = dp['population_gn'] + dp['population_sc'] + dp['population_st']
    return dp


def get_district_literacy_data(state):
    # response = fetch_data('literacy')
    # data = pd.read_json(state_lit)
    # data_literacy = pd.json_normalize(data['data'])
    data_literacy = fetch_district_lit(state)
    district_code_list = data_literacy['district_code'].to_list()
    district_name_list = []
    for code in district_code_list:
        district_name_list.append(get_district_name(code))
    district_names = pd.DataFrame({'district_code': district_code_list, 'district_name': district_name_list})
    data_literacy = data_literacy.merge(district_names, on='district_code')
    data_literacy = data_literacy.sort_values('district_name')
    # print(data_literacy['district_name'])
    int_cols = ['population_gn', 'population_sc', 'population_st', 'literate_gn', 'literate_sc', 'literate_st']
    float_cols = ['literacy_gn', 'literacy_sc', 'literacy_st']
    for col in int_cols:
        data_literacy[col] = pd.to_numeric(data_literacy[col], errors='coerce').fillna(0).astype('int')
    for col in float_cols:
        data_literacy[col] = pd.to_numeric(data_literacy[col], errors='coerce').fillna(0.00).astype('float')
    return data_literacy


def get_district_gender_ratio_data(state):
    data = fetch_district_gratio(state)
    # data_gratio = pd.json_normalize(data['data'])
    dgratio = data[['district_name', 'state_name', 'gender_ratio', 'gn_gr', 'sc_gr', 'st_gr']]
    num_cols = ['gender_ratio', 'gn_gr', 'sc_gr', 'st_gr']
    for col in num_cols:
        dgratio[col] = pd.to_numeric(dgratio[col], errors='coerce').fillna(0).astype('int')
    return dgratio


state_population = get_state_population_data()

# print(state_population)
# district_population = get_district_population_data()
# print("received district population")

if state_literacy is None:
    state_literacy = get_state_literacy_data()
    # print("received state literacy")
# district_literacy = get_district_literacy_data()
# print("received district literacy")
# print(get_state_code('Assam'))
# state_list = fetch_states()
n_states = len(state_list)

state_gender_ratio = get_state_gender_ratio_data()

all_categories = ['ST', 'SC', 'General']
# districts_list = fetch_districts()
# n_districts = len(districts_list)


def make_all_india_population_table(cats='ST'):
    hidden_categories = [x for x in all_categories if x not in cats]
    column_names = {'ST': 'population_st', 'SC': 'population_sc', 'General': 'population_gn'}
    columns_to_hide=[column_names.get(y) for y in hidden_categories]
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='population_total', name='Total Population', type='numeric',
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
        # hidden_columns=['population_sc, population_gn'],
        data=state_population.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        hidden_columns=columns_to_hide,
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


def make_all_india_literacy_table(cats='ST'):
    hidden_categories = [x for x in all_categories if x not in cats]
    column_names = {'ST': 'literacy_st', 'SC': 'literacy_sc', 'General': 'literacy_gn'}
    columns_to_hide = [column_names.get(y) for y in hidden_categories]
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='literacy_tot', name='State Literacy', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_st', name='ST Literacy', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_sc', name='SC Literacy', type='numeric', hideable=True,
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_gn', name='General Literacy', type='numeric', hideable=True,
             format=Format(precision=2, scheme=Scheme.fixed)),
        # dict(id='population_total', name='State Population', type='numeric',
        #      format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='st_per', name='ST Percentage', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        # hidden_columns=['population_sc, population_gn'],
        data=state_literacy.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        hidden_columns=columns_to_hide,
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


def make_all_india_gender_ratio_table(cats='ST'):
    hidden_categories = [x for x in all_categories if x not in cats]
    column_names = {'ST': 'st_gr', 'SC': 'sc_gr', 'General': 'gn_gr'}
    columns_to_hide = [column_names.get(y) for y in hidden_categories]
    columns = [
        dict(id='state_name', name='State Name'),
        dict(id='gender_ratio', name='Gender Ratio', type='numeric',
             format=Format(precision=0, scheme=Scheme.fixed)),
        dict(id='st_gr', name='ST Gender Ratio', type='numeric',
             format=Format(precision=0, scheme=Scheme.fixed)),
        dict(id='sc_gr', name='SC Gender Ratio', type='numeric', hideable=True,
             format=Format(precision=0, scheme=Scheme.fixed)),
        dict(id='gn_gr', name='General Gender Ratio', type='numeric', hideable=True,
             format=Format(precision=0, scheme=Scheme.fixed)),
        # dict(id='population_total', name='State Population', type='numeric',
        #      format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='st_per', name='ST Percentage', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        # hidden_columns=['population_sc, population_gn'],
        data=state_gender_ratio.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        hidden_columns=columns_to_hide,
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


def make_all_india_literacy_graph(cats='ST'):
    state_literacy_d = state_literacy.sort_values('state_name', ascending=False)
    fig_all = go.Figure(layout=go.Layout(
        height=100 + (32 * n_states),
        xaxis=dict(title='Literacy %'),
        yaxis=dict(title='State'),
        title=dict(text="Literacy Details for India")
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        y=state_literacy_d['state_name'],
        x=state_literacy_d['literacy_st'],  # .apply(lambda x: format_decimal(x, format='00.00', locale='en')),
        name='ST',
        orientation='h',
        hovertemplate="%{x}%",
        # text=state_literacy_d['literate_st'].apply(lambda x: format_decimal(x, locale='en_IN')),
    ))
    if 'SC' in cats:
        fig_all.add_trace(go.Bar(
            y=state_literacy_d['state_name'],
            x=state_literacy_d['literacy_sc'],  # .apply(lambda x: format_percent(x/100, format='00.00\u0025',
            # locale='en')),
            name='SC',
            orientation='h',
            hovertemplate="%{x}%",
            # text=state_literacy_d['literate_sc'].apply(lambda x: format_decimal(x, locale='en_IN')),
        ))
    if 'General' in cats:
        fig_all.add_trace(go.Bar(
            y=state_literacy_d['state_name'],
            x=state_literacy_d['literacy_gn'],  # .apply(lambda x: format_percent(x/100, format='00.00\u0025',
            # locale='en')),
            name='General',
            orientation='h',
            hovertemplate="%{x}%",
            # text=state_literacy_d['literate_gn'].apply(lambda x: format_decimal(x, locale='en_IN')),
        ))
    fig_all.update_layout(barmode='group')
    fig_all.update_traces(textposition="outside")
    return fig_all


def make_all_india_population_graph(cats='ST'):
    state_population_d = state_population.sort_values('state_name', ascending=False)
    fig_all = go.Figure(layout=go.Layout(
        height=100 + (32 * n_states),
        xaxis=dict(title='Population'),
        yaxis=dict(title='State'),
        title=dict(text="Population Details for India")
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        y=state_population_d['state_name'],
        x=state_population_d['population_st'],
        name='ST',
        orientation='h',
        # text=sorted_all_df['ST %']
    ))
    if 'SC' in cats:
        fig_all.add_trace(go.Bar(
            y=state_population_d['state_name'],
            x=state_population_d['population_sc'],
            name='SC',
            orientation='h',
            # visible='legendonly'
        ))
    if 'General' in cats:
        fig_all.add_trace(go.Bar(
            y=state_population_d['state_name'],
            x=state_population_d['population_gn'],
            name='General',
            orientation='h',
            # visible='legendonly'
        ))
    fig_all.update_layout(barmode='group')
    return fig_all


def make_all_india_gender_ratio_graph(cats='ST'):
    state_gratio_d = state_gender_ratio.sort_values('state_name', ascending=False)
    fig_all = go.Figure(layout=go.Layout(
        height=100 + (32 * n_states),
        xaxis=dict(title='Gender Ratio %'),
        yaxis=dict(title='State'),
        title=dict(text="Gender Ratio Details for India")
    ))
    fig_all.update_layout(legend=dict(orientation='h'))
    fig_all.add_trace(go.Bar(
        y=state_gratio_d['state_name'],
        x=state_gratio_d['st_gr'],  # .apply(lambda x: format_decimal(x, format='00.00', locale='en')),
        name='ST',
        orientation='h',
    ))
    if 'SC' in cats:
        fig_all.add_trace(go.Bar(
            y=state_gratio_d['state_name'],
            x=state_gratio_d['sc_gr'],  # .apply(lambda x: format_percent(x/100, format='00.00\u0025',
            # locale='en')),
            name='SC',
            orientation='h',
        ))
    if 'General' in cats:
        fig_all.add_trace(go.Bar(
            y=state_gratio_d['state_name'],
            x=state_gratio_d['gn_gr'],  # .apply(lambda x: format_percent(x/100, format='00.00\u0025',
            # locale='en')),
            name='General',
            orientation='h',
        ))
    fig_all.update_layout(barmode='group')
    fig_all.update_traces(textposition="outside")
    return fig_all


# fig_india = make_all_india_population_graph()

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
    ],
)

bdi_card = dbc.Card(
    [
        dbc.CardHeader("Basic Demographic Indicators"),
        dbc.CardBody(
            [
                html.P("Select one or more of the following basic demographic indicators", className="card-text"),
                dbc.RadioItems(
                    id='dbi-select',
                    options=[
                        {"label": name, "value": name} for name in dbi_list
                        # {'label': 'Population', 'value': 'Population'},
                        # {'label': 'Literacy', 'value': 'Literacy'},
                        # {'label': 'Gender Ratio', 'value': 'Gender Ratio'},
                        # {'label': 'Fertility Rate', 'value': 'Fertility Rate'},
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

# visualization_graph = dcc.Graph(
# id='graph',
# figure=fig_country
# figure=fig_all
# figure=fig_india,
# )

# visualization_graph1 = dcc.Graph(
#     id='graph',
#     # figure=fig_country
#     figure=fig_all
#
# )
layout = html.Div(children=[
    html.Div(html.Img(src=app.get_asset_url('cps_logo.png'),
                      style={'margin': "auto", 'width': "100%", 'text-align': "center"}, )),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", active=True, href='/apps/demography')),
            dbc.NavItem(dbc.NavLink("Religion", href='/apps/religion')),
            dbc.NavItem(dbc.NavLink("ORP Atlas", href='/apps/orpreligions')),
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
    html.H3('Demography information of Scheduled Tribes of India', style={'text-align': 'center'}),
    html.Br(),
    dbc.CardGroup(
        [
            bdi_card,
            aoi_card
        ],
    ),
    dbc.CardGroup(
        [
            cat_card,
            viz_card
        ]
    ),

    html.Br(),
    html.Br(),
    html.Div(
        [
            dbc.Button("Get Data", id='viz-button', color="primary", n_clicks=0),
        ],
        className="d-grid gap-2",
    ),

    html.Br(),
    dcc.Loading(
        id="loading-1",
        type="circle",
        children=html.Div(id="loading-output-1", style={'display': 'none'}),
    ),
    html.Br(),
    dbc.Card(
        id='map-card',
        children=''
        # [
        #     dbc.CardImg(src='/assets/India_literacy.svg', top=True),
        #     dbc.CardBody(
        #         [
        #             html.Label(
        #                 f'Detail of Map')
        #         ], style={'margin': "auto", 'text-align': "center"},
        #     )
        # ]
    ),
    html.Br(),
    html.H4(
        id='area-label',
        children=[],
        style={'textAlign': 'center'}
    ),
    html.Br(),

    html.Div(
        id='viz-table',
        children=[
            # all_country_table,
        ],
    ),
    html.Br(),
    html.Div(
        id='demography-visualization',
        children=[
            html.Br(),
        ],  # style={'display': 'None'}
    ),
    html.Br(),
    html.Br(),
    html.Footer(
        children=[
            dbc.Label("Copyright © 2022. Centre for Policy Studies.")
        ],
        style={'textAlign': 'center'}
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
     Output('demography-visualization', 'children'),
     # Output('demography-visualization1', 'children')],
     Output('area-label', 'children'),
     Output('map-card', 'children'),
     Output("loading-output-1", "children")],
    [Input('viz-button', 'n_clicks'),
     State('dbi-select', 'value'),
     State('aoi-select', 'value'),
     State('cat-selector', 'value'),
     State('states-select', 'value'),
     State('viz-selector', 'value')]
)
def get_partial_data(n, dbi, aoi, cats, states, viz):
    # print(dbi, aoi, cats, states, viz)
    if states is None:
        states = ''
    if n == 0:
        # raise PreventUpdate
        return None, None, None, None, None
    elif aoi == 'India':
        if viz[-1] == 'graph':
            # fig_india.for_each_trace(
            #     lambda trace: trace.update(visible=True) if trace.name in cats else (),
            # )
            # fig_india.for_each_trace(
            #     lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
            # )
            if dbi == 'Population':
                fig_pop = make_all_india_population_graph(cats)
                population_visualization = dcc.Graph(
                    id='graph',
                    figure=fig_pop
                )
                all_india_table = make_all_india_population_table(cats)
                fig_pop.for_each_trace(
                    lambda trace: trace.update(visible=True) if trace.name in cats else (),
                )
                fig_pop.for_each_trace(
                    lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
                )
                return all_india_table, population_visualization, \
                       dbc.Label("Population Data for India from 2011"), make_map(dbi, aoi, states), n
            elif dbi == 'Literacy':
                fig_lit = make_all_india_literacy_graph(cats)
                literacy_visualization = dcc.Graph(
                    id='graph',
                    figure=fig_lit
                )
                fig_lit.for_each_trace(
                    lambda trace: trace.update(visible=True) if trace.name in cats else (),
                )
                fig_lit.for_each_trace(
                    lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
                )
                all_india_table = make_all_india_literacy_table(cats)
                return all_india_table, literacy_visualization, \
                       dbc.Label("Literacy Data for India from 2011"), make_map(dbi, aoi, states), n
            elif dbi == 'Gender Ratio':
                fig_lit = make_all_india_gender_ratio_graph(cats)
                gender_ratio_visualization = dcc.Graph(
                    id='graph',
                    figure=fig_lit
                )
                fig_lit.for_each_trace(
                    lambda trace: trace.update(visible=True) if trace.name in cats else (),
                )
                fig_lit.for_each_trace(
                    lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
                )
                all_india_table = make_all_india_gender_ratio_table(cats)
                return all_india_table, gender_ratio_visualization, \
                       dbc.Label("Gender Ratio Data for India from 2011"), make_map(dbi, aoi, states), n
            elif dbi == 'Fertility Rate':  # TODO
                # all_india_table = make_all_india_population_table()
                all_india_table = None
                return all_india_table, [], dbc.Label("Fertility Rate data for India from 2011 is not currently available"), \
                        make_map(dbi, aoi, states), n
        else:
            if dbi == 'Population':
                all_india_table = make_all_india_population_table(cats)
                return all_india_table, [], dbc.Label("Population Data for India from 2011"), \
                       make_map(dbi, aoi, states), n
            elif dbi == 'Literacy':
                all_india_table = make_all_india_literacy_table(cats)
                return all_india_table, [], dbc.Label("Literacy Data for India from 2011"), \
                       make_map(dbi, aoi, states), n
            elif dbi == 'Gender Ratio':
                all_india_table = make_all_india_gender_ratio_table(cats)
                return all_india_table, [], dbc.Label("Gender Ratio Data for India from 2011"), \
                       make_map(dbi, aoi, states), n
            elif dbi == 'Fertility Rate':  # TODO
                # all_india_table = make_all_india_population_table()
                all_india_table = None
                return all_india_table, [], dbc.Label("Fertility Rate data for India from 2011 is not currently available"), \
                        make_map(dbi, aoi, states), n
            else:
                all_india_table = make_all_india_population_table()
                return all_india_table, [], dbc.Label(''), make_map(dbi, aoi, states), n
    elif aoi == 'States':  # TODO
        if states != '':
            if viz[-1] == 'graph':
                if dbi == 'Population':
                    district_population = get_district_population_data(states)
                    fig_pop = make_filtered_state_population_graph(district_population, states, cats)
                    population_visualization = dcc.Graph(
                        id='graph',
                        figure=fig_pop
                    )
                    state_table = make_filtered_state_population_table(district_population, cats)
                    fig_pop.for_each_trace(
                        lambda trace: trace.update(visible=True) if trace.name in cats else (),
                    )
                    fig_pop.for_each_trace(
                        lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
                    )
                    return state_table, population_visualization, \
                           dbc.Label("Population Data for " + states + " from 2011"), make_map(dbi, aoi, states), n
                elif dbi == 'Literacy':
                    # print(states)
                    district_literacy = get_district_literacy_data(states)
                    # print(district_literacy)
                    state_table = make_filtered_state_literacy_table(district_literacy, cats)
                    fig_lit = make_filtered_state_literacy_graph(district_literacy, states, cats)
                    literacy_visualization = dcc.Graph(
                        id='graph',
                        figure=fig_lit
                    )
                    fig_lit.for_each_trace(
                        lambda trace: trace.update(visible=True) if trace.name in cats else (),
                    )
                    fig_lit.for_each_trace(
                        lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
                    )
                    return state_table, literacy_visualization, \
                           dbc.Label("Literacy Data for " + states + " from 2011"), make_map(dbi, aoi, states), n
                elif dbi == 'Gender Ratio':
                    # print(states)
                    district_gender_ratio = get_district_gender_ratio_data(states)
                    # print(district_literacy)
                    state_table = make_filtered_state_gender_ratio_table(district_gender_ratio, cats)
                    fig_lit = make_filtered_state_gender_ratio_graph(district_gender_ratio, states, cats)
                    gratio_visualization = dcc.Graph(
                        id='graph',
                        figure=fig_lit
                    )
                    fig_lit.for_each_trace(
                        lambda trace: trace.update(visible=True) if trace.name in cats else (),
                    )
                    fig_lit.for_each_trace(
                        lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
                    )
                    return state_table, gratio_visualization, \
                           dbc.Label("Gender Ratio Data for " + states + " from 2011"), make_map(dbi, aoi, states), n
                elif dbi == 'Fertility Rate':  # TODO
                    # all_india_table = make_all_india_population_table()
                    all_india_table = None
                    return all_india_table, [], dbc.Label(
                        "Fertility Rate data for " + states + " from 2011 is not currently available")   , \
                            make_map(dbi, aoi, states), n
            #     return filtered_table, filtered_visualization, dbc.Label(
            #         "Population Data for " + states + "  from 2011")
            # else:
            #     return filtered_table, [], dbc.Label("Population Data for " + states + "  from 2011")
            else:
                if dbi == 'Population':
                    state_table = make_filtered_state_population_table(get_district_population_data(states), cats)
                    return state_table, [], dbc.Label("Population Data for India from 2011"), \
                           make_map(dbi, aoi, states), n
                elif dbi == 'Literacy':
                    state_table = make_filtered_state_literacy_table(get_district_literacy_data(states), cats)
                    return state_table, [], dbc.Label("Literacy Data for India from 2011"), \
                           make_map(dbi, aoi, states), n
                elif dbi == 'Gender Ratio':
                    state_table = make_filtered_state_gender_ratio_table(get_district_gender_ratio_data(states), cats)
                    return state_table, [], dbc.Label("Gender Ratio Data for India from 2011"), \
                           make_map(dbi, aoi, states), n
                elif dbi == 'Fertility Rate':  # TODO
                    # all_india_table = make_all_india_population_table()
                    all_india_table = None
                    return all_india_table, [], dbc.Label(
                        "Fertility Rate data for " + states + " from 2011 is not currently available")   , \
                            make_map(dbi, aoi, states), n
        else:
            return None, None, None, None, None
    else:
        return None, None, None, None, None


def make_filtered_state_population_table(districts, cats='ST'):
    hidden_categories = [x for x in all_categories if x not in cats]
    column_names = {'ST': 'population_st', 'SC': 'population_sc', 'General': 'population_gn'}
    columns_to_hide = [column_names.get(y) for y in hidden_categories]
    districts = districts.sort_values('district_name')
    district_columns = [
        dict(id='district_name', name='District Name'),
        dict(id='population_total', name='Total Population', type='numeric',
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
        data=districts.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        hidden_columns=columns_to_hide,
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
        css=[{"selector": ".show-hide", "rule": "display: none"}],
    )
    return filtered_state_table


def make_filtered_state_literacy_table(districts, cats='ST'):
    # districts = districts.sort_values('district_code')
    hidden_categories = [x for x in all_categories if x not in cats]
    column_names = {'ST': 'literacy_st', 'SC': 'literacy_sc', 'General': 'literacy_gn'}
    columns_to_hide = [column_names.get(y) for y in hidden_categories]
    columns = [
        dict(id='district_name', name='District Name'),
        # dict(id='literacy_tot', name='District Literacy', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_st', name='ST Literacy', type='numeric',
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_sc', name='SC Literacy', type='numeric', hideable=True,
             format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='literacy_gn', name='General Literacy', type='numeric', hideable=True,
             format=Format(precision=2, scheme=Scheme.fixed)),
        # dict(id='population_total', name='State Population', type='numeric',
        #      format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='st_per', name='ST Percentage', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        # hidden_columns=['population_sc, population_gn'],
        data=districts.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        hidden_columns=columns_to_hide,
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
    return all_country_table


def make_filtered_state_gender_ratio_table(districts, cats='ST'):
    hidden_categories = [x for x in all_categories if x not in cats]
    column_names = {'ST': 'st_gr', 'SC': 'sc_gr', 'General': 'gn_gr'}
    columns_to_hide = [column_names.get(y) for y in hidden_categories]
    districts = districts.sort_values('district_name')
    columns = [
        dict(id='district_name', name='District Name'),
        # dict(id='literacy_tot', name='District Literacy', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
        dict(id='gender_ratio', name='Gender Ratio', type='numeric',
             format=Format(precision=0, scheme=Scheme.fixed)),
        dict(id='st_gr', name='ST Gender Ratio', type='numeric',
             format=Format(precision=0, scheme=Scheme.fixed)),
        dict(id='sc_gr', name='SC Gender Ratio', type='numeric', hideable=True,
             format=Format(precision=0, scheme=Scheme.fixed)),
        dict(id='gn_gr', name='General Gender Ratio', type='numeric', hideable=True,
             format=Format(precision=0, scheme=Scheme.fixed)),
        # dict(id='population_total', name='State Population', type='numeric',
        #      format=Format(group=Group.yes).groups([3, 2, 2])),
        # dict(id='st_per', name='ST Percentage', type='numeric',
        #      format=Format(precision=2, scheme=Scheme.fixed)),
    ]
    all_country_table = dash_table.DataTable(
        id='all_country_table',
        columns=columns,
        # hidden_columns=['population_sc, population_gn'],
        data=districts.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        column_selectable="single",
        style_as_list_view=True,
        hidden_columns=columns_to_hide,
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
    return all_country_table


def make_filtered_state_population_graph(districts, states, cats='ST'):
    districts = districts.sort_values('district_name', ascending=False)
    n_district = len(districts['district_name'])

    fig_districts = go.Figure(layout=go.Layout(
        height=200 + (32 * n_district),
        xaxis=dict(title='Population'),
        # xaxis_title='Population',
        yaxis=dict(title='Districts'),
        title_text="Population Details for " + states
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['district_name'],
        x=districts['population_st'],
        name='ST',
        orientation='h',
        text=districts['population_st']  # .apply(lambda x: '{0:1.2f}%'.format(x)),
    ))
    if 'SC' in cats:
        fig_districts.add_trace(go.Bar(
            y=districts['district_name'],
            x=districts['population_sc'],
            name='SC',
            orientation='h',
            text=districts['population_sc'],  # .apply(lambda x: '{0:1.2f}%'.format(x)),
            visible='legendonly'
        ))
    if 'General' in cats:
        fig_districts.add_trace(go.Bar(
            y=districts['district_name'],
            x=districts['population_gn'],
            name='General',
            orientation='h',
            text=districts['population_gn'],  # .apply(lambda x: '{0:1.2f}%'.format(x)),
            visible='legendonly'
        ))
    fig_districts.update_layout(barmode='group')
    fig_districts.update_traces(textposition="outside")

    return fig_districts


def make_filtered_state_literacy_graph(districts, states, cats='ST'):
    districts = districts.sort_values('district_name', ascending=False)
    n_district = len(districts['district_name'])

    fig_districts = go.Figure(layout=go.Layout(
        height=200 + (32 * n_district),
        xaxis=dict(title='Literacy %'),
        # xaxis_title='Population',
        yaxis=dict(title='Districts'),
        title_text="Literacy Details for " + states
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['district_name'],
        x=districts['literacy_st'],
        name='ST',
        orientation='h',
        hovertemplate="%{x}%",
        # text=districts['literate_st']  # .apply(lambda x: '{0:1.2f}%'.format(x)),
    ))
    if 'SC' in cats:
        fig_districts.add_trace(go.Bar(
            y=districts['district_name'],
            x=districts['literacy_sc'],
            name='SC',
            orientation='h',
            hovertemplate="%{x}%",
            # text=districts['literate_sc'],  # .apply(lambda x: '{0:1.2f}%'.format(x)),
            visible='legendonly'
        ))
    if 'General' in cats:
        fig_districts.add_trace(go.Bar(
            y=districts['district_name'],
            x=districts['literacy_gn'],
            name='General',
            orientation='h',
            hovertemplate="%{x}%",
            # text=districts['literate_gn'],  # .apply(lambda x: '{0:1.2f}%'.format(x)),
            visible='legendonly'
        ))
    fig_districts.update_layout(barmode='group')
    fig_districts.update_traces(textposition="outside")

    return fig_districts


def make_filtered_state_gender_ratio_graph(districts, states, cats='ST'):
    districts = districts.sort_values('district_name', ascending=False)
    n_district = len(districts['district_name'])

    fig_districts = go.Figure(layout=go.Layout(
        height=200 + (32 * n_district),
        xaxis=dict(title='Population'),
        # xaxis_title='Population',
        yaxis=dict(title='Districts'),
        title_text="Gender Ratio Details for " + states
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['district_name'],
        x=districts['st_gr'],
        name='ST',
        orientation='h',
    ))
    if 'SC' in cats:
        fig_districts.add_trace(go.Bar(
            y=districts['district_name'],
            x=districts['sc_gr'],
            name='SC',
            orientation='h',
            visible='legendonly'
        ))
    if 'General' in cats:
        fig_districts.add_trace(go.Bar(
            y=districts['district_name'],
            x=districts['gn_gr'],
            name='General',
            orientation='h',
            visible='legendonly'
        ))
    fig_districts.update_layout(barmode='group')
    fig_districts.update_traces(textposition="outside")

    return fig_districts


def make_map(dbi, aoi, states):
    missing_codes = [3, 4, 6, 7, 9, 34]
    if dbi == 'Population':
        if aoi == 'India':
            map_india = [
                dbc.CardImg(src='/assets/maps/demography/india/population/population.png', top=True),
                dbc.CardBody(
                    [
                        html.Label(
                            f'ST Population of India in 2011')
                    ], style={'margin': "auto", 'text-align': "center"},
                )
            ]
        elif aoi == 'States':
            map_india = [
                dbc.CardImg(src='/assets/maps/demography/india/population/population.png', top=True),
                dbc.CardBody(
                    [
                        html.Label(
                            f'ST Population of India in 2011')
                    ], style={'margin': "auto", 'text-align': "center"},
                )
            ]
        else:
            map_india = ''
        return map_india
    elif dbi == 'Literacy':
        if aoi == 'India':
            map_india = [
                dbc.CardImg(src='/assets/maps/demography/india/literacy/literacy.png', top=True),
                dbc.CardBody(
                    [
                        html.Label(
                            f'Literacy of India in 2011')
                    ], style={'margin': "auto", 'text-align': "center"},
                )
            ]
        elif aoi == 'States':
            map_india = [
                dbc.CardImg(src='/assets/maps/demography/india/literacy/literacy.png', top=True),
                dbc.CardBody(
                    [
                        html.Label(
                            f'Literacy of India in 2011')
                    ], style={'margin': "auto", 'text-align': "center"},
                )
            ]
        else:
            map_india = ''
        return map_india
    elif dbi == 'Gender Ratio':
        if aoi == 'India':
            map_india = [
                dbc.CardImg(src='/assets/maps/demography/india/genderratio/genderratio.png', top=True),
                dbc.CardBody(
                    [
                        html.Label(
                            f'{dbi} of India in 2011')
                    ], style={'margin': "auto", 'text-align': "center"},
                )
            ]
        elif aoi == 'States':
            state_code = get_state_code(states)
            if state_code not in missing_codes:
                map_india = [
                    dbc.CardImg(src="/assets/maps/demography/states/genderratio/" + state_code + ".svg", top=True),
                    dbc.CardBody(
                        [
                            html.Label(
                                f'{dbi} of India in 2011')
                        ], style={'margin': "auto", 'text-align': "center"},
                    )
                ]
            else:
                map_india = [
                    dbc.Label[f'Data for {dbi} of ST population in {states} in 2011 is not available']
                ]
        else:
            map_india = ''
        return map_india
    return ''
