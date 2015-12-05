<b>Vera HMI</b>

This is a program that is meant for use in Vera, a car developed by Chalmers Vera Team at Chalmers University of technology in Gothenburg, Sweden (www.chalmersverateam.se). The team participates in primarily two European competitions, Shell Eco Marathon in Rotterdam and Pisaralla Pisimälle in Nokia Finland. These competitions challenges student teams from around the world to design, build and test ultra energy-efficient vehicles. With annual events first in the Americas, then Europe and Asia, the winners are the teams that go the furthest using the least amount of energy. The events spark debate about the future of mobility and inspire young engineers to push the boundaries of fuel efficiency.

The source code in this repository is what we call the HMI part of the system (Human Machine Interface) and is intended for communicating with the ECU also developed by our team via a serial communication link. 

The purpose of this program is to primarily receive data from the ECU in the car and save it in a local database. The secondary purpose is to present this data to the driver during the race. The data is then easily accessible through WiFi. All you need is a device with a WiFi connection to the HMI and a web browser. Another ongoing development is live streaming of the collected and saved data to a server to enable the rest of the team to see the state of the vehicle such as temperatures etc. This is done using a Huawei ZTE MF823 4g modem and plotly python API for Raspberry pi (plot.ly, https://github.com/plotly/raspberrypi).

Installation instructions:

1. Install Raspbian Jessie (or later) on an SD card. 
2. Clone git repo (https://github.com/andreaskall/VeraHMI.git)
3. Make /VeraHMI/Init/VeraHMI_init executable (sudo chmod +x .../VeraHMI_init)
4. run the script (sudo .../VeraHMI_init)
    This script will install all dependecies and make the proper settings automatically.
5. The Raspberry Pi will reboot when installation is done. The application will run at boot.
6. DONE :) 
7. 
