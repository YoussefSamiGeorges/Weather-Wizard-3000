import json
import requests
import datetime
from typing import Dict, List, Any, Tuple, Optional, Union
import os

class WeatherApp:
    OWM_ENDPOINT: str = "https://api.openweathermap.org/data/2.5/forecast"
    API_KEY: str = os.environ.get("OWM_API_KEY", "")

    def __init__(self) -> None:
        self.city_name: str = ""
        self.will_rain: bool = False
        self.max_temp_k: float = 0.0
        self.feels_like_temp_k: float = 0.0
        self.min_temp_k: float = 0.0
        self.avg_humidity: float = 0.0

    def fetch_weather_data(self, lat: float, lon: float, target_date: datetime.date) -> None:
        url_string: str = f"{self.OWM_ENDPOINT}?lat={lat}&lon={lon}&appid={self.API_KEY}"
        weather_data: Dict[str, Any] = self.make_api_request(url_string)
        self.process_weather_data(weather_data, target_date)

    def fetch_weather_data_with_city_name(self, city_name: str, target_date: datetime.date) -> None:
        url_string: str = f"{self.OWM_ENDPOINT}?q={city_name}&appid={self.API_KEY}"
        weather_data: Dict[str, Any] = self.make_api_request(url_string)
        self.process_weather_data(weather_data, target_date)

    def process_weather_data(self, weather_data: Dict[str, Any], target_date: datetime.date) -> None:
        self.city_name = weather_data["city"]["name"]
        forecasts: List[Dict[str, Any]] = weather_data["list"]

        temp_max: float = float('-inf')
        temp_min: float = float('inf')
        feels_like_total: float = 0.0
        humidity_total: float = 0.0
        count: int = 0
        rain_detected: bool = False

        for hour_data in forecasts:
            dt_txt: str = hour_data["dt_txt"]
            date_time: datetime.date = datetime.datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").date()

            if date_time == target_date:
                main: Dict[str, Any] = hour_data["main"]
                weather: Dict[str, Any] = hour_data["weather"][0]

                condition_code: int = weather["id"]
                if condition_code < 700:
                    rain_detected = True

                current_temp_max: float = main["temp_max"]
                current_temp_min: float = main["temp_min"]
                current_feels_like: float = main["feels_like"]

                temp_max = max(temp_max, current_temp_max)
                temp_min = min(temp_min, current_temp_min)
                feels_like_total += current_feels_like
                humidity_total += main["humidity"]
                count += 1

        if count > 0:
            self.will_rain = rain_detected
            self.max_temp_k = temp_max
            self.min_temp_k = temp_min
            self.feels_like_temp_k = feels_like_total / count
            self.avg_humidity = humidity_total / count

    def get_weather_message(self) -> str:
        max_converted: List[float] = self.convert_kelvin_to_celsius_fahrenheit(self.max_temp_k)
        feels_like_converted: List[float] = self.convert_kelvin_to_celsius_fahrenheit(self.feels_like_temp_k)
        min_converted: List[float] = self.convert_kelvin_to_celsius_fahrenheit(self.min_temp_k)

        rain_message: str = "☔ Rain expected! Bring an umbrella!" if self.will_rain else "🌤️ No rain today!"

        return (
            f"🌡️ Today's weather in {self.city_name}:\n"
            f"- Max Temp: {max_converted[0]:.2f}°C / {max_converted[1]:.2f}°F\n"
            f"- Feels Like: {feels_like_converted[0]:.2f}°C / {feels_like_converted[1]:.2f}°F\n"
            f"- Min Temp: {min_converted[0]:.2f}°C / {min_converted[1]:.2f}°F\n"
            f"- Avg Humidity: {self.avg_humidity:.2f}%\n"
            f"{rain_message}\n"
        )

    @staticmethod
    def convert_kelvin_to_celsius_fahrenheit(kelvin: float) -> List[float]:
        celsius: float = kelvin - 273.15
        fahrenheit: float = celsius * 9 / 5 + 32
        return [celsius, fahrenheit]

    @staticmethod
    def make_api_request(url_string: str) -> Dict[str, Any]:
        response: requests.Response = requests.get(url_string)
        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}")
        return response.json()

    @staticmethod
    def get_auto_location() -> List[float]:
        try:
            response: requests.Response = requests.get("https://ipinfo.io/json")
            if response.status_code != 200:
                raise Exception(f"Location API request failed with status code {response.status_code}")

            data: Dict[str, Any] = response.json()
            loc: List[str] = data["loc"].split(",")
            return [float(loc[0]), float(loc[1])]
        except Exception as e:
            print(f"Error getting location: {str(e)}")
            # Default coordinates
            return [46.947975, 7.447447]

    def ai_suggestion(self) -> str:
        weather_summary: str = self.get_weather_message()
        prompt: str = (
            "Let's play a role play."
            "You are Weather Wizard 3000 not Gemini."
            "You are my personal weather forecasting assistant"
            " that helps me stay comfy and stylish in any weather."
            f"Based on this weather summary: {weather_summary}"
            " (I'm a 20-year-old man)"
            " Recommend 3 outfits with these rules:"
            "\n1. ALWAYS include a jacket if temperature <15°C/59°F"
            "\n2. Single response format (not chat)"
            "\n3. Follow this exact structure:"
            "\n     * Mandatory:"
            "\n         * Top garment: ex: Black shirt, Green chemise, or red T-shirt ... etc."
            "\n         * Lower garment: ex: Black Jens, grey short  ...etc."
            "\n         * Shoes: ex: White sneakers, Classic shoes, grey sport shoes"
            "\n     * Elective (You can add it or no depends on the suggestion custom):"
            "\n         * Jacket: Black Pump jacket, Blue Jens jacket, blue Pump jacket ... etc"
            "\n         * Different accessories: ice cap, cap ... etc."
            "\n\nEXAMPLE RESPONSE:"
            "\n\n Hello I am Weather Wizard 3000 your personal weather forecasting assistant"
            "\n that helps you stay comfy and stylish in any weather."
            "\\n\\nHello! I am Weather Wizard 3000, your personal weather forecasting assistant that helps you stay comfy and stylish in any weather.\n"
            "\n"
            "\\n\\nBased on the weather summary: Temperature: 12°C, rainy, moderate wind, here are three outfit recommendations for you:\n"
            "\n"
            "\\n\\n1. **Outfit 1**\n"
            "\\n   - **Mandatory:**\n"
            "\\n     - Top garment: Navy thermal long-sleeve shirt\n"
            "\\n     - Lower garment: Dark grey waterproof trousers\n"
            "\\n     - Shoes: Black waterproof boots\n"
            "\\n     - Jacket: Olive green insulated raincoat\n"
            "\\n   - **Elective:**\n"
            "\\n     - Accessories: Black wool beanie, umbrella\n"
            "\n"
            "\\n\\n2. **Outfit 2**\n"
            "\\n   - **Mandatory:**\n"
            "\\n     - Top garment: Charcoal sweater\n"
            "\\n     - Lower garment: Black jeans\n"
            "\\n     - Shoes: Brown leather waterproof shoes\n"
            "\\n     - Jacket: Black hooded parka\n"
            "\\n   - **Elective:**\n"
            "\\n     - Accessories: Grey scarf\n"
            "\n"
            "\\n\\n3. **Outfit 3**\n"
            "\\n   - **Mandatory:**\n"
            "\\n     - Top garment: Blue flannel shirt\n"
            "\\n     - Lower garment: Dark blue chinos\n"
            "\\n     - Shoes: Grey sneakers with waterproof coating\n"
            "\\n     - Jacket: Dark green windproof jacket\n"
            "\\n   - **Elective:**\n"
            "\\n     - Accessories: Baseball cap, waterproof gloves\n"
            "\n"
            "\\n\\nSince the temperature is below 15°C, a jacket is mandatory for each outfit to keep you warm. Additionally, considering the rainy and windy conditions, I've included waterproof and wind-resistant items to ensure you stay dry and comfortable."
        )

        try:
            # Gemini API configuration
            GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")
            GEMINI_URL: str = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

            # Create request payload
            request_body: Dict[str, Any] = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }

            # Make API request
            headers: Dict[str, str] = {"Content-Type": "application/json"}
            response: requests.Response = requests.post(GEMINI_URL, json=request_body, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Gemini API Error: {response.status_code} - {response.text}")

            json_response: Dict[str, Any] = response.json()
            candidates: List[Dict[str, Any]] = json_response.get("candidates", [])

            if candidates and len(candidates) > 0:
                content_obj: Dict[str, Any] = candidates[0].get("content", {})
                parts: List[Dict[str, Any]] = content_obj.get("parts", [])
                if parts and len(parts) > 0:
                    return parts[0].get("text", "No fashion suggestions available.")

            return "No fashion suggestions available."

        except Exception as e:
            print(f"Error generating fashion suggestion: {str(e)}")
            return f"Error generating fashion suggestion: {str(e)}"
