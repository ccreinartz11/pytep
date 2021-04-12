# MATLAB engine installation guidelines
In order to install and run pyTEP, the MATLAB engine for pythong must be installed, which requires the following conditions to be met:
- A licensed (and activated) MATLAB/Simulink installation (Tested with 2019b and 2020b)
- Python 3.7
- (Optional) virtual Python environment
  
It is highly recommended to install pyTEP within a virtual environment.

### Step 1) Locate the MATLAB install path
Finding the MATLAB install path can either be done by searching through the file system, or executing ```fullfile(matlabroot,'extern','engines','python')``` in the MATLAB console.

The resulting path will look similar to 
```'/usr/local/MATLAB/R2019b/extern/engines/python'```

### Step 2) Installing the MATLAB engine

#### Linux

Create a virtual environment such as ```pyTEPenv``` with Python3.7, take note of the location of which the virtual environment is created (e.g. ```/home/USER/.venvs/pyTEPenv```).

Once the virtual environment is created and the MATLAB path has been obtained, change directories to the MATLAB engine path and run setup ```setup.py```, whilst pointing it towards your virtual environment
```
cd /usr/local/MATLAB/R2019b/extern/engines/python
sudo python3.7 setup.py install --prefix="/PATH/TO/VENVDIR/pyTEPenv"
```

#### Windows (Using anaconda prompt)

Open the Anaconda prompt (Anaconda 3) as Administrator. 

Create and activate a virtual environment such as '''pyTEPenv''' with Python3.7.
```
conda create -n yourenvname python=3.7 anaconda
source activate yourenvname
```
Once the virtual environment is created and the MATLAB path has been obtained, change directories to the MATLAB engine path and run setup ```setup.py```, whilst pointing it towards the locations of your virtual environment (execute the following while your newly created virtual envirnoment is active).
```
cd /usr/local/MATLAB/R2019b/extern/engines/python
python setup.py install --prefix="Path to your virtual environment\yourenvname"
```

### Step 3) Validating the MATLAB engine install
Whilst in the virtual environment, type ```python``` to obtain a Python shell
```
>>> import matlab.engine
>>> eng = matlab.engine.start_matlab()
>>> eng
```
A MALTAB engine object should then be successfully created:
```<matlab.engine.matlabengine.MatlabEngine object at 0x7f3424ae9f50>```
## Misc
### Recompiling the TEP binaries
FIND THE ERROR MESSAGE

Calling
```
mex temexd_mod.c
```
will create temexd_mod.mexa64, which requires ```gcc``` (or any other c compiler) in order to be compiled.
### Installing Python 3.7
ADD TEXT FOR PYTHON 3.7 INSTALL
```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7
```

