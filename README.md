<b>Vera HMI</b>

This is a program that is meant for use in Vera, a car developed by Chalmers Vera Team at Chalmers University of technology in Gothenburg, Sweden (www.chalmersverateam.se). The team participates in primarily two European competitions, Shell Eco Marathon in Rotterdam and Pisaralla Pisimälle in Nokia Finland. These competitions challenges student teams from around the world to design, build and test ultra energy-efficient vehicles. With annual events first in the Americas, then Europe and Asia, the winners are the teams that go the furthest using the least amount of energy. The events spark debate about the future of mobility and inspire young engineers to push the boundaries of fuel efficiency.

The source code in this repository is what we call the HMI part of the system (Human Machine Interface) and is intended for communicating with the ECU also developed by our team via a serial communication link. 

The purpose of this program is to primarily receive data from the cars ECU and save it in a local database. The secondary purpose is to present this data to the driver during the race. The data is then easily accessible through WiFi. All you need is a device with a WiFi connection to the HMI and a web browser. 

The next step is to attach a 3G/4G module and provide live data to the rest of the team through our website (www.chalmersverateam.se).


To run the program simple execute main.py (with sudo permission) on a Raspberry Pi (preferably a model 2 or later).
