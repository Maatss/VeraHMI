<b>Vera HMI</b>

This is a program that is meant for use in Vera, a car developed by Chalmers Vera Team at Chalmers University of technology in Gothenburg, Sweden (www.chalmersverateam.se). The team participates in primarily two European competitions, Shell Eco Marathon in Rotterdam and Pisaralla Pisimälle in Nokia Finland. These competitions challenges student teams from around the world to design, build and test ultra energy-efficient vehicles. With annual events first in the Americas, then Europe and Asia, the winners are the teams that go the furthest using the least amount of energy. The events spark debate about the future of mobility and inspire young engineers to push the boundaries of fuel efficiency.

The source code in this repository is what is call the HMI part of the system (Human Machine Interface) and is intended for communicating with the ECU also developed by our team via a universal serial bus.  

The purpose of this program is to primarily receive data from the ECU in the car and save it in a local database. The secondary purpose is to present this data to the driver during the race. The data is then easily accessible through WiFi. All you need is a device with a WiFi connection to the HMI and a web browser. Another ongoing development is live streaming of the collected data to a remote server in order to enable the rest of the team to see the state of the vehicle such as temperatures, error code from the ECU etc. This is done using a Huawei ZTE MF823 4g modem and it uses plotly python API for Raspberry Pi (see their website: plot.ly, or the git repo for their project: https://github.com/plotly/raspberrypi).

Installation instructions:

1. Install Raspbian Jessie (or later) on an SD card (you can download it from https://www.raspberrypi.org/downloads/raspbian). Plug the SD card into the Raspberry Pi and fire it up! (Note: Debian Jessie Lite also works for a more lightweight OS). For the following steps it is assumed you have accesss to the terminal on the Raspberry Pi (either via SSH or directly with a monitor and keyboard connected to the computer). It is also assumed thet the RPi can access the internet.
2. run "sudo raspi-config" in the command promt. Go to 'Internationalisation Options' > 'change timezone'. Change the time zone to the desired one. 
3. Also in the raspi-config menu go to 'Advanced option' > 'Serial' and disable shell and kernel messages on the serial connection. This is done in order to make the "AMA0" serial interface available for the GPS module.
4. Also in the raspi-config menu, press 'expand filesystem' to resize the partition to fill the whole SD card. After this press 'finish' and answer yes to the popup question. The computer will reboot. 
5. Clone git repo to the home directory (/home/pi), the address to the repo is: https://github.com/andreaskall/VeraHMI.git .
6. Make /VeraHMI/Init/VeraHMI_init executable (sudo chmod +x .../VeraHMI_init)
7. run the script (sudo .../VeraHMI_init)
    This script will install all dependecies and make the proper settings automatically.
8. The Raspberry Pi will reboot when installation is done. The application will run at boot.
9. DONE :) 
