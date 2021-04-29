# TREX_RASPBERRY
---

## Brief
This Program takes photos periodically to train neural network application as well as forwarding the phone app motor commands to the TREX_CONTROLLER program

## Installation

clone this repository on your raspberry workspace :
```bash
 git clone https://github.com/florianwotin/TREX_RASPBERRY.git
```

Create a rfcomm.service in /etc/systemd/system and copy the following code into it:
```[Service]
Description=RFCOMM service
After=bluetooth.service
Requires=bluetooth.service

[Service]
ExecStart=/usr/bin/rfcomm watch hci0

[Install]
WantedBy=multi-user.target
```

Create a trex.service in /etc/systemd/system and copy the following code into it:
```[Service]
[Unit]
Description=The TREX Photo Service
After=multi-user.target

[Service]
Environment=DISPLAY=0.0
Environment=XAUTHORITY=/home/pi/.Xauthority
Type=idle
ExecStart=/usr/bin/python3 /home/pi/Projects/TakePhoto.py > home/pi/Projects/output.txt
Restart=always
RestartSec=1

[Install]
WantedBy=multi.user.target
```

Then update the services with the commands:
```bash
sudo systemctl enable rfcomm.service
sudo systemctl enable trex.service
```

Then reboot the raspberry

## How does the program works
The program will take a photo with the webcam every second after receiving the recording activation message (0xE 0x0 0x1) from the phone app via bluetooth.

Each photo will have a UUID and a corresponding "direction" label between [-8, 8].
This label is calculated with the folowing formula:

```python
label = int((left_motor - right_motor)/10) 

label = min(label, 8) if (label > 0) else max(label, -8))
```


When the stop recording message (0xE 0x0 0x0) is received, the program will save a csv with the folowing format:

| File Name | label |
| --------- |:-----:|
| UUID      |   0   |
| UUID      |  -5   |
| UUID      |  -4   |

This CSV can then be used to train the neural network.
