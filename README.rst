.. role:: raw-latex(raw)
   :format: latex
..

Introduction to pyTEP
#####################

What is pyTEP?
==============

pyTEP is an open-source simulation API for the Tennessee Eastman process
in Python. It facilitates the setup of complex simulation scenarios and
provides the option of interactive simulation.

Through pyTEPs high-level API, users can setup simulations, change
operating conditions and store simulation data without being exposed to
the underlying mechanics of the simulator. In addition to the newly
introduced features, pyTEP promises more versatility and more
straightforward usage that existing TEP simulators.

How to cite
===========

Reinartz, C. and Enevoldsen, T.T. "pyTEP: A Python package for interactive simulations of the Tennessee Eastman process", 2021


Installation
############

In order to install and run pyTEP, the MATLAB engine for pythong must be
installed, which requires the following conditions to be met: - A
licensed (and activated) MATLAB/Simulink installation (Tested with 2019a
and 2020b) - Python 3.7 - (Optional) virtual Python environment

It is highly recommended to install pyTEP within a virtual environment.

Summary of installation steps

1. Create a virtual environment with Python3.7
2. Install the MATLAB engine into the virtual environment
3. pip install pytep

Installing the MATLAB engine
=====================================

Step 1 - Locating the MATLAB install path
------------------------------------------

Finding the MATLAB install path can either be done by searching through the file system, or executing 

.. code-block:: matlab

	fullfile(matlabroot,'extern','engines','python')

in the MATLAB console. The resulting path will look similar to 
`/usr/local/matlab/r2019b/extern/engines/python`.
The path specified above is used in this guide, but keep in mind that it might be different on your system.

Step 2 - Installing the MATLAB engine
-------------------------------------

Linux
^^^^^

Create a virtual environment such as `pytep_env` with Python3.7, take note of the location of which the virtual environment is created (e.g. `/home/USER/.venvs/pytep_env`). Once the virtual environment is created and the MATLAB path has been obtained, change directories to the MATLAB engine path and run `setup.py`, whilst pointing it towards your virtual environment

.. code-block:: bash

	cd /usr/local/MATLAB/R2019b/extern/engines/python sudo python3.7
	setup.py install –prefix="/PATH/TO/VENVDIR/pytep_env"

Windows (Using anaconda prompt)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open the Anaconda prompt (Anaconda 3) as Administrator. 

Create and activate a virtual environment such as `pytep_env` with Python3.7.

.. code-block:: bash

	conda create -n yourenvname python=3.7 anaconda
	source activate yourenvname

Once the virtual environment is created and the MATLAB path has been obtained, change directories to the MATLAB engine path and run setup.py, whilst pointing it towards the locations of your virtual environment (execute the following while your newly created virtual envirnoment is active).

.. code-block:: bash

	cd /usr/local/MATLAB/R2019b/extern/engines/python
	python setup.py install –prefix="Path to your virtual environment\yourenvname"

Step 3 - Validating the MATLAB engine install
---------------------------------------------

Whilst in the virtual environment, type `python` to obtain a Python shell

.. code-block:: python

	import matlab.engine
	eng = matlab.engine.start_matlab()
	eng
	'matlab.engine.matlabengine.MatlabEngineobject at 0x7f3424ae9f50'

If the MatlabEngineobject is created, you have successfully installed the MATLAB engine for Python in your virtual environment, and you’re ready to install pytep.

Installing pyTEP
================

Using pip
---------

pyTEP is available on PyPI (https://pypi.org/project/pytep/).
We recommend using the pip install unless you have a really good reason not to. 
You can install using pip like this:

.. code-block:: bash

	pip install pytep

Validating installation
-----------------------

Once pyTEP has been installed, it can be validated by running a simple
simulation using the following sequence. Note that `si.setup()` takes
a while because it starts the matlab engine and loads the TEP Simulink model.
Be aware that you only need to call `si.setup()` once when you use pyTEP. 
Once `si.setup()` is called, you can always reset the simulation environment using
`si.reset()`, which is much faster.

.. code-block:: python

   >>> import pytep.siminterface as siminterface
   >>> si = siminterface.SimInterface()
   >>> si.setup()
   <pytep.siminterface.SimInterface object at 0x7fac07e2a4d0>
   >>> si.set_idv(1, 0.5)
   >>> si.simulate(1)
   >>> si.get_idv(1)
   0.5
   
For a more thorough validation you can navigate to the directory where pytep is installed and run some tests. 
If you installed using pip, that will look something like this:

.. code-block:: 

	(base)    source path_to_your_environment/bin/activate
	(yourenv) cd path_to_your_environment/lib/python3.7/site-packages/pytep
	(yourenv) pytest

If `pytest` doesn't work, try `python -m pytest`.

Issues - Look here first
========================

Wrong MATLAB/Simulink version
------------------------------

pyTEP is built and distributed for Python3.7 and MATLAB/Simulink 2019b. 
The default installation assumes that you meet these requirements (this includes the version of the installed Matlab engine for python). 

If you use one of the following MATLAB versions - R2019a, R2020a, R2020b - you should also be able to use pyTEP. 
In order to do so, you need to navigate to the simulator directory inside your pytep package directory (in your virtual environment)

.. code-block:: 

	cd path_to_your_environment/lib/python3.7/site-packages/pytep/simulator
	
`pyTEP` uses the `MultiLoop_mode3.mdl` and `TElib.mdl` files. These must belong to the correct MATLAB/Simulink version. 
For MATLAB R2019a, you can simply rename the existing `MultiLoop_mode3_R2019a.mdl` and `TElib_R2019a.mdl` to `MultiLoop_mode3.mdl` and `TElib.mdl`, respectively.
For MATLAB R2020a or R2020b, you will need to open the model files in Simulink and save them. Simulink should then prompt you to save them in the newer version. 
For pyTEP to work it is important that the files that belong to your version of MATLAB are named `MultiLoop_mode3.mdl` and `TElib.mdl`.


Recompiling the TEP binaries
----------------------------

In some circumstances, the TEP simulink binaries for MATLAB must be
recompiled for the given system. This can be achieved by opening the
MATLAB console and navigating to `pytep/simulator` and calling

.. code-block:: matlab

	mex temexd_mod.c

which will create `temexd_mod.mexa64`, which requires ``gcc`` (or
any other c compiler) in order to be compiled.

Installing Python 3.7
---------------------

The following sequence is instructions for installing the Python3.7
interpreter.

.. code:: bash

   sudo apt install software-properties-common
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   sudo apt install python3.7
