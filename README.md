# tappipe
Python library for decoding Tigo TAP->CCA RS485 Power Report packets
More info available at https://github.com/kicomoco/tappipe

A big thank you to willglyn (https://github.com/willglynn/taptap) whose work in documenting the protocol and taptap program (written in rust) allowed me to create this python version.

## PIP
This package has been built and uploaded to pypi, and can be installed with pip.
```
pip install tappipe
```
Please Note: obviously this command may be different on your system, pip, pip3, python -m pip, python3 -m pip....adjust as necessary!

## Example Scripts
In the examples folder is an example mqtt script, that takes command line arguments for specifying MQTT server and the serial port to open
```
usage: tappipe [-h] -s MQTT_SERVER [-p MQTT_PORT] [-u MQTT_USERNAME]
               [-w MQTT_PASSWORD] -t MQTT_PREFIX -c SERIAL_PORT
```

## What is returned?
The processor takes a byte array (in the mqtt example it is read from the serial port), and when it has a valid frame this is returned as an object.

Within the object it can be checked for the type of frame, the type of pv data (if exists), cmd type etc and then access the data packets in a parsed format for Power Reports.

## TODO
- Implement logging using a logging module rather than print
- Implement unit testing so can check nothing breaks with each revision