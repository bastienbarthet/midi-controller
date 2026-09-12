# Midi Controller
_Micro python code for arduino to create a midi contoller with slider_

The aim of this project is to create a plug and play USB midi device to control any DAW or VST software.

The hardware part is composed of an ESP32 Nano Arduino due to it ability to handle plug-and-play USB generic midi device capabilities. Then sliders (3 pins sliders) are connected to the analog inputs of the Arduino board. And that's all, no toehr component is needed. You can choose which slider you want while it's a 3 pin slider. The signal smoothering is done programatically in the python code, no other electronic component is needed. The Arduino LED is used to get the device status.

# Hardware connection scheme
Here is the connection shceme for 1 slider on the A0 Arduino Nano analog input.

| Slider pin          | Arduino Nano ESP32 pin    | Role                    |
|---------------------|---------------------------|-------------------------|
| Pin 1               | GND                       | Ground (0V)             |
| Middle pin (slider) | A0                        | Analog signal           |
| Pin 2               | 3.3V (VCC)                | Power supply (3.3V)     |

Other sliders can be added on the A1, A2, A3 etc inputs.

# Flashing Arduino with the right micro python version
TODO

# Uploading the firmware
TODO

# Usage
TODO

# Customisaiton
TODO