# Quick Start Guide

## 🚀 Running the Application

After installing dependencies with `pip install -r requirements.txt`, run the application using:

```bash
streamlit run run.py
```

Or alternatively:

```bash
streamlit run app/main.py
```

## 📁 Project Structure Overview

The project has been restructured into modular components:

- **`app/config.py`** - All configuration constants and settings
- **`app/ui/styles.py`** - CSS styling
- **`app/ui/components.py`** - All UI components (intro, sidebar, tabs)
- **`app/utils/location.py`** - Location detection services
- **`app/utils/data_processor.py`** - Data processing and safety calculations
- **`app/utils/map_utils.py`** - Map creation and visualization
- **`app/utils/notifications.py`** - Desktop notification system
- **`app/main.py`** - Main application logic (orchestrates all modules)
- **`run.py`** - Entry point for running the application

## 🔧 Making Changes

- **Change styling?** → Edit `app/ui/styles.py`
- **Modify safety thresholds?** → Edit `app/config.py`
- **Update UI components?** → Edit `app/ui/components.py`
- **Change data processing?** → Edit `app/utils/data_processor.py`
- **Modify map display?** → Edit `app/utils/map_utils.py`

## ✅ Benefits of This Structure

1. **Modularity** - Each component has a single responsibility
2. **Maintainability** - Easy to find and update specific features
3. **Testability** - Each module can be tested independently
4. **Scalability** - Easy to add new features without cluttering code
5. **Readability** - Clear separation of concerns

