import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
# import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_table
from dash_table.Format import Format, Group

from app import app

df = pd.read_csv('./data/population_state_india_2011.csv')
state_list = sorted(df['State Name'])
all_df = df[['State Name', 'ST', 'SC', 'General',
             'State', 'ST %', 'SC %', 'General %']]
sorted_all_df = all_df.sort_values('State Name')

columns = [
    dict(id='State Name', name='State Name'),
    dict(id='ST', name='ST', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='SC', name='SC', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='General', name='General', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='State', name='State', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
]
all_country_table = dash_table.DataTable(
    id='all_country_table',
    columns=columns,
    data=sorted_all_df.to_dict('records'),
    sort_action="native",
    sort_mode="single",
    column_selectable="single",
    style_as_list_view=True,
    style_cell_conditional=[
        {
            'if': {'column_id': 'State Name'},
            'textAlign': 'left'
        }
    ],
    style_header={
        'fontWeight': 'bold'
    },
)

# df = pd.read_csv('./data/population_state_india_2011.csv')
# all_df = df[['State Name', 'ST', 'SC', 'General',
#              'State', 'ST %', 'SC %', 'General %']]
# sorted_all_df = all_df.sort_values('State Name', ascending=False)

n_states = len(sorted_all_df['State Name'])

fig_all = go.Figure(layout=go.Layout(
    height=100 + (32 * n_states),
    xaxis_title='Population',
    yaxis_title='State',
    title_text="Population Details for India"
))
fig_all.update_layout(legend=dict(orientation='h'))
fig_all.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['ST'],
    name='ST',
    orientation='h',
    # text=sorted_all_df['ST %']
))
fig_all.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['SC'],
    name='SC',
    orientation='h',
    # visible='legendonly'
))
fig_all.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['General'],
    name='General',
    orientation='h',
    # visible='legendonly'
))
fig_all.update_layout(barmode='stack')

fig_all.add_trace(go.Scatter(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['State'],
    name='Total',
    orientation='h',
    mode="markers",
    # text=sorted_all_df['State'].apply(lambda x: '{0:1.2f}%'.format(x)),
))

n_states = len(sorted_all_df['State Name'])
fig_all_group = go.Figure(layout=go.Layout(
    height=100 + (64 * n_states),
    xaxis_title='Population',
    yaxis_title='State',
    title_text="Population Details for India"
))
fig_all_group.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['ST'],
    name='ST',
    orientation='h',
    text=sorted_all_df['ST %'].apply(lambda x: '{0:1.2f}%'.format(x)),
))
fig_all_group.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['SC'],
    name='SC',
    orientation='h',
    text=sorted_all_df['SC %'].apply(lambda x: '{0:1.2f}%'.format(x)),
    visible='legendonly'
))
fig_all_group.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['General'],
    name='General',
    orientation='h',
    text=sorted_all_df['General %'].apply(lambda x: '{0:1.2f}%'.format(x)),
    visible='legendonly'
))
fig_all_group.add_trace(go.Bar(
    y=sorted_all_df['State Name'],
    x=sorted_all_df['State'],
    name='Total',
    orientation='h',
    text="100 %",
    visible='legendonly'
))
fig_all_group.update_layout(barmode='group')
# fig_all_group.update_layout(legend=dict(orientation='h'))
fig_all_group.update_traces(textposition="outside")

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
                        {'label': name, 'value': name} for name in state_list
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
                        {'label': 'Total', 'value': 'Total'}
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
    # figure=fig_country
    # figure=fig_all
    figure=fig_all_group,
)

