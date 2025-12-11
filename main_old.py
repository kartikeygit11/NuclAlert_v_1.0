import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import geocoder
import folium
from streamlit_folium import folium_static
from plyer import notification
import time

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Nuclear Radiation Detection",
    page_icon="☢️",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# Custom CSS for dark theme styling
st.markdown("""
    <style>
        .main {
            background-color: #121212;
            color: white;
        }
        .stAlert {
            border-radius: 10px;
            background-color: #1e1e1e;
        }
        .st-bb {
            background-color: #1e1e1e;
        }
        .st-at {
            background-color: #2d2d2d;
        }
        .metric-card {
            background: #1e1e1e;
            color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 15px;
            border: 1px solid #333;
        }
        .header {
            background: linear-gradient(135deg, #8B0000, #B22222);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #444;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1a1a2e, #16213e);
            color: white;
        }
        .tab-content {
            padding: 15px;
            background: #1e1e1e;
            color: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            border: 1px solid #333;
        }
        .plant-card {
            border-left: 5px solid;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            background: #1e1e1e;
            color: white;
            border: 1px solid #333;
        }
        .safe {
            border-color: #28a745;
        }
        .moderate {
            border-color: #ffc107;
        }
        .dangerous {
            border-color: #dc3545;
        }
        .css-1aumxhk {
            background-color: #121212;
            color: white;
        }
        .st-b7 {
            color: white;
        }
        .st-c0 {
            background-color: #121212;
        }
        .st-c1 {
            background-color: #1e1e1e;
        }
        .st-c2 {
            color: white;
        }
        .stDataFrame {
            background-color: #1e1e1e;
            color: white;
        }
        .st-eb {
            background-color: #1e1e1e;
        }
        .st-d8 {
            color: white;
        }
        .st-dh {
            color: white;
        }
        .st-df {
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
        }
        .stDownloadButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
        }
        .stTextInput>div>div>input {
            background-color: #1e1e1e;
            color: white;
        }
        .stSelectbox>div>div>select {
            background-color: #1e1e1e;
            color: white;
        }
        .stFileUploader>div>div>div>div {
            background-color: #1e1e1e;
            color: white;
        }
        .stExpander {
            background-color: #1e1e1e;
            color: white;
            border: 1px solid #333;
        }
        .css-1y4p8pa {
            background-color: #121212;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- INTRO PAGE -----------------
if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:
    st.markdown(
        """
        <div class="header">
            <h1 style='text-align:center;'>☢️ Nuclear Radiation Detection & Safety Dashboard</h1>
            <p style='text-align:center; font-size:18px;'>
            A real-time monitoring system designed to detect, analyze, and alert users when they are near nuclear radiation zones.
            Stay informed. Stay safe.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Radiation_warning_symbol.svg/600px-Radiation_warning_symbol.svg.png",
            width=120
        )

    st.markdown("## 🔍 Project Overview")
    with st.expander("Learn more about this dashboard"):
        st.write("""
        This advanced monitoring system provides:
        - **Real-time location tracking** with GPS precision
        - **Nuclear plant safety classification** based on operational age and safety records
        - **Instant alerts** with desktop notifications when in dangerous proximity
        - **Interactive heatmap** visualization of radiation risk zones
        - **Custom data integration** for personalized monitoring
        """)

    st.markdown("## ⚙️ How It Works")
    with st.expander("See how the system operates"):
        st.write("""
        1. **Upload** a CSV file containing nuclear plant details (Name, Latitude, Longitude, Age)
        2. The system **pinpoints your location** automatically with IP geolocation
        3. It **calculates precise distances** between you and each plant
        4. Plants are classified as:
            - 🟢 **Safe** (Under 15 years old)
            - 🟠 **Moderate** (15-40 years old)
            - 🔴 **Dangerous** (Over 40 years old)
        5. You receive **real-time notifications** when entering risk zones
        """)                                                                       

    st.markdown("## 📌 Technology Stack")
    with st.expander("View technical details"):
        st.write("""
        - **Python 3.9+** (Core application logic)
        - **Streamlit** (Interactive web interface)
        - **Geopy** (Accurate distance calculations)
        - **Folium** (Interactive Leaflet maps)
        - **Plyer** (Cross-platform desktop notifications)
        - **Pandas** (Data processing and analysis)
        """)

    st.markdown("---")
    if st.button("🚀 Proceed to Dashboard", type="primary"):
        st.session_state.show_intro = False
        st.rerun()
    st.stop()

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Radiation_warning_symbol.svg/600px-Radiation_warning_symbol.svg.png" width="90">
        <h2>☢️ Nuclear Safety Dashboard</h2>
        <p>Real-time nuclear hazard tracking</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📂 Data Upload")
    uploaded_file = st.file_uploader("Upload plant data CSV", type=["csv"], help="CSV should contain columns: Name, Latitude, Longitude, Age")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    This dashboard provides real-time monitoring of nuclear radiation risks in your vicinity.
    Developed for public safety awareness.
    """)
    
    st.markdown("---")
    
    with st.expander("Safety Guidelines"):
        st.markdown("""
        - Stay at least **50km** from dangerous plants
        - Limit exposure time in moderate zones
        - Follow local emergency procedures
        - Monitor radiation levels regularly
        """)

# ----------------- MAIN CONTENT -----------------
st.markdown("""
<div class="header">
    <h1 style='text-align: center;'>📊 Nuclear Power Plant Analysis</h1>
    <p style='text-align: center; font-size:18px;'>Monitor and receive instant alerts about nearby nuclear radiation risks.</p>
