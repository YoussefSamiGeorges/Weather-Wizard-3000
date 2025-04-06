# Weather Wizard 3000 🌦️

A personal weather forecasting assistant with AI-powered outfit recommendations, built in Python.

![WhatsApp Image 2025-04-07 at 00 44 47](https://github.com/user-attachments/assets/93c72502-7f23-41ec-85ff-5440fe69a86d)

## 📋 Overview

Weather Wizard 3000 is a command-line application that provides weather forecasts and personalized outfit recommendations. The app fetches real-time weather data using the OpenWeatherMap API and leverages AI to suggest appropriate clothing based on the current conditions.

### ✨ Features

- **5-day weather forecast** - Get weather predictions for today and the next 4 days
- **Multiple location options**:
  - Search by city name
  - Auto-detect location using IP address
  - Enter coordinates manually
- **Comprehensive weather data**:
  - Temperature (max, min, and feels like)
  - Humidity levels
  - Rain predictions
- **AI-powered outfit suggestions** tailored to weather conditions
- **User-friendly interface** with emoji-enhanced output for better readability

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Internet connection
- OpenWeatherMap API key
- (Optional) Google Gemini API key for AI outfit suggestions

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/weather-wizard-3000.git
   cd weather-wizard-3000
   ```

2. Install required dependencies:
   ```bash
   pip install requests
   ```

3. Set up environment variables:
   ```bash
   # Linux/MacOS
   export OWM_API_KEY="your_openweathermap_api_key"
   export GEMINI_API_KEY="your_gemini_api_key" # Optional for AI outfit suggestions

   # Windows
   set OWM_API_KEY=your_openweathermap_api_key
   set GEMINI_API_KEY=your_gemini_api_key # Optional for AI outfit suggestions
   ```

### Usage

Run the application:
```bash
python main.py
```

Follow the interactive prompts to:
1. Select a date for the forecast
2. Choose a location method
3. Get your weather forecast
4. (Optional) Receive AI-powered outfit recommendations

## 📊 Project Structure

```
weather-wizard-3000/
├── main.py          # Main application with UI logic
├── WeatherApp.py    # Weather data processing and API interactions
└── README.md        # Project documentation
```

## 🧮 How It Works

1. The application fetches weather data from OpenWeatherMap's forecast API
2. It processes the JSON response to extract relevant weather information
3. For outfit suggestions, it sends a prompt to Google's Gemini API with the weather data
4. The AI generates contextually appropriate clothing recommendations

## 🔒 Privacy and Security

- The application uses your location only for weather forecasting purposes
- API keys should be stored as environment variables, not hardcoded
- The AI component does not store any personal information

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔄 Future Improvements

- [ ] GUI interface
- [ ] Mobile app version
- [ ] Weather alerts and notifications
- [ ] Support for more weather data points (wind, UV index, etc.)
- [ ] Saved location favorites
- [ ] Historical weather data
