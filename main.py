import os
import requests
import json
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class AlertLevel(Enum):
    """Alert levels for weather conditions"""
    SAFE = "🟢"  # All clear
    WARNING = "🟡"  # Closeish vicinity
    DANGER = "🔴"  # SEEK SHELTER IMMEDIATELY


class SparkyWeatherAssistant:
    """Sparky the Weatherbug - AI Weather Assistant with dynamic shell color alerts"""

    def __init__(self, api_key: str = None):
        """
        Initialize Sparky the Weatherbug

        Args:
            api_key: OpenWeatherMap API key (defaults to WEATHER_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

        if not self.api_key:
            raise ValueError(
                "Weather API key not found. Please set WEATHER_API_KEY environment variable."
            )

        self.personality = [
            "Stay safe out there, buddy! 🐛",
            "Sparky here with your weather update! ☀️",
            "Let's check what Mother Nature is cooking up! 🌦️",
            "Your friendly weatherbug reporting for duty! 🐞",
        ]

    def get_weather(self, city: str, country_code: str = None) -> dict:
        """
        Fetch current weather data for a location

        Args:
            city: City name
            country_code: Optional country code (e.g., 'US', 'UK')

        Returns:
            Weather data dictionary
        """
        location = f"{city},{country_code}" if country_code else city

        try:
            response = requests.get(
                self.base_url,
                params={"q": location, "appid": self.api_key, "units": "metric"},
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch weather data: {str(e)}"}

    def assess_danger_level(self, weather_data: dict) -> AlertLevel:
        """
        Assess weather danger level and return appropriate shell color

        Args:
            weather_data: Weather data from API

        Returns:
            AlertLevel enum with shell color
        """
        if "error" in weather_data:
            return AlertLevel.SAFE

        main = weather_data.get("main", {})
        weather = weather_data.get("weather", [{}])[0]
        wind = weather_data.get("wind", {})

        temp = main.get("temp", 0)
        feels_like = main.get("feels_like", 0)
        humidity = main.get("humidity", 0)
        wind_speed = wind.get("speed", 0)
        description = weather.get("main", "").lower()
        event_id = weather.get("id", 0)

        # RED ALERT - SEEK SHELTER IMMEDIATELY
        if (
            "tornado" in description
            or "hurricane" in description
            or "thunderstorm" in description
            and wind_speed > 50
            or temp < -40
            or temp > 55
            or (wind_speed > 80)
            or event_id < 230  # Thunderstorm with rain/snow
        ):
            return AlertLevel.DANGER

        # YELLOW ALERT - Warning vicinity
        if (
            "thunderstorm" in description
            or "heavy rain" in description
            or "heavy snow" in description
            or wind_speed > 40
            or temp < -20
            or temp > 45
            or (humidity > 90 and temp > 30)
            or event_id in range(500, 532)  # Rain conditions
        ):
            return AlertLevel.WARNING

        # GREEN - All clear
        return AlertLevel.SAFE

    def generate_sparky_message(self, weather_data: dict, alert_level: AlertLevel) -> str:
        """
        Generate a friendly message from Sparky with personality

        Args:
            weather_data: Weather data from API
            alert_level: Current alert level

        Returns:
            Formatted message with shell color and weather info
        """
        import random

        if "error" in weather_data:
            return f"{AlertLevel.SAFE.value} Sparky here! I'm having trouble accessing weather data. Please check your API key and internet connection!"

        city = weather_data.get("name", "Unknown")
        country = weather_data.get("sys", {}).get("country", "")
        location = f"{city}, {country}" if country else city

        main = weather_data.get("main", {})
        weather = weather_data.get("weather", [{}])[0]
        wind = weather_data.get("wind", {})

        temp = main.get("temp", 0)
        feels_like = main.get("feels_like", 0)
        humidity = main.get("humidity", 0)
        pressure = main.get("pressure", 0)
        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", 0)
        description = weather.get("description", "").title()
        icon = weather.get("icon", "01d")

        greeting = random.choice(self.personality)

        # Alert message based on danger level
        alert_messages = {
            AlertLevel.SAFE: "All clear! Everything looks perfect! 🌞",
            AlertLevel.WARNING: "⚠️ WARNING! Severe weather in the vicinity! Stay alert!",
            AlertLevel.DANGER: "🚨 RED ALERT! SEEK SHELTER IMMEDIATELY! Dangerous conditions ahead!",
        }

        alert_msg = alert_messages[alert_level]

        message = f"""
{alert_level.value} SPARKY THE WEATHERBUG REPORT {alert_level.value}
{'=' * 50}

{greeting}

📍 Location: {location}
🌡️  Temperature: {temp}°C (Feels like {feels_like}°C)
💧 Humidity: {humidity}%
💨 Wind Speed: {wind_speed} m/s
🧭 Wind Direction: {wind_deg}°
🌍 Pressure: {pressure} hPa

🌤️  Conditions: {description}

{alert_msg}

Stay safe and keep an eye on the skies! 🐛✨
"""
        return message

    def get_forecast(self, city: str, country_code: str = None) -> dict:
        """
        Fetch 5-day forecast for a location

        Args:
            city: City name
            country_code: Optional country code

        Returns:
            Forecast data dictionary
        """
        location = f"{city},{country_code}" if country_code else city

        try:
            response = requests.get(
                self.forecast_url,
                params={"q": location, "appid": self.api_key, "units": "metric"},
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch forecast data: {str(e)}"}

    def display_weather(self, city: str, country_code: str = None) -> None:
        """
        Display current weather with Sparky's shell color alert

        Args:
            city: City name
            country_code: Optional country code
        """
        weather_data = self.get_weather(city, country_code)
        alert_level = self.assess_danger_level(weather_data)
        message = self.generate_sparky_message(weather_data, alert_level)
        print(message)

    def display_forecast(self, city: str, country_code: str = None) -> None:
        """
        Display 5-day forecast

        Args:
            city: City name
            country_code: Optional country code
        """
        forecast_data = self.get_forecast(city, country_code)

        if "error" in forecast_data:
            print(f"🔴 Error: {forecast_data['error']}")
            return

        print(f"\n📅 5-DAY FORECAST FOR {forecast_data.get('city', {}).get('name')}")
        print("=" * 60)

        for item in forecast_data.get("list", [])[:8]:  # Show first 8 (2 days)
            dt = datetime.fromtimestamp(item["dt"])
            temp = item["main"]["temp"]
            description = item["weather"][0]["description"].title()
            alert = self.assess_danger_level(item)

            print(f"\n{alert.value} {dt.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Temperature: {temp}°C")
            print(f"   Conditions: {description}")


def main():
    """Main function to demonstrate Sparky the Weatherbug"""
    try:
        sparky = SparkyWeatherAssistant()

        # Example usage
        print("\n" + "=" * 60)
        print("🐞 WELCOME TO SPARKY THE WEATHERBUG 🐞")
        print("=" * 60)

        # Get weather for a city
        city = input("\nEnter a city name (default: London): ").strip() or "London"
        sparky.display_weather(city)

        # Show forecast
        show_forecast = input("\nWould you like to see the forecast? (y/n): ").lower()
        if show_forecast == "y":
            sparky.display_forecast(city)

    except KeyboardInterrupt:
        print("\n\nSparky says: Stay safe! Goodbye! 🐛")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
