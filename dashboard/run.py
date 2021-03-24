import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# import matlab.engine
import pytep.siminterface as simulation_interface
si = simulation_interface.SimInterface.setup()  # siminterface is singleton. Must be set up first.
import index


def main():
    index.app.run_server(debug=False)


if __name__ == '__main__':
    main()
