# Nuclear Radiation Monitoring System

A real-time monitoring system designed to detect, analyze, and alert users when they are near nuclear radiation zones.

## 🚀 Features

- **Real-time location tracking** with GPS precision
- **Nuclear plant safety classification** based on operational age and safety records
- **Instant alerts** with desktop notifications when in dangerous proximity
- **Interactive heatmap** visualization of radiation risk zones
- **Custom data integration** for personalized monitoring

## 📁 Project Structure

```
Nuclear-Radiation-Monitoring-System/
├── app/
│   ├── __init__.py
│   ├── main.py              # Main Flask application
│   ├── config.py            # Configuration constants
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── location.py      # Location services
│   │   ├── data_processor.py # Data processing utilities
│   │   ├── map_utils.py     # Map visualization
│   │   └── notifications.py # Desktop notifications
│   └── ui/
│       ├── __init__.py
│       ├── components.py    # UI components (legacy)
│       └── styles.py        # CSS styles (legacy)
├── templates/
│   ├── base.html           # Base template
│   ├── intro.html          # Introduction page
│   └── dashboard.html      # Main dashboard
├── static/
│   ├── css/
│   │   └── style.css       # Custom CSS styles
│   └── maps/               # Generated map files
├── uploads/                # Uploaded CSV files
├── data/
│   └── data2.csv           # Sample data file
├── run.py                  # Application entry point
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Nuclear-Radiation-Monitoring-System-main
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

### Running the Application

Run the application using one of the following methods:

**Method 1: Using run.py (Recommended)**
```bash
python run.py
```

**Method 2: Using Flask directly**
```bash
flask run
```

The application will be available at `http://localhost:5000`

### Using the Dashboard

1. **Upload Data**: Upload a CSV file containing nuclear plant data with the following columns:
   - `Name`: Plant name
   - `Latitude`: Plant latitude
   - `Longitude`: Plant longitude
   - `Age`: Plant age in years

2. **View Dashboard**: The dashboard will automatically:
   - Detect your location using IP geolocation
   - Calculate distances to all nuclear plants
   - Classify plants by safety level
   - Display alerts and visualizations

3. **Explore Tabs**:
   - **Alerts Dashboard**: View safety metrics and nearby plants
   - **Interactive Map**: Explore the map with plant locations
   - **Plant Data**: View and download processed data

## 📊 Safety Classifications

Plants are classified based on their age:
- 🟢 **Safe**: Under 15 years old
- 🟠 **Moderate**: 15-40 years old
- 🔴 **Dangerous**: Over 40 years old

## ⚠️ Alert Zones

- **Dangerous Zone**: Within 50km of dangerous plants
- **Moderate Zone**: Within 75km of moderate-risk plants
- **Safe Zone**: Within 100km of safe plants

## 🛠️ Technology Stack

- **Python 3.9+** - Core application logic
- **Flask** - Web framework
- **Geopy** - Accurate distance calculations
- **Folium** - Interactive Leaflet maps
- **Plyer** - Cross-platform desktop notifications
- **Pandas** - Data processing and analysis

## 📝 Sample Data Format

```csv
Name,Latitude,Longitude,Age
Plant Alpha,40.7128,-74.0060,10
Plant Beta,34.0522,-118.2437,25
Plant Gamma,41.8781,-87.6298,45
```

## 🔧 Configuration

You can modify safety thresholds and other settings in `app/config.py`:
- Safety age thresholds
- Distance thresholds
- Map settings
- Notification timeouts

## 📄 License

This project is open source and available for educational purposes.

## ⚠️ Disclaimer

This application is for educational and awareness purposes only. Always follow official safety guidelines and emergency procedures in your area.
