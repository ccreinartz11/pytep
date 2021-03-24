from app import app
from dashboard.content import mainpage

app.layout = mainpage.mainpage

if __name__ == '__main__':
    app.run_server(debug=False)
