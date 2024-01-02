# WeatherScan 2.0 - Used for creating forecast image, encoding as audio, and sending.
# GNU General Public License, version 3.0 (GPL-3.0)
# See the full license text at: https://www.gnu.org/licenses/gpl-3.0.html

#!/bin/bash

#Create SSTV Image with OpenWeatherMap API and Template
python3 /path/to/file/weatherscan.py #Adjust path as necessary

#Convert image to WAV file using Pysstv
python3 -m pysstv --mode PD120 /path/to/file/output_image.jpg /path/to/file/forecast.wav

#Open new window, prepare sound files. Sound files play in secondary terminal
gnome-terminal -- /path/to/file/forecastaudio.sh

# Step 4: Open PTT (hamlib command, replace with path to your serial PTT device)
rigctl -p /dev/ttyUSB0 -P RTS T 1 pause 140

#Close the terminal window
exit 0

# End of the script
