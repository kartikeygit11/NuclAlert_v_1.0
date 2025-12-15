"""Main Flask application for Nuclear Radiation Monitoring System."""

from flask import Flask, render_template, request, session, redirect, url_for, send_file, jsonify
import pandas as pd
import os
import io

from app.config import PAGE_CONFIG
from app.utils.location import update_user_location_with_fallback
from app.utils.data_processor import (
    process_plant_data,
    calculate_distances,
    classify_zones
)
from app.utils.map_utils import (
    create_map,
    add_plant_markers,
    add_user_marker
)
from app.utils.notifications import send_notification

# In-memory cache to avoid large cookies (browser session storage has size limits)
DATA_CACHE = {}


def create_app():
    """Create and configure the Flask application."""
    # Get the base directory (project root)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, 
                template_folder=os.path.join(base_dir, 'templates'),
                static_folder=os.path.join(base_dir, 'static'),
                static_url_path='/static')
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Create maps directory if it doesn't exist
    os.makedirs(os.path.join(base_dir, 'static', 'maps'), exist_ok=True)
    
    def load_and_process_data():
        """Load data from data/data2.csv and process it."""
        try:
            # Get the path to data/data2.csv
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            data_path = os.path.join(base_dir, 'data', 'data2.csv')
            
            # Load and process data
            df = pd.read_csv(data_path)
            
            # Handle the first empty column if it exists
            if df.columns[0].strip() == '' or df.columns[0] == 'Unnamed: 0':
                df = df.drop(df.columns[0], axis=1)
            
            # Ensure we have the required columns (Name, Latitude, Longitude, Age)
            # If Age column doesn't exist or has issues, calculate it from OperationalFrom
            if 'Age' not in df.columns:
                df['Age'] = 0
            
            # Fill NaN values in Age column
            if df['Age'].isna().any():
                # Try to calculate age from OperationalFrom if available
                if 'OperationalFrom' in df.columns:
                    from datetime import datetime
                    current_year = datetime.now().year
                    def calculate_age(x):
                        if pd.isna(x):
                            return 0
                        try:
                            # Try to extract year from date string
                            date_str = str(x)
                            if len(date_str) >= 4:
                                year = int(date_str[:4])
                                return max(0, current_year - year)
                        except:
                            pass
                        return 0
                    df['Age'] = df.apply(
                        lambda row: row['Age'] if pd.notna(row['Age']) and row['Age'] > 0 
                        else calculate_age(row.get('OperationalFrom', 0)), 
                        axis=1
                    )
                else:
                    df['Age'] = df['Age'].fillna(0)
            
            # Ensure Age is numeric
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(0)
            
            # Filter to only required columns
            required_cols = ['Name', 'Latitude', 'Longitude', 'Age']
            # Check if all required columns exist
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            df = df[required_cols].copy()
            
            # Add a reference plant near Prayagraj / Allahabad for demo alerts
            prayagraj_plant = {
                'Name': 'Prayagraj Research Reactor',
                'Latitude': 25.4358,
                'Longitude': 81.8463,
                'Age': 22  # Moderate by default thresholds
            }
            df = pd.concat([df, pd.DataFrame([prayagraj_plant])], ignore_index=True)
            
            # Remove rows with missing essential data
            df = df.dropna(subset=['Name', 'Latitude', 'Longitude'])
            
            df = process_plant_data(df)
            
            # Get user location
            user_latitude, user_longitude = update_user_location_with_fallback()
            
            # Calculate distances and classify zones
            plant_distances = calculate_distances(df, user_latitude, user_longitude)
            safe_zones, moderate_zones, dangerous_zones = classify_zones(
                df, user_latitude, user_longitude
            )
            # Detect if user is on-site (within 1km of any plant)
            on_site_plants = [
                plant['Name'] for plant in plant_distances
                if plant.get('Distance') is not None and plant['Distance'] <= 1
            ]
            
            # Create map
            map_obj = create_map(user_latitude, user_longitude)
            add_plant_markers(map_obj, df)
            add_user_marker(map_obj, user_latitude, user_longitude, on_site_plants)
            
            # Save map to HTML
            map_filename = f"map_{session.get('map_id', 0)}.html"
            map_path = os.path.join(base_dir, 'static', 'maps', map_filename)
            map_obj.save(map_path)
            session['map_filename'] = map_filename
            session['map_id'] = session.get('map_id', 0) + 1
            
            # Send notifications
            if dangerous_zones:
                send_notification('dangerous', dangerous_zones)
            elif moderate_zones:
                send_notification('moderate', moderate_zones)
            elif safe_zones:
                send_notification('safe', safe_zones)
            
            # Store data in memory cache (avoid oversized cookies)
            DATA_CACHE['df_data'] = df.to_dict('records')
            DATA_CACHE['plant_distances'] = plant_distances
            DATA_CACHE['safe_zones'] = safe_zones
            DATA_CACHE['moderate_zones'] = moderate_zones
            DATA_CACHE['dangerous_zones'] = dangerous_zones
            DATA_CACHE['user_latitude'] = user_latitude
            DATA_CACHE['user_longitude'] = user_longitude
            DATA_CACHE['on_site_plants'] = on_site_plants
            DATA_CACHE['map_filename'] = map_filename
            
            return {
                'success': True,
                'total_plants': len(df),
                'safe_count': len(df[df['Safety'] == 'Safe']),
                'moderate_count': len(df[df['Safety'] == 'Moderate']),
                'dangerous_count': len(df[df['Safety'] == 'Dangerous']),
                'safe_zones': safe_zones,
                'moderate_zones': moderate_zones,
                'dangerous_zones': dangerous_zones,
                'map_filename': map_filename,
                'on_site_plants': on_site_plants
            }
        except Exception as e:
            return {'error': f'Error processing data: {str(e)}'}
    
    @app.route('/')
    def index():
        """Main index page - shows intro or dashboard."""
        if 'show_intro' not in session:
            session['show_intro'] = True
        
        if session.get('show_intro'):
            return render_template('intro.html', PAGE_CONFIG=PAGE_CONFIG)
        
        # Load and process data automatically
        if 'df_data' not in session:
            load_and_process_data()
        
        return render_template('dashboard.html', PAGE_CONFIG=PAGE_CONFIG)
    
    @app.route('/skip_intro', methods=['POST'])
    def skip_intro():
        """Skip the intro page."""
        session['show_intro'] = False
        # Load and process data when skipping intro
        load_and_process_data()
        return redirect(url_for('index'))
    
    @app.route('/load_data', methods=['GET'])
    def load_data():
        """Load and process data from data/data2.csv."""
        result = load_and_process_data()
        if result.get('error'):
            return jsonify(result), 500
        return jsonify(result)
    
    @app.route('/get_data')
    def get_data():
        """Get processed data for display."""
        if 'df_data' not in DATA_CACHE:
            return jsonify({'error': 'No data available'}), 404
        
        return jsonify({
            'plants': DATA_CACHE.get('df_data', []),
            'distances': DATA_CACHE.get('plant_distances', []),
            'safe_zones': DATA_CACHE.get('safe_zones', []),
            'moderate_zones': DATA_CACHE.get('moderate_zones', []),
            'dangerous_zones': DATA_CACHE.get('dangerous_zones', []),
            'map_filename': DATA_CACHE.get('map_filename', ''),
            'on_site_plants': DATA_CACHE.get('on_site_plants', [])
        })
    
    @app.route('/download_processed')
    def download_processed():
        """Download processed data as CSV."""
        if 'df_data' not in session:
            return jsonify({'error': 'No data available'}), 404
        
        df = pd.DataFrame(session['df_data'])
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='processed_nuclear_plants.csv'
        )
    
    
    return app
