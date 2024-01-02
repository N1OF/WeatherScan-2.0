# WeatherScan 2.0 - Used to schedule Cron job with rights to open terminal on user's desktop session
# GNU General Public License, version 3.0 (GPL-3.0)
# See the full license text at: https://www.gnu.org/licenses/gpl-3.0.html

#!/bin/bash

# Change these variables according to your setup
TERMINAL_COMMAND="gnome-terminal"  # Change to your terminal emulator (e.g., xterm, konsole)
PROGRAM_COMMAND="/path/to/file/forecastplay.sh"
DELAY_SECONDS=5  # Adjust as needed

# Open terminal
$TERMINAL_COMMAND &

# Wait for the terminal to be fully open
sleep $DELAY_SECONDS

# Run the program in the terminal
xdotool type "$PROGRAM_COMMAND"
xdotool key Return

#Sleep for 3 minutes. Adjust as needed to give enough time for your audio files to generate and play
sleep 180

# Close the terminal (change "Ctrl+D" if your terminal requires a different command)
xdotool key Ctrl+D

