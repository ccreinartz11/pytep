from app import app
from app import server
from frontend import mainpage

app.layout = mainpage.mainpage

if __name__ == '__main__':
    app.run_server(debug=False)
