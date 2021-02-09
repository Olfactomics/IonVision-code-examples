# IonVision script examples
This repository contains examples of using IonVision through its HTTP and WebSocket APIs. Many of
the scripts could be used as-is, but hopefully they also provide good examples and inspiration for
writing your own scripts to utilise the IonVision device in novel ways!

## Repository structure
The examples scripts are divided into their own folders each containing a single script in one
programming language. Many examples are available in multiple languages. Each type of example is
numbered and that number is placed at the start of the folder name. After that the folder name lists
the language that version of the example is in. Finally the name of the type of the example script
is listed.

## Included examples

### Live result history
A script that visualises multiple 1-dimensional scan results in real time. Uses both the WebSocket
and HTTP APIs. Could be used as a base for any kind of scripts reacting on events from the WebSocket
API. Also provides an example of downloading and very lightly processing scan result data from the
HTTP API.

 - **Python** `01-Python-Live results history`