# webcam-theremin
A modular musical instrument played with hand gestures detected from a webcam feed. Uses OpenCV and MediaPipe in Python for hand detection &amp; tracking, and Pure Data for sound synthesis. [See a video demonstrating the instrument here](URL "https://youtu.be/lhVT2A8Nzn8")

## Requirements
[Mediapipe](URL "https://google.github.io/mediapipe/getting_started/python.html")
```
pip install mediapipe==0.8.9.1
```

[Open CV](URL "https://github.com/opencv/opencv/wiki")
```
pip install opencv-python==4.5.5.64
```

[Pure Data](URL "https://puredata.info/downloads/pure-data")

## Getting Started
After opening one of the Pure Data patches in the Pd folder, run the Python script. This will start the webcam and you will then be able to use hand gestures to control synths in Pure Data. By default, all control is done with the the tip of the index finger of the detected hand.

## Modules
The Pure Data components of this instrument are modular, and can be wired together in many different ways. The functionality of each module has been kept to a minimum - for all intents and purposes, each module does one thing and one thing only. This allows for lots of flexibility when it comes to creating/modifying patches and extending existing functionality/adding more modules.

<img width="1100" alt="Example Patch" src="https://user-images.githubusercontent.com/85010533/164815483-94576335-e1e7-454e-9477-c8f1f3b7676f.png">

Below is a list of the modules included and a brief description of each's functionality.

- ```get_hand_position``` Listens for detected x and y position of fingertip (each a floating-point number between 0 and 1) and outputs each on left and right outlets respectively

- ```position_to_frequency``` Takes the x position of the fingertip (a floating point number between 0 and 1) and outputs a number representing the frequency of a note in Hz and the range of the instrument in semitones. Has controls for the range of the instrument in semitones, the lowest pitch of the instrument in Hz, and an option to snap all frequencies to the nearest semitone.
- ```send_range``` Sends the range of the instrument in semitones over websocket. Is used in the Python script in all provided patches here to draw "fret markers" on the screen representing the point at which a note is perfectly in tune.
- ```frequency_interpolation``` Takes a stream of frequencies and takes a user-specified amount of time to output interpolated values between each frequency. Makes for a very smooth glissando between notes.
- ```oscillators~```Takes a frequency and outputs an oscillating signal. Has controls for register, tuning, volume, as well as controls for selecting and controlling different oscillator types:
    - Sine
    - Saw
    - Fixed Width Pulse (Square), including option for pulse width
    - PWM, including options for pulse depth and speed
- ```organ_synth~```Takes a frequency and outputs an oscillating signal made up of up to twelve oscillators, or "organ stops", each operating at a multiple of the given frequency, similar to partials in the harmonic series. Has controls for register, tuning, volume, volume of each "stop", and oscillator type (sine, saw, or square).
- ```position_to_freq_mod~```Takes a frequency and the position of the fingertip (y position in all patches provided) and modulates the frequency, creating a vibrato effect. The position of the fingertip controls the depth of the modulation.
    - **Speed** controls the modulation speed in Hz
    - **Max Depth** controls the maximum depth of the modulation
    - **Waveform** controls the shape of the modulation (sine, saw, or square)
    - **Zero-Depth Position on Screen** controls the position on the screen at which the depth of the modulation will be at zero
    - **Max-Depth Position on Screen** controls the position on the screen at which the depth of the modulation will be at its greatest
    - **Interpolation Speed** controls the amount of time taken to transition between modulation depths
- ```position_to_filter~```Takes a frequency and the position of the fingertip (y position in all patches provided) and filters the signal. The filter's frequency is controlled by the position of the fingertip. Has controls for low frequency, high frequency, low frequency position on screen, high frequency position on screen, resonance, interpolation speed and bypass.
- ```position_to_volume~```Takes a frequency and the position of the fingertip (y position in all patches provided) and changes the amplitude of the signal using the fingertip's position. Has controls for -infinity gain position on screen, unity gain position on screen, interpolation speed and bypass.
- ```kb_amplitude_envelope~```Takes a signal and uses MIDI note-on/note-off messages (from any note) to control an envelope that affects the amplitude of the signal. Has controls for attack, hold, decay, sustain, release and bypass.
- ```kb_filter_envelope~```Takes a signal and uses MIDI note-on/note-off messages (from any note) to control an envelope that filters the signal. Has controls for initial frequency, peak frequency, sustain frequency, end frequency, resonance, attack, hold, decay, release and bypass.
- ```kb_dynamic_range~```Takes a signal and MIDI velocity messages to control the amplitude of the signal. The dynamic range slider controls how much the velocity affects the signal.
- ```frequency_modulation~```Takes a frequency and modulates it to create a vibrato effect. Has controls for speed, depth, waveform (sine/saw/square) and bypass.
- ```amplitude_modulation```Takes a signal and modulates its amplitude.  Has controls for speed, depth, waveform (sine/saw/square) and bypass.
- ```delay~```A simple delay/echo with controls for delay time, feedback, LPF frequency, HPF frequency, volume and bypass.
- ```reverb~```Takes a mono signal and outputs a stereo signal. A simple reverb with controls for volume, feedback, high-frequency damping, damping crossover frequncy and bypass.
