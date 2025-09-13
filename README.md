# Plot Digitizer

A web app that takes in images of plots and attempts to estimate the values associated with those plots.

## Overview
This is a web application that takes in images of plots and analyzes them to extract numerical data points. The current implementation provides a demonstration interface with sample data extraction.

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd plot-digitizer
   ```

2. Run the application:
   ```bash
   python3 app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **Upload Image**: Click "Select Plot Image" and choose a plot/graph image file (PNG, JPG, JPEG, GIF, BMP)

2. **Set Axis Ranges**: Enter the X and Y axis ranges that correspond to your plot's scale

3. **Analyze**: Click "Analyze Plot" to process the image

4. **View Results**: The extracted data points will be displayed in a table format

5. **Export Data**: 
   - Click "Download CSV" to save the data as a CSV file
   - Click "Copy to Clipboard" to copy the data for pasting into other applications

## Current Implementation

This is a **demonstration version** that:
- Provides a fully functional web interface
- Shows how the plot digitizer would work
- Returns sample data points for demonstration purposes
- Includes all the necessary UI components and functionality

## Future Enhancements

For a production version, the following computer vision libraries would be integrated:
- **OpenCV** for image processing and edge detection
- **PIL/Pillow** for image manipulation
- **NumPy** for numerical computations
- **SciPy** for advanced signal processing

The enhanced version would:
- Automatically detect plot axes
- Identify data points using computer vision
- Handle various plot types and styles
- Provide more accurate coordinate extraction
- Support automatic scaling based on detected axis labels

## Architecture

- **Backend**: Python HTTP server (no external dependencies required)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap for styling)
- **File Handling**: Multipart form data processing
- **Data Export**: CSV generation and clipboard integration

## Files Structure

```
plot-digitizer/
├── app.py                 # Main application server
├── templates/
│   └── index.html        # Web interface template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── main.js       # Frontend functionality
├── requirements.txt      # Python dependencies (for future use)
└── README.md            # This file
```

## Technical Details

The application uses a lightweight HTTP server implementation that handles:
- File uploads via multipart form data
- JSON API responses
- Static file serving
- Cross-platform compatibility

The demo implementation provides realistic sample data that demonstrates the expected output format and user experience of a fully functional plot digitizer.
