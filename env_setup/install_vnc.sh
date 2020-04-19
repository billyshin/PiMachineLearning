sudo apt-get remove xrdp vnc4server tightvncserver
sudo apt-get install -y tightvncserver
sudo apt-get install -y xrdp
sudo apt-get install --no-install-recommends xserver-xorg
sudo apt-get install --no-install-recommends xinit
sudo apt-get install raspberrypi-ui-mods
sudo apt-get install --no-install-recommends raspberrypi-ui-mods lxsession

sudo raspi-config