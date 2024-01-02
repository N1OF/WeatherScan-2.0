# WeatherScan-2.0
WeatherScan 2.0 - README

These scripts are used to send a PD120 SSTV image via a Amateur Radio Transceiver that is either a forecast for the area, or a radar image pulled from NWS.

RADAR

This script is used to download a static radar image from a NWS office, convert it to a soundfile, PTT a transceiver, and play the audio via a soundcard.

Prerequisites

-ImageMagick
-Python
-PySSTV
-Hamlib

Installation

Download the repository, and edit the following variables
-In radarlaunch.sh, change your TERMINAL_COMMAND to match the terminal your Linux Distribution uses. This will allow Cron to launch the script properly.

-In radar.sh, change the wget command to link to a NWS office that covers your location.

-This script is designed for use with the PD120 SSTV Mode. This mode requires an image resolution of 640x496. If you wish to use a different mode, change the pysstv mode to what you want to use, and change the convert command to the proper resolution. Please refer to the PySSTV documentation for available modes and required resolutions.

-In all three files, edit the file paths to match your setup.

-Run chmod +x on all .sh files to mark as executable

-To run once, type "./radar.sh" in the project directory

FORECAST

This script is used to overlay text onto a template image, using data pulled from OpenWeatherMap and NWS API's. This then converts the image to a PD120 audio file, PTT's a transceiver, and plays the audio via a soundcard.

Prerequisites

-OpenWeatherMap API Key (Can use a free one, or can use a different provider)
-PySSTV
-Hamlib
-Python

Installation

Download the repository, and edit the following variables
-In forecastlaunch.sh, change your TERMINAL_COMMAND to match the terminal your Linux Distribution uses. This will allow Cron to launch the script properly.

-In openweathermap.py, you have to replace several variables for your setup. They include:
	
   -api_key: Your OpenWeatherMap API key
	
   -nws_alerts_endpoint: Your county code for NWS alerts
	
   -'units': Imperial or Metric units
	
   -location: The name of your town/city
	
   -county: The county you reside in
	
   -background_color: This changes the background color of the icon image. Change this to work with your template.
	
   -Image.open: The path to your template image
	
   -font_path, font_size, and font(1/2/3): Paths to your font file of choice, as well as sizes
	
   -max_width: The max width for text wrapping, in pixels. Play around with this to fit your template image
	
   -wrapped_text: You may change the text in here to fit your needs, and rearrange the variables if you wish. Check your width at the end of this     line to match your template
	
   -wrapped_info: Edit this line for your station info
	
   -draw.text: Used to print the text with a drop shadow. You may change the font colors as needed for your template. You may also need to change the (X,Y) coordinates here for your text to work properly with your image.

   -iconSize and img.paste: These set your weather icon image size and location. Adjust as necessary.

-This script is designed for use with the PD120 SSTV Mode. This mode requires an image resolution of 640x496. If you wish to use a different mode, change the pysstv mode to what you want to use. Please refer to the PySSTV documentation for available modes and required resolutions.

-In all four files, edit the file paths to match your setup.

-Run chmod +x on all .sh/.py files to mark as executable

-To run once, type "./forecast.sh" in the project directory

AUTOMATION

This software is designed to be launched via a Cron job every hour. In the author's case, the radar image is sent on the hour every hour, and the forecast image is sent on the half hour. Example cron jobs are posted below, with a secondary command to print any errors to a log file in the project directory.

0 * * * * export DISPLAY=:0 && /path/to/file/forecastlaunch.sh >> /path/to/file/forecasterrors.log 2>&1
30 * * * * export DISPLAY=:0 && /path/to/file/radarlaunch.sh" >> /path/to/file/radarerrors.log 2>&1

EXAMPLE RECEIVED IMAGES

![Weatherscan2 0-Decode](https://github.com/N1OF/WeatherScan-2.0/assets/125296450/a25ac6b4-9e60-412a-a502-5e38f020942b)
![RadarImage-Decode](https://github.com/N1OF/WeatherScan-2.0/assets/125296450/d335ac77-920c-42f4-bb1d-048a7d5b8e5e)
