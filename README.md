# Real-Time Vehicle Localization System Using UWB

## Project Overview

This project implements a real-time indoor vehicle/tag localization system using Qorvo Ultra-Wideband (UWB) technology and Raspberry Pi 4 computers.

The system uses UWB ranging to measure the distance between a mobile tag and multiple fixed anchors. The measured distances are processed on a Raspberry Pi and used to estimate the two-dimensional position of the mobile tag.

The project was developed in two stages:

1. Three-anchor localization for initial ranging and trilateration validation.
2. Four-anchor localization using Least-Squares Multilateration (LSM) for improved localization reliability.

The system also provides a real-time graphical visualization of the anchor positions, ranging circles, estimated tag position, distances, Time-of-Flight (ToF), angles, and anchor status.

The project was developed as part of a larger Vehicle-to-Everything (V2X) research platform and provides a foundation for integrating UWB localization with robotics and intelligent transportation systems.

---

## Objectives

The main objectives of this project are:

- Develop a real-time indoor localization system using Qorvo UWB technology.
- Configure one mobile tag and multiple fixed anchors.
- Implement FiRa Double-Sided Two-Way Ranging (DS-TWR).
- Obtain real-time distance measurements between the tag and anchors.
- Estimate the mobile tag position using multilateration.
- Implement Least-Squares Multilateration for the four-anchor configuration.
- Develop a Python-based real-time visualization interface.
- Monitor ranging status and measurement updates.
- Provide a modular platform for future robotics and V2X applications.

---

## System Architecture

The system consists of:

- One mobile UWB tag
- Four fixed UWB anchors
- Raspberry Pi 4 computers
- Qorvo UWB development boards
- Python-based ranging data processing
- Trilateration / multilateration algorithms
- Real-time Matplotlib visualization

### Basic Architecture

