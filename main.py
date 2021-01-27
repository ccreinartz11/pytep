import index
from backend import matlab_bridge


def main():
    mb = matlab_bridge.MatlabBridge()
    index.app.run_server(debug=False)


if __name__ == '__main__':
    main()
