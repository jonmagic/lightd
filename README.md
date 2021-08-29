# lightd

My home lighting daemon for the Raspberry Pi.

## Setup

I'm using a Raspberry Pi 3 with an 8GB micro SD card and I used the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) to install the Raspberry Pi OS without a Desktop GUI as I plan on using this as a headless server.

I created an empty file called `ssh` in the root of the SD card so that it would boot with ssh enabled. Once the device was powered up I ssh'd into it using the default username of `pi` and password `raspberry`.

Next I ran `raspi-config` to update the password to something more secure and configured the WiFi to connet to my home network.

Finally I ran `sudo apt update` and `sudo apt upgrade` to get the latest software.

## Configure

I decided to use git to clone the lightd repo instead of simply downloading a copy of it so I can easily get updates. To do that I needed to install git first.

```
sudo apt install git
```

The service also requires the rpi-rf library which requires python3 so I installed it.

```
sudo apt install python3-pip
sudo pip3 install rpi-rf
```

Then I switched into the `/usr/local` directory to clone the lightd repo.

```
cd /usr/local
sudo git clone https://github.com/jonmagic/lightd
```

Next I wanted the service to start on startup and tried [all five options in this post](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/) and only systemd ended up working.

I created the file.

```
sudo nano /lib/systemd/system/lightd.service
```

And pasted in these file contents.

```
[Unit]
Description=lightd
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /usr/local/lightd/server.py > /usr/local/lightd/server.log 2>&1

[Install]
WantedBy=multi-user.target
```

And finally finished configuring the service by updating permissions, reloading the daemon, enabling it, and then rebooting.

```
sudo chmod 644 /lib/systemd/system/lightd.service
sudo systemctl daemon-reload
sudo systemctl enable lightd.service
sudo reboot
```

## Lighting systems

### Pergola Lighting Controller

- uses 433Mhz RF
- https://www.instructables.com/RF-433-MHZ-Raspberry-Pi/ or [pdf copy](rf-433mhz-how-to.pdf)

| data    | info                |
|---------|---------------------|
| 402     | pulselength         |
| 1       | protocol            |
| 2677763 | toggle power        |
| 2677762 | delay off           |
| 2677764 | increase brightness |
| 2677770 | decrease brightness |
| 2677773 | minimum brightness  |
| 2677765 | 100% brightness     |
| 2677766 | 75% brightness      |
| 2677768 | 50% brightness      |
| 2677769 | 25% brightness      |
| 2677771 | diy 1               |
| 2677772 | diy 2               |
| 2677774 | diy 3               |
| 2677775 | diy 4               |

```
curl http://lightd.local:8081/pergola/toggle_power
```
