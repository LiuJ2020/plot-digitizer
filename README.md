# plot-digitizer
A web app that takes in images of plots and attempts to estimate the values associated with those plots.

## Functional Requirements:
1. **Image Upload**: Users should be able to upload images of plots (e.g., PNG, JPEG).
2. **Plot Detection**: The app should detect the plot area within the uploaded image, then put points down on the ends of the x and y axes. It should also recgonize the numerical values on the axes.
3. **Point Selection**: The app should automatically place points on the plot line, but also allow users to manually add, move, or delete points. The points should be used to estimate the values of the plot.
4. **Data Extraction**: The app should extract the (x, y) coordinates of the selected points and convert them into a usable data format (e.g., CSV, JSON).
