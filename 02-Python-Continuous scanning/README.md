# Python continuous scanning script
This script continuously starts new scans on an IonVision device. Make sure to select a project and
load a parameter preset before starting the script. The script supports a few arguments, run it with
the `-h` option to see what they are `python scanner.py -h`. Running the device continuously is
quite useful in certain situations, like when you want to observe something for a longer period or
when just testing out the device. At least at Olfactomics such a script has seen periodic use during
research.

## Usage

```
python3 sniffer.py --address 192.168.10.1
```
Start the script and connect to an IonVision at address 192.168.10.1.

```
python3 sniffer.py --address 192.168.10.1 "A random comment"
```
Start the script as before but add the comment "A random comment xx" to every scan with xx being
replaced by an automatically incremented sequence number.

```
python3 sniffer.py --address 192.168.10.1 --sleep 10.25
```
Start the script as before but wait 10.25 minutes (10m15s) between scans.