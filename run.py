import matlab.engine  # The program doesn't execute if this is not imported before the simulation interface
import backend.siminterface as simulation_interface
si = simulation_interface.SimInterface.setup()  # siminterface is singleton. Must be set up first.
import index


def main():
    index.app.run_server(debug=False)


if __name__ == '__main__':
    main()
