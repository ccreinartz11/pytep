import dash

from frontend.mainpage import mainpage

app = dash.Dash(__name__)
app.layout = mainpage
app.run_server(debug=True)
