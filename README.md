# plot-digitizer
A web app that takes in images of plots and attempts to estimate the values associated with those plots.

# Setup Instructions:

### Python Setup:
0. Enter your backend folder:
   ```bash
   cd backend/
   ```
1. Make a virtual environment:
   ```bash
   python3 -m venv venv
   ```
2. Activate the virtual environment:
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
    - On Windows:  
      ```bash
      .\venv\Scripts\activate
      ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Functional Requirements:
1. **Image Upload**: Users should be able to upload images of plots (e.g., PNG, JPEG).
2. **Plot Detection**: The app should detect the plot area within the uploaded image, then put points down on the ends of the x and y axes. It should also recgonize the numerical values on the axes.
3. **Point Selection**: The app should automatically place points on the plot line, but also allow users to manually add, move, or delete points. The points should be used to estimate the values of the plot.
4. **Data Extraction**: The app should extract the (x, y) coordinates of the selected points and convert them into a usable data format (e.g., CSV, JSON).
