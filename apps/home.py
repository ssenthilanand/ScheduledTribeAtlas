import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import dash_table
from dash import dcc
from dash import html
from dash.dash_table.Format import Format, Scheme, Group

from apps.utils import fetch_data

pd.options.mode.chained_assignment = None

# host = "http://tribedemo.expertsoftware.in"
#
# population_url = host + "/population/"
#
# try:
#     response = requests.get(population_url)
#     response.raise_for_status()
# except HTTPError as http_err:
#     print(f'HTTP error occurred: {http_err}')
# except Exception as err:
#     print(f'Other error occurred: {err}')
# else:
#     pass

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
dp_sgf['st_per'] = (dp_sgf['population_st'] / dp_sgf['population_total']) * 100
dp_sgf['sc_per'] = (dp_sgf['population_sc'] / dp_sgf['population_total']) * 100
dp_sgf['gn_per'] = (dp_sgf['population_gn'] / dp_sgf['population_total']) * 100

# df = pd.read_csv('./data/st_population_state_india_2011.csv')
# st_df_country = df[['State Name', 'ST Population', 'State Population', 'ST Percentage']]
# sorted_st_df_country = st_df_country.sort_values('State Name')

# fig = px.bar(sorted_st_df_country, 'State Name', 'ST Percentage')
# fig = px.bar(dp_sgf, 'state_name', 'st_per')
fig = go.Figure()
fig.add_trace(go.Bar(
    x=dp_sgf['state_name'],
    y=dp_sgf['population_st'],
    name='ST population'
))
fig.add_trace(go.Bar(
    x=dp_sgf['state_name'],
    y=dp_sgf['population_total'],
    name='State population'
))
fig.update_xaxes(tickangle=45)
fig.update_layout(
    title_text='ST Population of India in 2011',
    title_x=0.5,
    # yaxis=dict(title='ST population %'),
    xaxis=dict(title='State'),
    legend=dict(x=0,
                y=1.0,
                orientation='h',
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
                ),
    barmode='group',
    height=600
)

india_st_population = dp_sgf['population_st'].sum()
india_total_population = dp_sgf['population_total'].sum()
india_st_percentage = india_st_population / india_total_population * 100

# all_country_table = dbc.Table.from_dataframe(sorted_st_df_country, striped=True, bordered=True, hover=True)


columns = [
    dict(id='state_name', name='State Name'),
    dict(id='population_total', name='State Population', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='population_st', name='ST Population', type='numeric',
         format=Format(group=Group.yes).groups([3, 2, 2])),
    # dict(id='population_total', name='State Population', type='numeric',
    #      format=Format(group=Group.yes).groups([3, 2, 2])),
    dict(id='st_per', name='ST Percentage', type='numeric',
         format=Format(precision=2, scheme=Scheme.fixed)),
]

# columns = [
#               dict(id='a', name='State Name'),
#               dict(id='a', name='ST Population', type='numeric'),
#               dict(id='a', name='State Population', type='numeric'),
#               dict(id='a', name='ST Percentage', type='numeric'),
#           ]

all_country_table = dash_table.DataTable(
    id='all_country_table',
    columns=columns,
    data=dp_sgf.to_dict('records'),
    sort_action="native",
    sort_mode="single",
    column_selectable="single",
    style_as_list_view=True,
    style_cell_conditional=[
        {
            'if': {'column_id': 'state_name'},
            'textAlign': 'left'
        }
    ],
    style_header={
        'fontWeight': 'bold'
    },
)
layout = html.Div(children=[

    html.Title('An Atlas of Scheduled Tribes of India'),
    dbc.Nav(
        children=[
            dbc.NavItem(dbc.NavLink("Home", active=True, href='/apps/home')),
            dbc.NavItem(dbc.NavLink("Demography", href='/apps/demography')),
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
    html.H3(['An Atlas of Scheduled Tribes of India'], style={'text-align': 'center'}),
    html.Br(),

    dbc.Card(
        [
            dbc.CardImg(src='/assets/ST2011.png', top=True),
            dbc.CardBody(
                [
                    html.Label(
                        f'Share of Scheduled Tribes population among India\'s overall population in 2011: {india_st_percentage:.2f}%')
                ], style={'margin': "auto", 'text-align': "center"},
            )
        ]
    ),

    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4(
                        ['State wide Scheduled Tribe population percentage in 2011'],
                        style={'text-align': 'center'}
                    ),
                    html.Br(),
                    all_country_table,
                    html.Br(),
                    dcc.Graph(
                        figure=fig
                    ),
                    html.Br()
                ]
            )
        ]
    ),

], style={'margin': "auto", 'width': "80%"}
)
