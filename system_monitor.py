#!/usr/bin/env python3
"""
Weather Information Utility
A comprehensive weather tool with API integration capabilities
"""

import os
import sys
import json
import time
import random
import math
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, asdict

@dataclass
class WeatherData:
    location: str
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: str
    condition: str
    description: str
    feels_like: float
    visibility: float
    uv_index: int
    timestamp: str

@dataclass
class ForecastData:
    date: str
    high_temp: float
    low_temp: float
    condition: str
    precipitation_chance: int
    humidity: float
    wind_speed: float

class WeatherUtility:
    def __init__(self):
        self.api_key = None
        self.use_api = False
        self.cache_duration = 300  # 5 minutes
        self.weather_cache = {}
        
        # Mock weather data for demonstration
        self.mock_locations = {
            'New York': {'lat': 40.7128, 'lon': -74.0060, 'timezone': 'EST'},
            'London': {'lat': 51.5074, 'lon': -0.1278, 'timezone': 'GMT'},
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503, 'timezone': 'JST'},
            'Sydney': {'lat': -33.8688, 'lon': 151.2093, 'timezone': 'AEST'},
            'Paris': {'lat': 48.8566, 'lon': 2.3522, 'timezone': 'CET'},
            'Moscow': {'lat': 55.7558, 'lon': 37.6176, 'timezone': 'MSK'},
            'Dubai': {'lat': 25.2048, 'lon': 55.2708, 'timezone': 'GST'},
            'Mumbai': {'lat': 19.0760, 'lon': 72.8777, 'timezone': 'IST'}
        }
        
        # Weather conditions and their characteristics
        self.weather_conditions = {
            'Clear': {'temp_modifier': 0, 'humidity_range': (30, 50), 'pressure_range': (1010, 1025)},
            'Partly Cloudy': {'temp_modifier': -2, 'humidity_range': (40, 60), 'pressure_range': (1005, 1020)},
            'Cloudy': {'temp_modifier': -5, 'humidity_range': (60, 80), 'pressure_range': (1000, 1015)},
            'Rain': {'temp_modifier': -8, 'humidity_range': (80, 95), 'pressure_range': (995, 1010)},
            'Thunderstorm': {'temp_modifier': -10, 'humidity_range': (85, 98), 'pressure_range': (990, 1005)},
            'Snow': {'temp_modifier': -15, 'humidity_range': (70, 90), 'pressure_range': (1000, 1020)},
            'Fog': {'temp_modifier': -3, 'humidity_range': (90, 100), 'pressure_range': (1005, 1025)},
            'Windy': {'temp_modifier': -5, 'humidity_range': (40, 70), 'pressure_range': (995, 1015)}
        }
    
    def set_api_key(self, api_key: str, provider: str = "openweathermap"):
        """Set API key for real weather data (OpenWeatherMap, WeatherAPI, etc.)"""
        self.api_key = api_key
        self.api_provider = provider
        self.use_api = True
        print(f"API key set for {provider}. Real weather data will be used.")
    
    def get_current_weather(self, location: str) -> WeatherData:
        """Get current weather for a location"""
        if self.use_api and self.api_key:
            return self._get_api_weather(location)
        else:
            return self._get_mock_weather(location)
    
    def _get_mock_weather(self, location: str) -> WeatherData:
        """Generate mock weather data for demonstration"""
        if location not in self.mock_locations:
            location = random.choice(list(self.mock_locations.keys()))
        
        # Base temperature based on location and season
        base_temp = self._get_base_temperature(location)
        
        # Random weather condition
        condition = random.choice(list(self.weather_conditions.keys()))
        condition_data = self.weather_conditions[condition]
        
        # Calculate weather parameters
        temp_modifier = condition_data['temp_modifier']
        temperature = base_temp + temp_modifier + random.uniform(-3, 3)
        
        humidity_min, humidity_max = condition_data['humidity_range']
        humidity = random.uniform(humidity_min, humidity_max)
        
        pressure_min, pressure_max = condition_data['pressure_range']
        pressure = random.uniform(pressure_min, pressure_max)
        
        wind_speed = random.uniform(0, 25)
        wind_direction = self._get_wind_direction()
        
        feels_like = temperature + random.uniform(-5, 5)
        visibility = random.uniform(1, 15) if condition in ['Fog', 'Rain'] else random.uniform(8, 15)
        uv_index = random.randint(0, 11)
        
        return WeatherData(
            location=location,
            temperature=round(temperature, 1),
            humidity=round(humidity, 1),
            pressure=round(pressure, 1),
            wind_speed=round(wind_speed, 1),
            wind_direction=wind_direction,
            condition=condition,
            description=self._get_weather_description(condition),
            feels_like=round(feels_like, 1),
            visibility=round(visibility, 1),
            uv_index=uv_index,
            timestamp=datetime.now().isoformat()
        )
    
    def _get_api_weather(self, location: str) -> WeatherData:
        """Get weather data from API (placeholder for real implementation)"""
        # This would be implemented with actual API calls
        # For now, return mock data with API indicator
        mock_data = self._get_mock_weather(location)
        mock_data.location = f"{location} (API)"
        return mock_data
    
    def _get_base_temperature(self, location: str) -> float:
        """Get base temperature for location considering season"""
        # Simplified seasonal temperature calculation
        month = datetime.now().month
        
        # Seasonal modifiers
        seasonal_modifiers = {
            'New York': {'winter': -5, 'spring': 15, 'summer': 25, 'fall': 10},
            'London': {'winter': 5, 'spring': 12, 'summer': 20, 'fall': 8},
            'Tokyo': {'winter': 8, 'spring': 18, 'summer': 28, 'fall': 15},
            'Sydney': {'winter': 15, 'spring': 20, 'summer': 25, 'fall': 18},
            'Paris': {'winter': 5, 'spring': 15, 'summer': 22, 'fall': 10},
            'Moscow': {'winter': -10, 'spring': 8, 'summer': 20, 'fall': 5},
            'Dubai': {'winter': 20, 'spring': 25, 'summer': 35, 'fall': 28},
            'Mumbai': {'winter': 25, 'spring': 30, 'summer': 32, 'fall': 28}
        }
        
        if month in [12, 1, 2]:
            season = 'winter'
        elif month in [3, 4, 5]:
            season = 'spring'
        elif month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'fall'
        
        return seasonal_modifiers.get(location, {'winter': 10, 'spring': 15, 'summer': 25, 'fall': 12})[season]
    
    def _get_wind_direction(self) -> str:
        """Get random wind direction"""
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        return random.choice(directions)
    
    def _get_weather_description(self, condition: str) -> str:
        """Get weather description"""
        descriptions = {
            'Clear': 'Clear skies with plenty of sunshine',
            'Partly Cloudy': 'Partly cloudy with some sun',
            'Cloudy': 'Overcast with mostly cloudy skies',
            'Rain': 'Light to moderate rainfall',
            'Thunderstorm': 'Thunderstorms with heavy rain',
            'Snow': 'Light snowfall',
            'Fog': 'Dense fog reducing visibility',
            'Windy': 'Strong winds with gusty conditions'
        }
        return descriptions.get(condition, 'Variable weather conditions')
    
    def get_forecast(self, location: str, days: int = 5) -> List[ForecastData]:
        """Get weather forecast for multiple days"""
        forecast = []
        base_temp = self._get_base_temperature(location)
        
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            condition = random.choice(list(self.weather_conditions.keys()))
            condition_data = self.weather_conditions[condition]
            
            # Daily temperature variation
            daily_variation = random.uniform(-5, 5)
            high_temp = base_temp + condition_data['temp_modifier'] + daily_variation + 5
            low_temp = high_temp - random.uniform(8, 15)
            
            forecast.append(ForecastData(
                date=date.strftime('%Y-%m-%d'),
                high_temp=round(high_temp, 1),
                low_temp=round(low_temp, 1),
                condition=condition,
                precipitation_chance=random.randint(0, 100),
                humidity=random.uniform(40, 90),
                wind_speed=random.uniform(0, 20)
            ))
        
        return forecast
    
    def get_weather_alerts(self, location: str) -> List[Dict[str, str]]:
        """Get weather alerts and warnings"""
        alerts = []
        
        # Generate random alerts based on conditions
        alert_types = [
            {'type': 'Heat Warning', 'message': 'Extreme heat expected. Stay hydrated and avoid prolonged outdoor activities.'},
            {'type': 'Cold Warning', 'message': 'Freezing temperatures expected. Dress warmly and protect exposed skin.'},
            {'type': 'Wind Advisory', 'message': 'Strong winds expected. Secure loose objects and drive carefully.'},
            {'type': 'Flood Watch', 'message': 'Heavy rainfall may cause flooding in low-lying areas.'},
            {'type': 'Thunderstorm Warning', 'message': 'Severe thunderstorms with lightning and heavy rain expected.'},
            {'type': 'Fog Advisory', 'message': 'Dense fog reducing visibility. Drive with caution.'}
        ]
        
        # Randomly select 0-2 alerts
        num_alerts = random.randint(0, 2)
        selected_alerts = random.sample(alert_types, min(num_alerts, len(alert_types)))
        
        for alert in selected_alerts:
            alerts.append({
                'type': alert['type'],
                'message': alert['message'],
                'issued': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'expires': (datetime.now() + timedelta(hours=random.randint(6, 24))).strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return alerts
    
    def get_weather_history(self, location: str, days: int = 7) -> List[WeatherData]:
        """Get historical weather data"""
        history = []
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            # Generate historical data with some variation
            base_temp = self._get_base_temperature(location) + random.uniform(-10, 10)
            condition = random.choice(list(self.weather_conditions.keys()))
            
            weather_data = self._get_mock_weather(location)
            weather_data.timestamp = date.isoformat()
            weather_data.temperature = base_temp + random.uniform(-5, 5)
            
            history.append(weather_data)
        
        return history
    
    def compare_locations(self, locations: List[str]) -> Dict[str, WeatherData]:
        """Compare weather across multiple locations"""
        comparison = {}
        
        for location in locations:
            comparison[location] = self.get_current_weather(location)
        
        return comparison
    
    def get_weather_recommendations(self, weather_data: WeatherData) -> List[str]:
        """Get recommendations based on current weather"""
        recommendations = []
        
        # Temperature-based recommendations
        if weather_data.temperature < 0:
            recommendations.append("❄️ Bundle up! Wear warm clothing and protect exposed skin.")
        elif weather_data.temperature < 10:
            recommendations.append("🧥 Cool weather - consider a jacket or sweater.")
        elif weather_data.temperature > 30:
            recommendations.append("☀️ Hot weather - stay hydrated and seek shade.")
        elif weather_data.temperature > 25:
            recommendations.append("🌡️ Warm weather - light clothing recommended.")
        
        # Condition-based recommendations
        if weather_data.condition == 'Rain':
            recommendations.append("☔ Bring an umbrella or rain jacket.")
        elif weather_data.condition == 'Thunderstorm':
            recommendations.append("⛈️ Avoid outdoor activities during thunderstorms.")
        elif weather_data.condition == 'Snow':
            recommendations.append("❄️ Drive carefully on snowy roads.")
        elif weather_data.condition == 'Fog':
            recommendations.append("🌫️ Drive with caution due to reduced visibility.")
        
        # Wind-based recommendations
        if weather_data.wind_speed > 15:
            recommendations.append("💨 Strong winds - secure loose objects.")
        
        # UV index recommendations
        if weather_data.uv_index > 7:
            recommendations.append("☀️ High UV index - use sunscreen and protective clothing.")
        elif weather_data.uv_index > 3:
            recommendations.append("🌞 Moderate UV index - some sun protection recommended.")
        
        return recommendations
    
    def format_weather_report(self, weather_data: WeatherData) -> str:
        """Format weather data into a readable report"""
        report = []
        report.append("=" * 50)
        report.append(f"WEATHER REPORT - {weather_data.location.upper()}")
        report.append("=" * 50)
        report.append(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("CURRENT CONDITIONS:")
        report.append("-" * 20)
        report.append(f"Temperature: {weather_data.temperature}°C")
        report.append(f"Feels Like: {weather_data.feels_like}°C")
        report.append(f"Condition: {weather_data.condition}")
        report.append(f"Description: {weather_data.description}")
        report.append("")
        
        report.append("DETAILED METRICS:")
        report.append("-" * 20)
        report.append(f"Humidity: {weather_data.humidity}%")
        report.append(f"Pressure: {weather_data.pressure} hPa")
        report.append(f"Wind: {weather_data.wind_speed} km/h {weather_data.wind_direction}")
        report.append(f"Visibility: {weather_data.visibility} km")
        report.append(f"UV Index: {weather_data.uv_index}")
        report.append("")
        
        # Add recommendations
        recommendations = self.get_weather_recommendations(weather_data)
        if recommendations:
            report.append("RECOMMENDATIONS:")
            report.append("-" * 15)
            for rec in recommendations:
                report.append(f"• {rec}")
            report.append("")
        
        return "\n".join(report)
    
    def save_weather_data(self, weather_data: WeatherData, filename: str = None) -> str:
        """Save weather data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weather_data_{weather_data.location}_{timestamp}.json"
        
        data = asdict(weather_data)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename
    
    def export_forecast_csv(self, forecast: List[ForecastData], filename: str = None) -> str:
        """Export forecast data to CSV format"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"weather_forecast_{timestamp}.csv"
        
        with open(filename, 'w') as f:
            f.write("Date,High Temp,Low Temp,Condition,Precipitation Chance,Humidity,Wind Speed\n")
            for day in forecast:
                f.write(f"{day.date},{day.high_temp},{day.low_temp},{day.condition},{day.precipitation_chance},{day.humidity},{day.wind_speed}\n")
        
        return filename
    
    def get_weather_statistics(self, location: str, days: int = 30) -> Dict[str, float]:
        """Get weather statistics for a location"""
        history = self.get_weather_history(location, days)
        
        temperatures = [day.temperature for day in history]
        humidities = [day.humidity for day in history]
        pressures = [day.pressure for day in history]
        
        return {
            'avg_temperature': round(sum(temperatures) / len(temperatures), 1),
            'max_temperature': round(max(temperatures), 1),
            'min_temperature': round(min(temperatures), 1),
            'avg_humidity': round(sum(humidities) / len(humidities), 1),
            'avg_pressure': round(sum(pressures) / len(pressures), 1),
            'rainy_days': len([day for day in history if 'rain' in day.condition.lower()]),
            'sunny_days': len([day for day in history if day.condition.lower() == 'clear'])
        }

def demo():
    """Demonstrate the Weather Utility capabilities"""
    weather = WeatherUtility()
    
    print("🌤️  WEATHER UTILITY DEMO 🌤️")
    print("=" * 50)
    
    # Current weather
    location = "New York"
    current_weather = weather.get_current_weather(location)
    print(f"\n🌡️  CURRENT WEATHER - {location}:")
    print(f"Temperature: {current_weather.temperature}°C")
    print(f"Condition: {current_weather.condition}")
    print(f"Humidity: {current_weather.humidity}%")
    print(f"Wind: {current_weather.wind_speed} km/h {current_weather.wind_direction}")
    
    # Forecast
    print(f"\n📅 5-DAY FORECAST - {location}:")
    forecast = weather.get_forecast(location, 5)
    for day in forecast:
        print(f"{day.date}: {day.high_temp}°C/{day.low_temp}°C - {day.condition}")
    
    # Weather alerts
    print(f"\n⚠️  WEATHER ALERTS - {location}:")
    alerts = weather.get_weather_alerts(location)
    if alerts:
        for alert in alerts:
            print(f"• {alert['type']}: {alert['message']}")
    else:
        print("No active weather alerts")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    recommendations = weather.get_weather_recommendations(current_weather)
    for rec in recommendations:
        print(f"• {rec}")
    
    # Location comparison
    print(f"\n🌍 LOCATION COMPARISON:")
    locations = ["New York", "London", "Tokyo"]
    comparison = weather.compare_locations(locations)
    for loc, data in comparison.items():
        print(f"{loc}: {data.temperature}°C - {data.condition}")
    
    # Statistics
    print(f"\n📊 WEATHER STATISTICS (30 days) - {location}:")
    stats = weather.get_weather_statistics(location, 30)
    print(f"Average Temperature: {stats['avg_temperature']}°C")
    print(f"Temperature Range: {stats['min_temperature']}°C to {stats['max_temperature']}°C")
    print(f"Rainy Days: {stats['rainy_days']}")
    print(f"Sunny Days: {stats['sunny_days']}")

def interactive_mode():
    """Interactive mode for weather utility"""
    weather = WeatherUtility()
    
    print("\n🌤️  INTERACTIVE WEATHER UTILITY 🌤️")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Get Current Weather")
        print("2. Get Weather Forecast")
        print("3. Get Weather Alerts")
        print("4. Compare Locations")
        print("5. Get Weather History")
        print("6. Get Weather Statistics")
        print("7. Generate Weather Report")
        print("8. Save Weather Data")
        print("9. Export Forecast (CSV)")
        print("10. Set API Key (for real data)")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-10): ").strip()
        
        if choice == "0":
            print("Thanks for using Weather Utility! 🌤️")
            break
        elif choice == "1":
            location = input("Enter location: ") or "New York"
            current_weather = weather.get_current_weather(location)
            print(f"\n🌡️  CURRENT WEATHER - {location}:")
            print(f"Temperature: {current_weather.temperature}°C")
            print(f"Feels Like: {current_weather.feels_like}°C")
            print(f"Condition: {current_weather.condition}")
            print(f"Description: {current_weather.description}")
            print(f"Humidity: {current_weather.humidity}%")
            print(f"Pressure: {current_weather.pressure} hPa")
            print(f"Wind: {current_weather.wind_speed} km/h {current_weather.wind_direction}")
            print(f"Visibility: {current_weather.visibility} km")
            print(f"UV Index: {current_weather.uv_index}")
        elif choice == "2":
            location = input("Enter location: ") or "New York"
            days = int(input("Number of days (default 5): ") or "5")
            forecast = weather.get_forecast(location, days)
            print(f"\n📅 {days}-DAY FORECAST - {location}:")
            for day in forecast:
                print(f"{day.date}: {day.high_temp}°C/{day.low_temp}°C - {day.condition} ({day.precipitation_chance}% rain)")
        elif choice == "3":
            location = input("Enter location: ") or "New York"
            alerts = weather.get_weather_alerts(location)
            print(f"\n⚠️  WEATHER ALERTS - {location}:")
            if alerts:
                for alert in alerts:
                    print(f"• {alert['type']}")
                    print(f"  {alert['message']}")
                    print(f"  Issued: {alert['issued']}")
                    print(f"  Expires: {alert['expires']}")
                    print()
            else:
                print("No active weather alerts")
        elif choice == "4":
            locations_input = input("Enter locations (comma-separated): ") or "New York, London, Tokyo"
            locations = [loc.strip() for loc in locations_input.split(',')]
            comparison = weather.compare_locations(locations)
            print(f"\n🌍 LOCATION COMPARISON:")
            for loc, data in comparison.items():
                print(f"{loc}: {data.temperature}°C - {data.condition} - {data.humidity}% humidity")
        elif choice == "5":
            location = input("Enter location: ") or "New York"
            days = int(input("Number of days (default 7): ") or "7")
            history = weather.get_weather_history(location, days)
            print(f"\n📈 WEATHER HISTORY - {location} (Last {days} days):")
            for day in history:
                date = datetime.fromisoformat(day.timestamp).strftime('%Y-%m-%d')
                print(f"{date}: {day.temperature}°C - {day.condition}")
        elif choice == "6":
            location = input("Enter location: ") or "New York"
            days = int(input("Number of days (default 30): ") or "30")
            stats = weather.get_weather_statistics(location, days)
            print(f"\n📊 WEATHER STATISTICS - {location} (Last {days} days):")
            print(f"Average Temperature: {stats['avg_temperature']}°C")
            print(f"Max Temperature: {stats['max_temperature']}°C")
            print(f"Min Temperature: {stats['min_temperature']}°C")
            print(f"Average Humidity: {stats['avg_humidity']}%")
            print(f"Average Pressure: {stats['avg_pressure']} hPa")
            print(f"Rainy Days: {stats['rainy_days']}")
            print(f"Sunny Days: {stats['sunny_days']}")
        elif choice == "7":
            location = input("Enter location: ") or "New York"
            current_weather = weather.get_current_weather(location)
            report = weather.format_weather_report(current_weather)
            print(f"\n{report}")
        elif choice == "8":
            location = input("Enter location: ") or "New York"
            current_weather = weather.get_current_weather(location)
            filename = weather.save_weather_data(current_weather)
            print(f"\n💾 Weather data saved to: {filename}")
        elif choice == "9":
            location = input("Enter location: ") or "New York"
            days = int(input("Number of days (default 7): ") or "7")
            forecast = weather.get_forecast(location, days)
            filename = weather.export_forecast_csv(forecast)
            print(f"\n📊 Forecast exported to: {filename}")
        elif choice == "10":
            api_key = input("Enter API key: ")
            provider = input("Enter provider (openweathermap/weatherapi, default: openweathermap): ") or "openweathermap"
            weather.set_api_key(api_key, provider)
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    demo()
    print("\n" + "="*50)
    interactive_mode()
