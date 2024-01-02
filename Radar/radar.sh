# WeatherScan 2.0 - Used for downloading radar image, coverting to correct image size, encoding as audio, and sending.
# GNU General Public License, version 3.0 (GPL-3.0)
# See the full license text at: https://www.gnu.org/licenses/gpl-3.0.html

#!/bin/bash

#Curl from NWS - Change KIWX to match your local office
wget -O radar.gif https://radar.weather.gov/ridge/standard/KIWX_0.gif

#Convert image to the right size (640x496 for PD120 Mode)
convert radar.gif -resize 640x496! converted.gif

#Convert image to WAV file using Pysstv
python3 -m pysstv --mode PD120 converted.gif radar.wav

#Open new terminal, play sound files. Sound files play in secondary terminal (adjust sleep in sstvplay.sh as needed)
gnome-terminal -- /path/to/file/radaraudio.sh

# Open PTT (hamlib command, replace with path to your serial PTT device. Change pause as needed to allow time for audio to play)
rigctl -p /dev/ttyUSB0 -P RTS T 1 pause 148

#Close the terminal window
exit 0

# End of the script
