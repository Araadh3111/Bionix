# Bionix 

An open-source, EMG-controlled bionic hand engineered for the IRIS National Science Fair. Bionix features a custom tendon-driven mechanical design, frictionless brass-rod joints, and an antagonistic elastic return system.

## Overview
Bionix translates raw electromyography (EMG) signals from the user's forearm into precise, articulated finger movements. The system uses a Raspberry Pi Pico to process analog muscle signals and distribute PWM control to a 5-servo array housed inside a custom 3D-printed palm cavity. 

## Features
* **Tendon-Driven Kinematics:** Uses high-tensile braided lines for active flexion and a shock-cord elastic system for passive extension, eliminating the "bowstring" effect.
* **Low-Friction Joints:** Completely screwless 3D-printed phalanges rotating on smooth 2.2mm solid brass dowel pins.
* **Myoelectric Control:** Integrated MyoWare 2.0 sensor for direct muscle-to-machine actuation.
* **Modular Power:** Safely steps down a 7.4V 2S Li-ion battery to 5V (via a 3A+ buck converter) to handle maximum servo stall torque without browning out the logic board.

## System Architecture & Diagrams

### Circuit Design
<img width="1212" height="1078" alt="Screenshot 2026-06-17 201810" src="https://github.com/user-attachments/assets/5a327cd5-b3e8-4db6-a252-3d87760bdd63" />

### Assembled Design 
<img width="1918" height="1078" alt="image" src="https://github.com/user-attachments/assets/fea72298-4da7-4a97-9010-2b1c27e1de03" />

## File Structure

\`\`\`text
Bionix/
├── .git/                 # Git repository data
├── CAD/                  # Fusion 360 models, assemblies, and STL files for 3D printing
├── circuit design/       # KiCad schematics (Peak.kicad_sch) for power and signal routing
├── Code/                 # Control software for the Raspberry Pi Pico
├── BOM.xlsx              # Complete Bill of Materials and cost breakdown
└── README.md             # Project documentation (You are here)
\`\`\`

## Hardware Requirements
* Raspberry Pi Pico (RP2040/RP2350)
* 5x Micro Servos (SG90/MG90S)
* 1x MyoWare 2.0 Muscle Sensor & Disposable Electrodes
* 1x 5V Buck Converter (>= 3A Output) & 2S Li-ion Battery
* 3D Printed Parts (PLA/PETG recommended)
* *For a full parts list, cost breakdown, and assembly hardware, please refer to the `BOM.csv` file.*
