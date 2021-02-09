"""
Licensed under the MIT license.

Copyright © 2021 Olfactomics Oy

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the “Software”), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import json
import time

import asyncio
import websockets

import requests

import matplotlib
import matplotlib.pyplot as plt
from PySide2 import QtCore  
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np

# -- Set some Matplotlib global settings --
# Use Qt for Python/Pyside2 backend for rendering the plot window
matplotlib.use("Qt5Agg")
# Disable plot window controls as they don't work without additional code that would redraw the window
matplotlib.rcParams["toolbar"] = "None"

# -- These globals can/must be edited to customise how the script works --
# Set the IP address of the IonVision device in your local network here
IONVISION_ADDRESS = "localhost"#"192.168.0.10"
# This controls how many results are show in the history plot at once
HISTORY_LENGTH = 10
# Controls which intensity is visualised, IntensityTop or IntensityBottom
USED_INTENSITY="IntensityTop"

# -- These globals are automatically generated and should not be edited --
# The base address for the IonVision HTTP API
API_ADDRESS = "http://{}/api".format(IONVISION_ADDRESS)
# The address of the IonVision WebSocket API
WS_ADDRESS = "ws://{}/socket".format(IONVISION_ADDRESS)

class Plot:
    """
    This class stores the state of the history plot being drawn.
    """
    def __init__(self):
        """
        Initialising the class mainly pre-creates the Matplotlib plot.
        """
        self._fig, self._ax = plt.subplots()
        self._history_data = None
        self._colour_bar = None
        """ 
        Disable close button from the plot window frame as it won't work without additional code
        that would redraw the window
        """
        plt.gcf().canvas.parent().setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

    def update(self):
        """
        Update the plot with the newest scan result data from the IonVision device. The method
        automatically fetches the result data from the HTTP API.
        """
        # Get the intensity data of the latest scan result
        intensity = self._get_latest_intensity()
        first_time = False

        # Initialise the history data with the correct intensity data size
        if self._history_data is None:
            first_time = True
            self._history_data = np.zeros((HISTORY_LENGTH, len(intensity)))

        # Shift history data up by 1 row and place the new intensity data to the first slot
        new_history = np.empty_like(self._history_data)
        new_history[1:] = self._history_data[:-1]
        new_history[0] = intensity
        self._history_data = new_history

        # Discard old history data and draw in the new data
        self._ax.clear()
        mesh = self._ax.pcolormesh(self._history_data, shading="auto", cmap="Spectral_r")

        # Remove old colourbar and create a new one with the current colour scale
        if not self._colour_bar is None:
            self._colour_bar.remove()
        self._colour_bar = self._fig.colorbar(mesh, ax=self._ax)

        # Draw the changes to the plot and pause to let it process the updates
        plt.draw()
        plt.pause(0.001)
        print("Plot data updated")

    def _get_latest_intensity(self) -> list:
        """
        Fetch the intensity data of latest scan result from the IonVision HTTP API.
        :returns: The latest intensity data.
        """
        response = requests.get(API_ADDRESS + "/results/latest")
        response.raise_for_status()
        result_data = response.json()
        return result_data["MeasurementData"][USED_INTENSITY]

async def process_ws_messages(uri: str, plot: Plot):
    """
    This function asynchronously checks for WebSocket messages from IonVision and loads new scan
    result data when it becomes available after a new scan has been finished.

    :param uri: The IonVision WebSocket URI.
    :param plot: An instance of the plot state of this script.
    """
    async with websockets.connect(uri) as websocket:
        while True:
            message = json.loads(await websocket.recv())
            if message["type"] == "scan.resultsProcessed":

                """
                On older systems or in more intensive applications, processing the WS mesages can
                take too long and cause messages to pile up. If that happens, one solution is to
                compare the WS message timestamp with the time when the message is processed and
                discard too old messages.
                """
                if time.time() * 1000 - message["time"] < 500:
                    plot.update()
                else:
                    print("Visualisation lagging behind new results, skipping result")

def main():
    # Initialise the plot state
    plot = Plot()
    # Start the WebSocket message listening loop
    asyncio.run(process_ws_messages(WS_ADDRESS, plot))


if __name__ == "__main__":
    main()