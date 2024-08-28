# ArduinoSynth
This repository was made to keep track of the code and related files for a pysically built digital synthesizer circuit making use of an Arduino Uno R4 WiFi. The code and files for a software app that allows users of the synthesizer to customize its waveform via bluetooth are also hosted in this repository. The image below shows the general overview of the project.
![](assets/Overview.png)

## Hardware Overview
- The synth uses push button inputs wired to the Arduino Uno's digital input pins, and utilizes the Arduino board's built in pull-up resistors. These buttons allow individual notes to be played (see the [Software Overview](#Software-Overview) section of this file for information on the software implementation of these inputs).
- A 3.5mm Aux port was added to the pysical synth design to facilitate audio output. Both left and right audio outputs were tied to the same souce for this project. A lowpass filter was also implemented in order to decouple the DC offset from the Arduino's DAC for the AC waveform desired for playback.

## Software Overview

## Sound Demo
