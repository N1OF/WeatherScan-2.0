import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Degrees to Cardinal Direction Conversion
def degrees_to_cardinal(degrees):
    """
    Convert degrees to a cardinal direction.
    """
    if 337.5 <= degrees < 360 or 0 <= degrees < 22.5:
        return "North"
    elif 22.5 <= degrees < 67.5:
        return "Northeast"
    elif 67.5 <= degrees < 112.5:
        return "East"
    elif 112.5 <= degrees < 157.5:
        return "Southeast"
    elif 157.5 <= degrees < 202.5:
        return "South"
    elif 202.5 <= degrees < 247.5:
        return "Southwest"
    elif 247.5 <= degrees < 292.5:
        return "West"
    elif 292.5 <= degrees < 337.5:
        return "Northwest"
    else:
        return "Unknown"

# OpenWeatherMap API key and endpoint
api_key = "652b155023e67075d1b6cc4a4d722969"
api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
forecast_endpoint = "http://api.openweathermap.org/data/2.5/forecast/"
nws_alerts_endpoint = f"https://api.weather.gov/alerts/active/zone/OHZ017"

# Parameters for your location (replace with your coordinates)
params = {
    'lat': 41.0391,
    'lon': -83.6502,
    'appid': api_key,
    'units': 'imperial'  # Use 'imperial' for Fahrenheit
}

# Make API request for Current Conditions
response = requests.get(api_endpoint, params=params)
data = response.json()

# API request for Forecast
results = requests.get(forecast_endpoint, params=params)
dataForecast = results.json()

# API request for Active Alerts
response_alerts = requests.get(nws_alerts_endpoint)
alerts_data = response_alerts.json()

# Extract relevant weather information
temperature = data['main']['temp']
description = data['weather'][0]['description']
icon_code = data['weather'][0]['icon']
wind_speed = data['wind']['speed']
wind_deg = data['wind']['deg']
precipPercent = dataForecast['list'][0]['pop']
feelslike = data['main']['feels_like']

# Extract alert data from NWS API
alerts = alerts_data.get('features', [])
alert_titles = [alert.get('properties', {}).get('event', 'Unknown Event') for alert in alerts]

# Print Alert titles if present, if not, print "There are no active alerts" string
if not alert_titles:
    alert_text = ("There are no active alerts")
else:
    for title in alert_titles:
        alert_text = (title)

# Round to nearest whole number
roundedTemp = round(temperature)
roundedWind = round(wind_speed)
roundedFeelsLike = round(feelslike)

# Convert precipPercent to Percentage
convertedRain = precipPercent * 100
intRain = int(convertedRain)

# Convert Wind Degrees to Cardinal Directions
cardinal_direction = degrees_to_cardinal(wind_deg)

# Set the background color for the icon
background_color = (25, 21, 255)  # Specify the RGB values for the background color (white in this example)

# Open a template image
img = Image.open("template_image.jpg")
draw = ImageDraw.Draw(img)

# Choose a different font and font size, used for main body
font_path1 = "/home/n0vrs/TWCFonts/Star3000.ttf"  # Replace with the path to your font file
font_size1 = 25
font1 = ImageFont.truetype(font_path1, font_size1)

# Choose a different font and font size, used for heading
font_path2 = "/home/n0vrs/TWCFonts/Star3000Small.ttf"  # Replace with the path to your font file
font_size2 = 25
font2 = ImageFont.truetype(font_path2, font_size2)

# Font used for alert text at bottom of window
font_path3 = "/home/n0vrs/TWCFonts/Star3000Extended.ttf"
font_size3 = 20
font3 = ImageFont.truetype(font_path3, font_size3)

# Set the maximum width for text wrapping
max_width = 450

# Wrap the text using the textwrap module
wrapped_text = textwrap.fill(f"Right now . . . in Findlay, the temperature is {roundedTemp}\u00b0F, under {description}. Winds {cardinal_direction} at {roundedWind} miles per hour. It currently feels like {roundedFeelsLike}\u00b0F. Chance of precipitation {intRain} percent.", width=30)

# Text Wrap for Station Info
wrapped_info = textwrap.fill(f"SSTV Radar Image sent at top of hour, Forecast sent at half hour. 8A-10P Daily, 432.350 MHz PD120.", width=35)

# Text Wrap for Alerts
wrapped_alerts = textwrap.fill(f"{alert_text} for Hancock County.", width=40)

# Add wrapped text to the image with the chosen font (Body Text)
#draw.text((60, 125), wrapped_text, fill="white", font=font1)

# Body Text with drop shadow
shadow_offset = 2  # Adjust as needed
draw.text((60 + shadow_offset, 125 + shadow_offset), wrapped_text, fill="black", font=font1)
draw.text((60, 125), wrapped_text, fill="white", font=font1)

# Wrapped Text for Station Info
#draw.text((60, 300), wrapped_info, fill="white", font=font1)

# Station Info text with drop shadow
draw.text((60 + shadow_offset, 330 + shadow_offset), wrapped_info, fill="black", font=font1)
draw.text((60, 330), wrapped_info, fill="white", font=font1)

# Add Title/Header
#draw.text((155,45), "Weatherscan 2.0", fill="yellow", font=font2)
#draw.text((155,75), "for Findlay, Ohio", fill="yellow", font=font2)

# Title/Header Drop Shadow
draw.text((155 + shadow_offset, 45 + shadow_offset), "Weatherscan 2.0", fill="black", font=font2)
draw.text((155, 45), "Weatherscan 2.0", fill="yellow", font=font2)
draw.text((155 + shadow_offset, 75 + shadow_offset), "for Findlay, Ohio", fill="black", font=font2)
draw.text((155, 75), "for Findlay, Ohio", fill="yellow", font=font2)

# Text for Alerts
draw.text((50 + shadow_offset, 430 + shadow_offset), wrapped_alerts, fill="black", font=font3)
draw.text((50, 430), wrapped_alerts, fill="white", font=font3)

# Insert the weather icon into the image and resize it
icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
icon_image = Image.open(requests.get(icon_url, stream=True).raw)

# Create a copy of the icon with an alpha channel
icon_image = icon_image.convert("RGBA")

# Create a new image with the specified background color
icon_background = Image.new('RGBA', icon_image.size, background_color)

# Paste the icon onto the new image with the specified background color
icon_with_background = Image.alpha_composite(icon_background, icon_image)

# Resize the icon to the desired dimensions (e.g., 50x50)
icon_size = (60, 60)
icon_with_background_resized = icon_with_background.resize(icon_size)

# Paste the resized icon onto the template image
img.paste(icon_with_background_resized, (55, 35), icon_with_background_resized)  # Adjust the coordinates based on your template


# Save the modified image
img.save("output_image.jpg")

