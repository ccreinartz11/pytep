.. role:: raw-latex(raw)
   :format: latex
..

pyTEP: Interactive Tennessee Eastman process simulator
====================================================================================

.. raw:: html

   <!-- TOC -->

-  `pyTEP: A Python package for interactive simulations of the Tennessee
   Eastman
   process <#pytep-a-python-package-for-interactive-simulations-of-the-tennessee-eastman-process>`__
-  `What is pyTEP? <#what-is-pytep>`__

   -  `How to cite <#how-to-cite>`__

-  `Installation guidelines <#installation-guidelines>`__
-  `MATLAB engine installation
   guidelines <#matlab-engine-installation-guidelines>`__

   -  `Step 1) Locate the MATLAB install
      path <#step-1-locate-the-matlab-install-path>`__
   -  `Step 2) Installing the MATLAB
      engine <#step-2-installing-the-matlab-engine>`__

      -  `Linux <#linux>`__
      -  `Windows (Using anaconda
         prompt) <#windows-using-anaconda-prompt>`__

   -  `Step 3) Validating the MATLAB engine
      install <#step-3-validating-the-matlab-engine-install>`__

-  `Installing pyTEP through pip <#installing-pytep-through-pip>`__

   -  `Validating installation <#validating-installation>`__

-  `Misc <#misc>`__

   -  `Recompiling the TEP binaries <#recompiling-the-tep-binaries>`__
   -  `Installing Python 3.7 <#installing-python-37>`__

.. raw:: html

   <!-- /TOC -->

What is pyTEP?
--------------

pyTEP is an open-source simulation API for the Tennessee Eastman process
in Python. It facilitates the setup of complex simulation scenarios and
provides the option of interactive simulation.

Through pyTEPs high-level API, users can setup simulations, change
operating conditions and store simulation data without being exposed to
the underlying mechanics of the simulator. In addition to the newly
introduced features, pyTEP promises more versatility and more
straightforward usage that existing TEP simulators.

How to cite
-----------

::

   Reinartz, C. and Enevoldsen, T.T. "pyTEP: A Python package for interactive simulations of the Tennessee Eastman process", 2021

Installation guidelines
=======================

In order to install and run pyTEP, the MATLAB engine for pythong must be
installed, which requires the following conditions to be met: - A
licensed (and activated) MATLAB/Simulink installation (Tested with 2019a
and 2020b) - Python 3.7 - (Optional) virtual Python environment

It is highly recommended to install pyTEP within a virtual environment.

Summary of installation steps

1. Create a virtual environment with Python3.7
2. Install the MATLAB engine into the virtual environment
3. pip install pytep

MATLAB engine installation guidelines
-------------------------------------

Step 1) Locate the MATLAB install path
--------------------------------------

Finding the MATLAB install path can either be done by searching through
the file system, or executing
``fullfile(matlabroot,'extern','engines','python')`` in the MATLAB
console.

The resulting path will look similar to ``'/usr/local/matlab/r2019b/extern/engines/python'``

Step 2) Installing the MATLAB engine
------------------------------------

   ### Linux

   Create a virtual environment such as ```pyTEPenv``` with Python3.7, take note of the location of which the virtual environment is created (e.g. ```/home/USER/.venvs/pyTEPenv```).

   Once the virtual environment is created and the MATLAB path has been obtained, change directories to the MATLAB engine path and run setup ```setup.py```, whilst pointing it towards your virtual environment

cd /usr/local/MATLAB/R2019b/extern/engines/python sudo python3.7
setup.py install –prefix=“/PATH/TO/VENVDIR/pyTEPenv”

::


   ### Windows (Using anaconda prompt)

   Open the Anaconda prompt (Anaconda 3) as Administrator. 

   Create and activate a virtual environment such as '''pyTEPenv''' with Python3.7.

conda create -n yourenvname python=3.7 anaconda source activate
yourenvname

::

   Once the virtual environment is created and the MATLAB path has been obtained, change directories to the MATLAB engine path and run setup ```setup.py```, whilst pointing it towards the locations of your virtual environment (execute the following while your newly created virtual envirnoment is active).

cd /usr/local/MATLAB/R2019b/extern/engines/python python setup.py
install –prefix=“Path to your virtual
environment:raw-latex:`\yourenvname`”

::


   ## Step 3) Validating the MATLAB engine install
   Whilst in the virtual environment, type ```python``` to obtain a Python shell

..

         import matlab.engine eng = matlab.engine.start_matlab() eng
         ``A MALTAB engine object should then be successfully created:``\ <matlab.engine.matlabengine.MatlabEngine
         object at 0x7f3424ae9f50>``\`

The MATLAB engine for Python has now been successfully installed in your
virtual environment, and you’re now ready to install pyTEP itself.

Installing pyTEP through pip
============================

pyTEP is available on pypi (https://pypi.org/project/pytep/)

::

   pip install pytep

Validating installation
-----------------------

Once pyTEP has been installed, it can be validated by running a simple
simulation using the following sequence. Note that ``si.setup()`` takes
a while due to loading the TEP Simulink model.

::

   >>> import pytep.siminterface as siminterface
   >>> si = siminterface.SimInterface()
   >>> si.setup()
   <pytep.siminterface.SimInterface object at 0x7fac07e2a4d0>
   >>> si.set_idv(1, 0.5)
   >>> si.simulate(1)
   >>> si.get_idv(1)
   0.5

Misc
====

Recompiling the TEP binaries
----------------------------

In some circumstance, the actual TEP binaries for MATLAB must be
recompiled for the given system. This can be achieved by opening the
MATLAB console and navigating to ``pytep/simulator`` and calling

::

   mex temexd_mod.c

which will then create ``temexd_mod.mexa64``, which requires ``gcc`` (or
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
