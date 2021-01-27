import backend.siminterface as siminterface
si = siminterface.SimInterface.setup_no_engine()  # siminterface is singleton. Must be set up first.
print('Setup siminterface.')
import index


def main():
    index.app.run_server(debug=False)


if __name__ == '__main__':
    print('In main')
    main()