visualization_graph1 = dcc.Graph(
    id='graph',
    # figure=fig_country
    figure=fig_all

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
        if viz == 'graph':
            # print(cats)
            # for cat in cats:
            fig_all_group.for_each_trace(
                lambda trace: trace.update(visible=True) if trace.name in cats else (),
            )
            fig_all_group.for_each_trace(
                lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
            )
            fig_all.for_each_trace(
                lambda trace: trace.update(visible=True) if trace.name in cats else (),
            )
            fig_all.for_each_trace(
                lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
            )

            # fig_all_group.for_each_trace(
            #     lambda trace: trace.update(visible='legendonly') if trace.name != cat else (),
            # )

            return all_country_table, visualization_graph
        else:
            return all_country_table, []
    else:
        dist_df = pd.read_csv('./data/population_district_india_2011.csv')
        dist_all_df = dist_df[['State Name', 'District Name', 'ST', 'SC', 'General',
                               'District', 'ST %', 'SC %', 'General %']]
        filtered_dist_all_df = dist_all_df[dist_all_df['State Name'] == states]
        sorted_filtered_dist_all_df = filtered_dist_all_df.sort_values('District Name', ascending=False)

        district_columns = [
            dict(id='District Name', name='District Name'),
            dict(id='ST', name='ST', type='numeric',
                 format=Format(group=Group.yes).groups([3, 2, 2])),
            dict(id='SC', name='SC', type='numeric',
                 format=Format(group=Group.yes).groups([3, 2, 2])),
            dict(id='General', name='General', type='numeric',
                 format=Format(group=Group.yes).groups([3, 2, 2])),
            dict(id='District', name='District', type='numeric',
                 format=Format(group=Group.yes).groups([3, 2, 2])),
        ]

        filtered_table = dash_table.DataTable(
            id='all_country_table',
            columns=district_columns,
            data=filtered_dist_all_df.sort_values('District Name').to_dict('records'),
            sort_action="native",
            sort_mode="single",
            column_selectable="single",
            style_as_list_view=True,
            style_cell_conditional=[
                {
                    'if': {'column_id': 'District Name'},
                    'textAlign': 'left'
                }
            ],
            style_header={
                'fontWeight': 'bold'
            },
        )

        filtered_visualization = dcc.Graph(
            id='graph',
            # figure=fig_filtered_state
            figure=make_filtered_state_population_graph(sorted_filtered_dist_all_df, states)
        )
        filtered_visualization.figure.for_each_trace(
            lambda trace: trace.update(visible=True) if trace.name in cats else (),
        )
        filtered_visualization.figure.for_each_trace(
            lambda trace: trace.update(visible='legendonly') if trace.name not in cats else (),
        )

        if viz == 'graph':
            return filtered_table, filtered_visualization
        else:
            return filtered_table, []


def make_filtered_state_population_graph(districts, states):
    districts = districts.sort_values('District Name', ascending=False)
    n_districts = len(districts['District Name'])

    fig_districts = go.Figure(layout=go.Layout(
        height=200 + (32 * n_districts),
        xaxis_title='Population',
        yaxis_title='Districts',
        title_text="Population Details for " + states
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['District Name'],
        x=districts['ST'],
        name='ST',
        orientation='h',
        text=districts['ST %'].apply(lambda x: '{0:1.2f}%'.format(x)),
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['District Name'],
        x=districts['SC'],
        name='SC',
        orientation='h',
        text=districts['SC %'].apply(lambda x: '{0:1.2f}%'.format(x)),
        visible='legendonly'
    ))
    fig_districts.add_trace(go.Bar(
        y=districts['District Name'],
        x=districts['General'],
        name='General',
        orientation='h',
        text=districts['General %'].apply(lambda x: '{0:1.2f}%'.format(x)),
        visible='legendonly'
    ))
    # fig_districts.add_trace(go.Bar(
    #     y=districts['District Name'],
    #     x=districts['District'],
    #     name='Total',
    #     orientation='h',
    #     text="100 %",
    #     visible='legendonly'
    # ))
    fig_districts.update_layout(barmode='stack')
    fig_districts.update_traces(textposition="outside")
    fig_districts.add_trace(go.Scatter(
        y=districts['District Name'],
        x=districts['District'],
        name='Total',
        orientation='h',
        mode="markers",
        # text=sorted_all_df['State'].apply(lambda x: '{0:1.2f}%'.format(x)),
    ))
    return fig_districts
