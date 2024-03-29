# Weatherscan 2.0 - Used for Playing WAV files generated by PySSTV, as well as CW ID.
# GNU General Public License, version 3.0 (GPL-3.0)
# See the full license text at: https://www.gnu.org/licenses/gpl-3.0.html

#!/bin/bash

#Allows Cron to run in terminal
export XDG_RUNTIME_DIR="/run/user/$(id -u)"

echo on

#Adjust sleep times as necessary, may need adjusted to allow terminal window(s) to open on time
sleep 1
play /path/to/file/radar.wav
sleep 1
play /path/to/file/id.wav
