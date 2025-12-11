"""UI components for the Streamlit application."""

import streamlit as st
import pandas as pd
from app.config import SAFETY_COLORS


def render_intro_page():
    """Render the introduction/welcome page."""
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


def render_sidebar():
    """Render the sidebar with file upload and information."""
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
        uploaded_file = st.file_uploader(
            "Upload plant data CSV",
            type=["csv"],
            help="CSV should contain columns: Name, Latitude, Longitude, Age"
        )
        
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
    
    return uploaded_file


def render_header():
    """Render the main page header."""
    st.markdown("""
    <div class="header">
        <h1 style='text-align: center;'>📊 Nuclear Power Plant Analysis</h1>
        <p style='text-align: center; font-size:18px;'>Monitor and receive instant alerts about nearby nuclear radiation risks.</p>
    </div>
    """, unsafe_allow_html=True)


def render_alerts_tab(df, safe_zones, moderate_zones, dangerous_zones, plant_distances):
    """Render the alerts dashboard tab."""
    st.markdown("### Current Radiation Status")
    
    # Safety metrics cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Plants</h3>
            <h2>{len(df)}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Safe Plants</h3>
            <h2 style="color:#28a745;">{len(df[df['Safety'] == 'Safe'])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Moderate Plants</h3>
            <h2 style="color:#ffc107;">{len(df[df['Safety'] == 'Moderate'])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Dangerous Plants</h3>
            <h2 style="color:#dc3545;">{len(df[df['Safety'] == 'Dangerous'])}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Alert system
    if dangerous_zones:
        st.error(f"""
        ### 🚨 HIGH RADIATION ALERT
        You are within **50km** of {len(dangerous_zones)} dangerous nuclear plants:
        {', '.join(dangerous_zones)}
        
        **Recommended action:** Evacuate immediately or seek shelter.
        """)
    elif moderate_zones:
        st.warning(f"""
        ### ⚠️ Moderate Radiation Warning
        You are within **75km** of {len(moderate_zones)} aging nuclear plants:
        {', '.join(moderate_zones)}
        
        **Recommended action:** Limit outdoor exposure time.
        """)
    elif safe_zones:
        st.success(f"""
        ### ✅ Safe Zone
        You are near {len(safe_zones)} newer nuclear plants:
        {', '.join(safe_zones)}
        
        No immediate danger detected.
        """)
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


def render_map_tab(map_obj):
    """Render the interactive map tab."""
    from streamlit_folium import folium_static
    
    st.markdown("### Interactive Radiation Map")
    st.markdown("""
    <p style="font-size:16px;">
    <span style="color:#28a745;">🟢 Safe</span> | 
    <span style="color:#ffc107;">🟠 Moderate</span> | 
    <span style="color:#dc3545;">🔴 Dangerous</span>
    </p>
    """, unsafe_allow_html=True)
    
    folium_static(map_obj, width=1200, height=600)
    
    st.markdown("---")
    st.markdown("**Map Legend**")
    st.markdown("""
    - <img src="https://cdn-icons-png.flaticon.com/512/447/447031.png" width="20"> Your current location
    - <i class="fa fa-check-circle" style="color:#28a745;"></i> Safe nuclear plant
    - <i class="fa fa-exclamation-circle" style="color:#ffc107;"></i> Moderate risk plant
    - <i class="fa fa-exclamation-triangle" style="color:#dc3545;"></i> Dangerous plant
    - <span style="display:inline-block; width:15px; height:15px; background:#007bff; border-radius:50%; opacity:0.1;"></span> 50km radius from your location
    """, unsafe_allow_html=True)


def render_data_tab(df):
    """Render the plant data tab."""
    st.markdown("### Nuclear Plant Database")
    
    # Apply styling to dataframe
    def style_safety(val):
        color = SAFETY_COLORS.get(val, {}).get('color', 'white')
        return f"background-color: {color}; color: white"
    
    styled_df = df.style.applymap(style_safety, subset=['Safety'])
    st.dataframe(styled_df, use_container_width=True)
    
    st.download_button(
        label="📥 Download Processed Data",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='processed_nuclear_plants.csv',
        mime='text/csv'
    )


def render_upload_prompt():
    """Render the upload prompt when no file is uploaded."""
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