```text
             UWB Anchor A1
                  |
                  |
             UWB Anchor A2
                  |
                  |
        -----------------------
        |                     |
        |     Mobile Tag      |
        |                     |
        -----------------------
             /          \
            /            \
     UWB Anchor A3    UWB Anchor A4


        UWB Ranging Measurements
                  |
                  v
          Raspberry Pi
                  |
                  v
        Python Data Processing
                  |
                  v
       Multilateration Algorithm
                  |
                  v
        Estimated X,Y Position
                  |
                  v
       Real-Time Visualization


       Development Stages
Stage 1 - Three-Anchor Localization

The initial implementation used:

Three fixed anchors
One mobile tag

Each anchor provided a distance measurement to the mobile tag.

The three measured distances were used for 2D trilateration.

This stage was mainly used to validate:

UWB communication
Distance measurement
FiRa DS-TWR ranging
Real-time data acquisition
Basic position estimation

The three-anchor configuration is simpler but has less redundancy and is more sensitive to ranging errors.

Stage 2 - Four-Anchor Localization

The system was subsequently extended to:

Four fixed anchors
One mobile tag

The additional anchor provides an extra distance measurement, allowing the position to be estimated using a Least-Squares Multilateration approach.

The four-anchor configuration represents the final architecture described in the project report.

The current software is designed to use all available valid anchor measurements rather than inserting artificial distance values.

UWB Communication

The system uses Qorvo UWB development boards for ranging.

The ranging process is based on the FiRa Double-Sided Two-Way Ranging (DS-TWR) protocol.

The UWB devices exchange ranging messages and determine the signal propagation time. This information is used to obtain the distance between the mobile tag and the anchor.

The basic relationship between propagation time and distance is:

d = c × t

Where:

d = distance between the anchor and tag
c = speed of light
t = Time-of-Flight

The Raspberry Pi receives the ranging information and processes it using the Python localization software.

Hardware Components
Component	Quantity	Purpose
Raspberry Pi 4 Model B	5	Embedded processing
Qorvo UWB Development Boards	5	UWB ranging
Mobile UWB Tag	1	Node whose position is estimated
Fixed UWB Anchors	4	Reference nodes
USB Cables	5	Raspberry Pi to UWB connection
microSD Cards	5	Operating system and software
5V/3A Power Supplies	5	Raspberry Pi power

The hardware configuration consists of one mobile tag and four fixed anchors. Each UWB board is connected to a Raspberry Pi through USB.

Software Architecture

The software is divided into modular components.

uwb_localization.py
        |
        +-------------------+
        |                   |
        v                   v
    parser.py          plotter.py
        |                   |
        v                   v
  Ranging Data       Visualization
        |
        v
    config.py
        |
        v
trilateration.py
        |
        v
Estimated Tag Position
Source Code

The main source code is located in:

src/uwb_localization/
1. config.py

Contains the global configuration of the localization system.

It includes:

Anchor coordinates
Anchor names
Distance values
ToF values
Anchor status
Measurement counters
Last update timestamps
Plot limits
Distance limits
Filtering parameters
Timeout settings
Speed of light
Visualization settings

Example anchor configuration:

ANCHORS = {
    "00:01": (0.0, 1.0),
    "00:02": (0.0, 5.0),
    "00:03": (3.0, 1.0),
    "00:04": (3.0, 5.0)
}
2. parser.py

Responsible for acquiring and processing the UWB ranging output.

The parser:

Starts the Qorvo ranging application.
Reads the ranging output.
Detects anchor MAC addresses.
Extracts distance measurements.
Validates the measured distance.
Applies exponential moving average filtering.
Calculates estimated ToF.
Updates anchor status.
Counts successful measurements.
Detects ranging timeouts.

The current configuration requests ranging information from four controlees:

[0x1, 0x2, 0x3, 0x4]

with:

n_controlees = 4
3. trilateration.py

Contains the position estimation algorithm.

The module supports:

Three-anchor trilateration
Four-anchor multilateration
Least-Squares position estimation

For three anchors, the system can estimate a 2D position using the three measured distances.

For four or more measurements, the equations are solved using a least-squares approach.

The main function is:

multilaterate(anchors, distances)

The function returns:

(x, y)

representing the estimated position of the mobile tag.

4. plotter.py

Provides the real-time graphical interface.

The visualization displays:

Anchor positions
Anchor names
Anchor coordinates
Measured distances
Ranging circles
Estimated tag position
Anchor-to-tag lines
Estimated angles
Time-of-Flight
Number of measurements
Anchor status
Current X,Y position

The plot updates continuously while the ranging process is running.

5. uwb_localization.py

This is the main entry point of the application.

It starts:

The UWB ranging parser.
The real-time visualization.

Basic execution flow:

Start Application
       |
       v
Start UWB Parser
       |
       v
Receive Ranging Data
       |
       v
Process Distances
       |
       v
Estimate Tag Position
       |
       v
Display Real-Time Position
Distance Processing

The received ranging measurements are checked before being used for localization.

The software verifies that:

The measurement belongs to a known anchor.
The ranging status is valid.
The distance is within the configured limits.
The measurement is not missing.

The current distance limits are:

Minimum distance = 0.20 m
Maximum distance = 20.00 m
Distance Filtering

UWB measurements may contain small variations due to environmental effects and measurement noise.

An Exponential Moving Average (EMA) filter is therefore used.

The current filtering parameter is:

ALPHA = 0.35

The filtered distance is calculated using the current measurement and the previous filtered value.

This provides smoother ranging values for the localization algorithm and visualization.

Time-of-Flight Calculation

The software also estimates the Time-of-Flight from the filtered distance.

The relationship used is:

t = d / c

where:

t = propagation time
d = measured distance
c = speed of light

The calculated value is displayed in nanoseconds.

Anchor Status Monitoring

Each anchor has a real-time status.

Possible states include:

WAITING
OK
TIMEOUT
WAITING

No successful ranging measurement has been received yet.

OK

A valid ranging measurement has been received.

TIMEOUT

No new measurement has been received from the anchor within the configured timeout period.

The current timeout is:

2 seconds
Three-Anchor Trilateration

In the initial implementation, three anchors were used for 2D localization.

Each anchor provides a distance:

d1
d2
d3

The tag position (x,y) is estimated from the intersection of the corresponding distance circles.

The three-anchor approach requires at least three valid distance measurements for 2D localization.

Advantages
Simple implementation
Lower hardware requirement
Easy system setup
Suitable for initial testing
Limitations
Sensitive to ranging errors
Less redundancy
Lower robustness when measurements are noisy
Four-Anchor Least-Squares Multilateration

The final system uses four anchors.

The measured distances are:

d1
d2
d3
d4

The localization equations are linearized and solved using a least-squares method.

The current implementation builds the system of equations using one anchor as a reference and solves:

A × X = B

using NumPy's least-squares solver.

This produces the estimated tag coordinates:

X = [x, y]

The four-anchor configuration provides an additional measurement compared with the three-anchor system and is intended to improve localization stability and robustness.

Dynamic Anchor Processing

The visualization software does not depend on a fixed artificial distance for the fourth anchor.

Instead, it checks which anchors currently have valid measurements.

If 3 valid anchors:
        Use 3-anchor localization

If 4 valid anchors:
        Use all 4 anchors

If fewer than 3 valid anchors:
        Wait for more measurements

This allows the software to continue operating when one anchor temporarily becomes unavailable.

Real-Time Visualization

The system provides a live 2D localization display.

The visualization includes:

+------------------------------------------------+
|              UWB LOCALIZATION                  |
|                                                |
| A1 ●------------------------● A2               |
|    \          TAG ★         /                  |
|     \                      /                   |
|      \                    /                    |
|       ● A3------------● A4                    |
|                                                |
| Current Position                               |
| X : xx.xx m                                    |
| Y : yy.yy m                                    |
+------------------------------------------------+

The actual graphical interface also displays ranging circles, distances, ToF, angles, status, and measurement counts.

Angle Calculation

The software calculates the angle from each anchor to the estimated tag position.

The angle is calculated using:

angle = atan2(y_tag - y_anchor,
              x_tag - x_anchor)

The calculated angle is displayed next to the corresponding anchor-to-tag line in the visualization.

Experimental Configuration

The final experimental configuration consists of:

Environment       : Indoor laboratory
Mobile Tags       : 1
Fixed Anchors     : 4
Processing Unit   : Raspberry Pi 4
UWB Technology    : Qorvo UWB
Ranging Protocol  : FiRa DS-TWR
Localization      : Least-Squares Multilateration
Programming       : Python
Visualization     : Matplotlib

The anchors are positioned at predetermined coordinates within the localization area.

Project Development Procedure

The project was developed in the following sequence:

1. UWB hardware setup
          |
          v
2. Raspberry Pi integration
          |
          v
3. FiRa DS-TWR ranging
          |
          v
4. Three-anchor testing
          |
          v
5. Trilateration
          |
          v
6. Four-anchor expansion
          |
          v
7. Least-Squares Multilateration
          |
          v
8. Real-time visualization
          |
          v
9. Vehicle / robotics integration
Results

The system successfully demonstrated:

Communication between the Raspberry Pi and Qorvo UWB hardware.
Real-time UWB ranging.
Continuous distance acquisition.
Three-anchor localization during the initial implementation.
Four-anchor localization architecture.
Real-time coordinate estimation.
Real-time visualization of the estimated tag position.
Monitoring of anchor ranging status.

The four-anchor configuration was developed as the final implementation to provide improved localization stability and robustness.

A comprehensive quantitative localization-accuracy evaluation using known ground-truth coordinates was not performed during the project and remains an area for future work.

Vehicle / Robotics Integration

The localization system was developed as a component of a broader V2X and robotics test platform.

The estimated UWB position can be used as an input for applications such as:

Vehicle localization
Robot localization
Indoor navigation
Autonomous systems
V2X research
Indoor asset tracking

The modular architecture allows the localization output to be integrated with other sensing and processing systems.

Project Structure
Real-Time-Vehicle-Localization-System/
│
├── README.md
├── requirements.txt
├── .gitignore
│
└── src/
    └── uwb_localization/
        │
        ├── config.py
        ├── parser.py
        ├── trilateration.py
        ├── plotter.py
        └── uwb_localization.py
Requirements

The Python software requires:

Python 3
NumPy
Matplotlib

Install the required Python packages using:

pip install -r requirements.txt
How to Run
1. Clone the repository
git clone https://github.com/abhijyothi111-bit/Real-Time-Vehicle-Localization-System.git
2. Enter the project directory
cd Real-Time-Vehicle-Localization-System
3. Install Python dependencies
pip install -r requirements.txt
4. Enter the localization source directory
cd src/uwb_localization
5. Start the localization application
python3 uwb_localization.py

Note: The current parser.py contains Raspberry Pi-specific paths and Qorvo UWB tool locations. These paths must be configured according to the target Raspberry Pi environment before execution.

Current Scope and Limitations

The current implementation focuses on:

2D indoor localization
One mobile tag
Four fixed anchors
FiRa DS-TWR ranging
Real-time position estimation
Python-based visualization

Current limitations include:

Quantitative ground-truth accuracy evaluation has not yet been completed.
The current system is designed for a single mobile tag.
The localization is currently two-dimensional.
Performance can be affected by multipath, obstruction, and ranging errors.
The software currently contains Raspberry Pi-specific paths that require configuration on another system.
The current repository contains the core localization software; hardware-specific firmware and supporting project documentation may be maintained separately.
Future Improvements

Possible future developments include:

Quantitative localization accuracy testing.
Ground-truth based error analysis.
Multi-tag localization.
3D localization.
Sensor fusion with LiDAR, IMU, or other sensors.
UWB-based custom data transmission.
Improved filtering techniques.
Improved outlier rejection.
Dynamic anchor configuration.
Network-based position sharing.
Integration with autonomous vehicles and robots.
Integration with a complete V2X communication system.
Applications

The developed platform can be extended for:

Indoor vehicle localization
Autonomous robot navigation
Warehouse automation
Asset tracking
Industrial IoT
Smart manufacturing
Indoor positioning systems
Robotics research
V2X research and development
Technologies Used
Hardware
Raspberry Pi 4 Model B
Qorvo UWB Development Boards
UWB Mobile Tag
UWB Fixed Anchors
Communication
Ultra-Wideband (UWB)
FiRa
Double-Sided Two-Way Ranging (DS-TWR)
USB
Software
Python
NumPy
Matplotlib
Qorvo UWB Tools
Algorithms
Trilateration
Least-Squares Multilateration
Exponential Moving Average Filtering
Time-of-Flight Calculation
Project Contribution

The project demonstrates the complete development of an embedded indoor localization platform, starting from UWB ranging and progressing to real-time position estimation and visualization.

The main contribution is the integration of Qorvo UWB hardware, Raspberry Pi processing, FiRa DS-TWR ranging, multilateration, filtering, status monitoring, and real-time visualization into a modular localization system.

Author

Abhi Jyothi

Electronics and Communication Engineering