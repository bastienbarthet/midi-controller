import machine
import time
import sys
import usb.device
from usb.device.midi import MIDIInterface

# MIDI configuration --> can be changed to fit you needs
MIDI_CCS = [20, 21, 22, 23] # Associated MIDI Control Change numbers
CHANNEL = 176 # 176 = CC Ch. 1

# Smoothing factor: 0.05 = smooth/slow, 0.9 = fast/noisy --> can be changed to fit your needs
BETA = 0.2
# Temporal smoothing (should be strictly set between 0 and 1)
TETA = 0.8

# Delay between 2 cycles --> should not be changed
DELAY = 0.005
# Hardware pin mapping for Arduino Nano ESP32 in MicroPython, DO NOT TOUCH!
# A0 -> Pin(1), A1 -> Pin(2), A2 -> Pin(3), A3 -> Pin(4)
PINS = [1, 2, 3, 4]
# Initialize ADC channels
sliders = []
for pin in PINS:
    adc = machine.ADC(machine.Pin(pin))
    adc.atten(machine.ADC.ATTN_11DB) # 0 to 3.3V range
    sliders.append(adc)


# Initialize states for each slider
num_sliders = len(sliders)
smoothed_vals = [s.read() for s in sliders]
last_midi_vals = [-1] * num_sliders

# Init MIDI interface
m = MIDIInterface()
usb.device.get().init(m, builtin_driver=True) ## comment this to deactivated midi compliant device

print(f"--- MICROPYTHON {num_sliders}-SLIDER MIDI CONTROLLER ({num_sliders} CHANNELS) ---")

while True:
    for i in range(num_sliders):
        # Read raw ADC (0-4095)
        raw_val = sliders[i].read()
        
        # Exponential moving average filter + custom value change filter
        smoothed_val = (raw_val * BETA) + (smoothed_vals[i] * (1 - BETA))
        if abs(smoothed_val-smoothed_vals[i])/32>TETA:
          smoothed_vals[i] = smoothed_val
        
        # Map 12-bit range (0-4095) to 7-bit MIDI range (0-127)
        midi_val = 127 - int(smoothed_vals[i] / 32)
        
        # Clamp values within strict MIDI limits
        if midi_val > 127: midi_val = 127
        elif midi_val < 0: midi_val = 0
        
        # Send MIDI message only if value changes
        if midi_val != last_midi_vals[i]:
            
            #print(f"Slider: {i}; MIDI: {midi_val}") ## uncomment for debug purpose

            # Control Change message (176 = CC Ch. 1, MIDI_CCS[i] = CC Number, midi_val = Value)
            m.control_change(CHANNEL, MIDI_CCS[i], midi_val)
            
            last_midi_vals[i] = midi_val
            
    # Short delay to balance response time and stability
    time.sleep(DELAY)