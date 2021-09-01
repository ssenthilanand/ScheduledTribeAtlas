import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import home, demography, religion, orpreligions, indiantribes, aboutus, contactus

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/apps/home':
        return home.layout
    elif pathname == '/apps/demography':
        return demography.layout
    elif pathname == '/apps/religion':
        return religion.layout
    elif pathname == '/apps/orpreligions':
        return orpreligions.layout
    elif pathname == '/apps/aboutus':
        return aboutus.layout
    elif pathname == '/apps/indiantribes':
        return indiantribes.layout
    elif pathname == '/apps/contactus':
        return contactus.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)