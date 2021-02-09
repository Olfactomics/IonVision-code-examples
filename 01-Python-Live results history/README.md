# Python scan result history visualiser
This Python script monitors when IonVision finishes scanning, downloads the new scan results and
visualises them in a "stack" together with a history or previous results. With the way the
visualisation of a single scan result is designed to stack with multiple results in a 2D spectrum,
the scan results should be 1-dimensional (only usv or ucv changes). More dimensions are supported
but they all are rendered as one long, continuous row.

## Usage
The script requires installing some Python packages. The required packages are listed in the
standard `requirements.txt` file. The easiest way to install multiple dependencies for a single
script is to use a virtual environment, but any setup familiar to you is fine. To install launch the
script using a virtual environment:

1. Create a new virtual environment:

Windows
```
python -m venv .pyenv
```

Linux
```
python3 -m venv .pyenv
```

2. Activate the virtual environment

Windows
```
.\.pyenv\Scripts\activate
```

Linux
```
source .pyenv/bin/activate
```

3. Install the requirements to your virtual environment

```
pip install -r requirements.txt
```

4. Remember to edit the script with the IP address of your IonVision device and possible other settings

5. Start your IonVision device and select the parameters you want to us

6. Launch the script

```
python visualiser.py
```

7. Start scanning, a visualisation of the results should start appearing in a new window

## Things to consider when using
 - The IP address of your IonVision device must be edited to the `IONVISION_ADDRESS` variable in the script
 - The IonVision device must be turned on before starting the script
 - To stop the script, press ctrl+c in the terminal window
 - Only properly supports 1-dimensional result data
 - The size of the result data can not be changed without restating the script