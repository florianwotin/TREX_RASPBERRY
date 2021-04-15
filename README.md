# TREX_RASPBERRY
---

## Brief
This Program takes photos periodically to train neural network application as well as forwarding the phone app motor commands to the TREX_CONTROLLER program

## Installation

clone this repository on your raspberry workspace :
```bash
 git clone https://github.com/florianwotin/TREX_RASPBERRY.git
```

Create a serialBluetooth.service in etc/systemd/system and copy the following code into it:
```[Service]
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/libexec/iptables.init start
ExecStop=/usr/libexec/iptables.init stop

```

Create a Trex.service in etc/systemd/system and copy the following code into it:
```bash

```

Then update the services with the command:

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

| File UUID | label |
| --------- |:-----:|
| fileName  |   0   |
| fileName  |  -5   |
| fileName  |  -4   | 

This CSV can then be used to train the neural network.
