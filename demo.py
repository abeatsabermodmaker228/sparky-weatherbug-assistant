#!/usr/bin/env python3
"""
Interactive demo script for Sparky the Weatherbug
Showcases all features with example cities
"""

from main import SparkyWeatherAssistant
import time


def demo():
    """Run a interactive demo of Sparky"""
    try:
        sparky = SparkyWeatherAssistant()

        print("\n" + "=" * 70)
        print("🐞 SPARKY THE WEATHERBUG - INTERACTIVE DEMO 🐞")
        print("=" * 70)

        demo_cities = {
            "1": ("New York", "US"),
            "2": ("Tokyo", "JP"),
            "3": ("London", "GB"),
            "4": ("Sydney", "AU"),
            "5": ("Custom", None),
        }

        print("\nSelect a city to check weather:")
        for key, (city, _) in demo_cities.items():
            print(f"  {key}. {city}")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice in demo_cities:
            if choice == "5":
                city = input("Enter city name: ").strip()
                country = input("Enter country code (or press Enter): ").strip() or None
            else:
                city, country = demo_cities[choice]

            print("\n" + "=" * 70)
            print(f"🐛 Sparky is checking the weather in {city}...")
            print("=" * 70)

            time.sleep(0.5)  # Simulate processing
            sparky.display_weather_with_response(city, country)

            # Ask for forecast
            forecast_choice = input("\n📅 Would you like to see the forecast? (y/n): ").lower()
            if forecast_choice == "y":
                print("\n" + "=" * 70)
                sparky.display_forecast(city, country)

            print("\n" + "=" * 70)
            print("🐞 Sparky says: Thanks for checking the weather! Stay safe! 🐞")
            print("=" * 70 + "\n")

        else:
            print("Invalid choice!")

    except KeyboardInterrupt:
        print("\n\n🐛 Demo interrupted. Goodbye!")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    demo()
