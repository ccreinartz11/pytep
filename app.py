import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from frontend.mainpage import mainpage

app = dash.Dash(__name__)
app.layout = mainpage
app.run_server(debug=True)
