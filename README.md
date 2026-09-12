# Midi Controller
_Micro python code for arduino to create a midi contoller with slider_

The aim of this project is to create a plug and play USB midi device to control any DAW or VST software.

The hardware part is composed of an ESP32 Nano Arduino due to it ability to handle plug-and-play USB generic midi device capabilities. 

Then, sliders (3 pins sliders) are connected to the analog inputs of the Arduino board. And that's all, no other component is needed. You can choose which slider you want while it's a 3 pin slider. 

The signal smoothering is done programatically in the python code, no other electronic component is needed. 

The Arduino LED is used to get the device status.

# Hardware connection scheme
Here is the connection shceme for 1 slider on the A0 Arduino Nano analog input.

| Slider pin          | Arduino Nano ESP32 pin    | Role                    |
|---------------------|---------------------------|-------------------------|
| Pin 1               | GND                       | Ground (0V)             |
| Middle pin (slider) | A0                        | Analog signal           |
| Pin 2               | 3.3V (VCC)                | Power supply (3.3V)     |

On 3 pins sliders with pin number #1-#2-#3, the connection scheme is usually:
* PIN 1 GND
* PIN 2 Analog output (to A0)
* PIN 3 VCC

Note: other sliders can be added on the A1, A2, A3, A4, A5, A6, A7 inputs.

# Flashing the Arduino with the right micro python version
Install micro python using this flashing software:
https://labs.arduino.cc/en/labs/micropython-installer

Then add the usb-device-midi package (https://github.com/micropython/micropython-lib/tree/master/micropython/usb/usb-device-midi) using the python packet uploader software (https://labs.arduino.cc/en/labs/micropython-package-installer), or the Arduino.Lab.for.MicroPython IDE (https://labs.arduino.cc/en/labs/micropython).

# Uploading the firmware
Upload the 'main.py' file to the Arduino using the Arduino.Lab.for.MicroPython IDE (https://labs.arduino.cc/en/labs/micropython)

# Usage
Connect to your computer, it should be seen in your midi compatible software as a standard usb midi device.

Enjoy !!!


# Customisation
_TODO: add config file to manage default CC channel and CC numbers_