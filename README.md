# ECE Capstone Spring 2023: B-I-K-E
**Best in Kard Entertainment**
Members: 
<ul>
<li>Sharwin Patil (CECS)</li>
<li>Connor Nelson (CECS)</li>
<li>Chris Swagler (CECS)</li>
<li>Tyler Passerine (CECS)</li>
<li>Adin Moses (ECE)</li>
<li>Jackson Heun (EE + Physics)</li>
</ul>

# Update (April 11, 2023):
We won first place at the ECE Capstone Expo and impressed industry judges with our blend of hardware/software solutions.

# Project Description
Our goal is to build an automated robotic poker table that will handle most of the functions a human dealer would, such as shuffling, dealing, and facilitating the game.

## Technology Stack
### Raspberry Pi 4B
The main compute for the B-I-K-E Poker Table is a Rasperry Pi 4B. The Pi is operating on native Ubuntu and will run our main program written in Python (3.10.6). The main program will facilitate the Poker logic and delegate low-level control to Arduino Unos and a Nucleo 32 via serial connection.
### Arduino Unos
The Unos will control motors and sensors for both the Card-Turret and Auto-Shuffler. A custom communication layer lies between the Arduinos and the Pi to ensure correct command execution and completion. Each Arduino is running C++ utilizing our own custom-built Stepper-Motor Controller Library.
### Arduino Nano
The Nano handles I/O control for the 4 button panels which enable players to provide input when playing Poker. Each button panel offers an I/O chip equipped with I2C and an interrupt pin. Our custom interfacing code translates the data over I2C into poker inputs for the Pi to operate upon.

