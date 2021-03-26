import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard.app import app
from dashboard.content import mainpage

app.layout = mainpage.mainpage

if __name__ == '__main__':
    app.run_server(debug=False)
