# Data Processing for OsciSenForce 
The following software controls the OsciSenForce testing system (VTE Therapy Device Testing Tool) at OsciFlex. This software is written in Python, both on the processing and "user interface" sides.  





This repository contains files relating to the OsciFlex LLC's OsciPulse minimum viable product User Interface. The user interface was entirely designed in the C++ language, as an Arduino microprocessor was used for the MVP. This software takes a variety of inputs from the user via buttons on the OsciPulse device, processes said inputs, and outputs results directly to the OLED screen on the front. The result is an intuitive first iteration of a user interface that can be further improved with higher resolution screen and aesthetic design.

This group of software also includes the control of the motor in the OsciPulse device to apply a force to the end user's leg. The code for control of the screen is directly connected to the motor control, allowing for seamless device control.
