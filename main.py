import machine
import time
import sys
import usb.device
from usb.device.midi import MIDIInterface

# 1. Hardware pin mapping for Arduino Nano ESP32 in MicroPython
# A0 -> Pin(1), A1 -> Pin(2), A2 -> Pin(3), A3 -> Pin(4)
PINS = [1, 2, 3, 4]
MIDI_CCS = [20, 21, 22, 23] # Associated MIDI Control Change numbers
CHANNEL = 176 # 176 = CC Ch. 1

# 2. Initialize ADC channels
sliders = []
for pin in PINS:
    adc = machine.ADC(machine.Pin(pin))
    adc.atten(machine.ADC.ATTN_11DB) # 0 to 3.3V range
    sliders.append(adc)

# 3. Filter parameters and state arrays
beta = 0.2 # Smoothing factor (0.05 = smooth/slow, 0.9 = fast/noisy)
num_sliders = len(sliders)

# Initialize states for each slider
smoothed_vals = [s.read() for s in sliders]
last_midi_vals = [-1] * num_sliders

# 4. Init MIDI interface
m = MIDIInterface()
usb.device.get().init(m, builtin_driver=True)

print(f"--- MICROPYTHON 4-SLIDER MIDI CONTROLLER ({num_sliders} CHANNELS) ---")

while True:
    for i in range(num_sliders):
        # A. Read raw ADC (0-4095)
        raw_val = sliders[i].read()
        
        # B. Exponential moving average filter
        smoothed_vals[i] = (raw_val * beta) + (smoothed_vals[i] * (1 - beta))
        
        # C. Map 12-bit range (0-4095) to 7-bit MIDI range (0-127)
        midi_val = int(smoothed_vals[i] / 32.25)
        
        # Clamp values within strict MIDI limits
        if midi_val > 127: midi_val = 127
        elif midi_val < 0: midi_val = 0
        
        # D. Send MIDI message only if value changes
        if midi_val != last_midi_vals[i]:
            # print("MIDI:", midi_val)

            # Control Change message (176 = CC Ch. 1, MIDI_CCS[i] = CC Number, midi_val = Value)
            #msg = bytes([CHANNEL, MIDI_CCS[i], midi_val])
            #sys.stdout.write(msg)
            m.control_change(CHANNEL, MIDI_CCS[i], midi_val)
            
            last_midi_vals[i] = midi_val
            
    # Short delay to balance response time and stability
    time.sleep(0.005)