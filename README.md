arduino-autoflasher
===================

This is an attempt to automate the flow of building and flashing firmwares for Arduinos connected to Raspberry Pis. I got tired of building the Arduino binary in the Arduino IDE on my Mac, scp:ing the firmware to the Pi and then running a script on the Pi to reset the AVR and run avrdude.

First edit avr-reset.py so it pulls the correct pin for resetting your Raspberry Pi connected Arduino. Then copy avrreset, avr-reset.py and flashserver.py to your Raspberry Pi.

On your pi:

    % chomod +x avrreset avr-reset.py flashserver.py
    % sudo cp avrreset avr-reset.py /usr/local/bin
    % ./flashserver-py

On your computer running the Arduino IDE:

    <build Arduino binary>
    % ./flashclient.py --host <rpi ip> </path/to/arduino.hex>

Host and port may be configured and a secret may be added that the client and server must agree on for flashing to start.

Bonus: if using fswatch (github.com/emcrisostomo/fswatch) you can have the Arduino firmware automatically uploaded and flashed after building it in the IDE. eg.

    % fswatch /var/folders/sk/0r9hjmx17r9_kls1zp3xddj00000gp/T/build3365321683727688908.tmp/MySketch.cpp.hex | xargs -n1 -J% ./flashclient.py  --host 172.16.3.124 %

Dependencies
------------

* flashclient.py is build on the exeptional Python Requests (python-requests.org)
* flashserver-py needs Tornado (tornadoweb.org) and of course
avrdude (nongnu.org/avrdude)
* avr-reset.py uses the RPi.GPIO package (pypi.python.org/pypi/RPi.GPIO)