</div>
""", unsafe_allow_html=True)

# ----------------- VARIABLES -----------------
user_latitude, user_longitude = None, None

if uploaded_file is not None:
    with st.spinner('Loading and analyzing data...'):
        df = pd.read_csv(uploaded_file)
        df.fillna(0, inplace=True)

        # Safety classification with more nuanced criteria
        def calculate_safety(age):
            if pd.isna(age):
                return 'Unknown'
            if age < 15:
                return 'Safe'
            elif 15 <= age < 25:
                return 'Moderate'
            else:
                return 'Dangerous'

        df['Safety'] = df['Age'].apply(calculate_safety)

        # Get user location with retry logic
        def update_user_location():
            global user_latitude, user_longitude
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    user_location = geocoder.ip('me')
                    if user_location.latlng:
                        user_latitude, user_longitude = user_location.latlng
                        return
                except Exception as e:
                    st.warning(f"Location detection attempt {attempt + 1} failed. Retrying...")
                    time.sleep(1)
            st.error("Could not determine your location automatically. Using default coordinates.")
            user_latitude, user_longitude = 40.7128, -74.0060  # Default to NYC

        update_user_location()

        # ----------------- ZONES -----------------
        colors = {
            'Safe': {'color': '#28a745', 'icon': 'check-circle'},
            'Dangerous': {'color': '#dc3545', 'icon': 'exclamation-triangle'},
            'Moderate': {'color': '#ffc107', 'icon': 'exclamation-circle'}
        }
        
        safe_zones, moderate_zones, dangerous_zones = [], [], []
        plant_distances = []

        # Create map with multiple tile options
        map = folium.Map(location=[user_latitude or 0, user_longitude or 0], zoom_start=6, tiles='CartoDB dark_matter')
        folium.TileLayer('openstreetmap').add_to(map)
        folium.TileLayer('stamenterrain').add_to(map)
        folium.TileLayer('cartodbpositron').add_to(map)
        folium.LayerControl().add_to(map)

        for _, row in df.iterrows():
            reactor_safety = row['Safety']
            plant_latitude, plant_longitude = row['Latitude'], row['Longitude']
            
            if user_latitude and user_longitude:
                distance = geodesic((user_latitude, user_longitude), (plant_latitude, plant_longitude)).km
                plant_distances.append({
                    'Name': row['Name'],
                    'Distance': distance,
                    'Safety': reactor_safety,
                    'Age': row['Age']
                })
                
                if reactor_safety == 'Safe' and distance <= 100:
                    safe_zones.append(row['Name'])
                elif reactor_safety == 'Moderate' and distance <= 75:
                    moderate_zones.append(row['Name'])
                elif reactor_safety == 'Dangerous' and distance <= 50:
                    dangerous_zones.append(row['Name'])

            # Customize markers based on safety level
            color = colors.get(reactor_safety, {}).get('color', 'blue')
            icon = colors.get(reactor_safety, {}).get('icon', 'info-circle')
            
            folium.Circle(
                location=[row['Latitude'], row['Longitude']],
                radius=30000,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.2,
                tooltip=f"{row['Name']} - {reactor_safety} ({row['Age']} years)"
            ).add_to(map)
            
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                icon=folium.Icon(
                    color='white',
                    icon_color=color,
                    icon=icon,
                    prefix='fa'
                ),
                popup=f"<b>{row['Name']}</b><br>Age: {row['Age']} years<br>Status: {reactor_safety}"
            ).add_to(map)

        # User marker with pulsating effect
        if user_latitude and user_longitude:
            folium.Marker(
                location=[user_latitude, user_longitude],
                icon=folium.CustomIcon(
                    icon_image="https://cdn-icons-png.flaticon.com/512/447/447031.png",
                    icon_size=(30, 30)
                ),
                tooltip="Your Location"
            ).add_to(map)
            
            folium.Circle(
                location=[user_latitude, user_longitude],
                radius=50000,
                color='#007bff',
                fill=True,
                fill_color='#007bff',
                fill_opacity=0.1,
                tooltip="50km radius from your location"
            ).add_to(map)

        # ----------------- NOTIFICATIONS -----------------
        def send_notification(level, plants):
            if not plants:
                return
                
            if level == 'dangerous':
                notification.notify(
                    title="🚨 HIGH RADIATION ALERT!",
                    message=f"Critical danger! You're within 50km of {len(plants)} dangerous plants: {', '.join(plants)}",
                    timeout=15,
                    app_icon=None
                )
            elif level == 'moderate':
                notification.notify(
                    title="⚠️ Moderate Radiation Warning",
                    message=f"Caution! You're within 75km of {len(plants)} aging plants: {', '.join(plants)}",
                    timeout=10
                )
            elif level == 'safe':
                notification.notify(
                    title="ℹ️ Radiation Monitoring",
                    message=f"You're near {len(plants)} newer plants: {', '.join(plants)}",
                    timeout=5
                )

        # ----------------- LAYOUT -----------------
        tab1, tab2, tab3 = st.tabs(["🚨 Alerts Dashboard", "🌍 Interactive Map", "📊 Plant Data"])

        with tab1:
            st.markdown("### Current Radiation Status")
            
            # Safety metrics cards
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown("""
                <div class="metric-card">
                    <h3>Total Plants</h3>
                    <h2>{}</h2>
                </div>
                """.format(len(df)), unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="metric-card">
                    <h3>Safe Plants</h3>
                    <h2 style="color:#28a745;">{}</h2>
                </div>
                """.format(len(df[df['Safety'] == 'Safe'])), unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div class="metric-card">
                    <h3>Moderate Plants</h3>
                    <h2 style="color:#ffc107;">{}</h2>
                </div>
                """.format(len(df[df['Safety'] == 'Moderate'])), unsafe_allow_html=True)
            
            with col4:
                st.markdown("""
                <div class="metric-card">
                    <h3>Dangerous Plants</h3>
                    <h2 style="color:#dc3545;">{}</h2>
                </div>
                """.format(len(df[df['Safety'] == 'Dangerous'])), unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Alert system
            if dangerous_zones:
                st.error(f"""
                ### 🚨 HIGH RADIATION ALERT
                You are within **50km** of {len(dangerous_zones)} dangerous nuclear plants:
                {', '.join(dangerous_zones)}
                
                **Recommended action:** Evacuate immediately or seek shelter.
                """)
                send_notification('dangerous', dangerous_zones)
            elif moderate_zones:
                st.warning(f"""
                ### ⚠️ Moderate Radiation Warning
                You are within **75km** of {len(moderate_zones)} aging nuclear plants:
                {', '.join(moderate_zones)}
                
                **Recommended action:** Limit outdoor exposure time.
                """)
                send_notification('moderate', moderate_zones)
            elif safe_zones:
                st.success(f"""
                ### ✅ Safe Zone
                You are near {len(safe_zones)} newer nuclear plants:
                {', '.join(safe_zones)}
                
                No immediate danger detected.
                """)
                send_notification('safe', safe_zones)
            else:
                st.info("""
                ### 🌿 Clear Area
                You are not within immediate proximity of any known nuclear plants.
                
                Continue monitoring for updates.
                """)
            
            st.markdown("---")
            
            # Nearby plants list
            st.markdown("### Nearby Nuclear Plants")
            if plant_distances:
                df_distances = pd.DataFrame(plant_distances).sort_values('Distance')
                df_distances['Distance'] = df_distances['Distance'].round(2)
                
                for _, plant in df_distances.head(5).iterrows():
                    safety_class = plant['Safety'].lower()
                    st.markdown(f"""
                    <div class="plant-card {safety_class}">
                        <h4>{plant['Name']}</h4>
                        <p>Distance: <b>{plant['Distance']} km</b> | Age: {plant['Age']} years | Status: <b>{plant['Safety']}</b></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No nuclear plants detected within 100km radius.")

        with tab2:
            st.markdown("### Interactive Radiation Map")
            st.markdown("""
            <p style="font-size:16px;">
            <span style="color:#28a745;">🟢 Safe</span> | 
            <span style="color:#ffc107;">🟠 Moderate</span> | 
            <span style="color:#dc3545;">🔴 Dangerous</span>
            </p>
            """, unsafe_allow_html=True)
            
            folium_static(map, width=1200, height=600)
            
            st.markdown("---")
            st.markdown("**Map Legend**")
            st.markdown("""
            - <img src="https://cdn-icons-png.flaticon.com/512/447/447031.png" width="20"> Your current location
            - <i class="fa fa-check-circle" style="color:#28a745;"></i> Safe nuclear plant
            - <i class="fa fa-exclamation-circle" style="color:#ffc107;"></i> Moderate risk plant
            - <i class="fa fa-exclamation-triangle" style="color:#dc3545;"></i> Dangerous plant
            - <span style="display:inline-block; width:15px; height:15px; background:#007bff; border-radius:50%; opacity:0.1;"></span> 50km radius from your location
            """, unsafe_allow_html=True)

        with tab3:
            st.markdown("### Nuclear Plant Database")
            st.dataframe(df.style.apply(lambda x: [
                f"background-color: {colors.get(val, {}).get('color', 'white')}; color: white" 
                for val in x], subset=['Safety']), 
                use_container_width=True)
            
            st.download_button(
                label="📥 Download Processed Data",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name='processed_nuclear_plants.csv',
                mime='text/csv'
            )

else:
    st.markdown("""
    <div style="text-align:center; padding:50px;">
        <h3>📂 Upload Nuclear Plant Data to Begin</h3>
        <p>Please upload a CSV file containing nuclear plant information to start monitoring.</p>
        <p><small>Sample CSV format: Name, Latitude, Longitude, Age</small></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample data download
    sample_data = pd.DataFrame({
        'Name': ['Plant Alpha', 'Plant Beta', 'Plant Gamma'],
        'Latitude': [40.7128, 34.0522, 41.8781],
        'Longitude': [-74.0060, -118.2437, -87.6298],
        'Age': [10, 25, 45]
    })
    
    st.download_button(
        label="⬇️ Download Sample Data",
        data=sample_data.to_csv(index=False).encode('utf-8'),
        file_name='sample_nuclear_plants.csv',
        mime='text/csv'
    )