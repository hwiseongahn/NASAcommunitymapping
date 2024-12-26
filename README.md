Algae-CO2 Correlation and Prediction Web Application
Visit it here: https://algaeandco2.up.railway.app/
Project Overview

This web application visualizes the correlation between algal growth and CO2 emissions in Alberta, Canada. By mapping the algae populations in lakes against CO2 emission hotspots, the application helps identify trends and spatial correlations, potentially informing environmental policies and industrial practices. The project is designed to offer valuable insights into how natural algae populations contribute to carbon sequestration and how they may help mitigate the effects of climate change.

In the future, we aim to develop predictive models that use historical data on algae density and CO2 emissions to forecast CO2 levels and assess how algae sequestration can counteract emissions. Incorporating satellite imagery from NASA's Worldview, we also plan to set up a computer vision-based tracker for monitoring algae blooms.

Features

- Heatmaps: Visualize algae population density and CO2 emissions in Alberta using interactive heatmaps.
- Geolocation Integration: Automatically assigns geographic coordinates to sampled algae data using the Geocode API.
- Data Cleaning & Formatting: Datasets are cleaned using MySQL, formatted with Python, and converted into JSON.
- Predictive Modeling (Future Feature): Use Linear Regression and Time Series models to predict CO2 levels and analyze algae's carbon sequestration potential.
- Satellite Imagery (Future Feature): Integrate NASA's Worldview satellite data for more accurate algae bloom tracking using computer vision.

Tools & Technologies

- Languages: Python
- Database: MySQL for data cleaning and storage
- Web Framework: Flask for web application development
- Mapping Library: Folium for creating interactive maps
- Geocoding: Geocode API to assign coordinates to sampled locations
- Future AI Integration: Machine Learning models for predictive analysis (Linear Regression, Time Series)
- Satellite Imagery: NASA's Worldview for future algae bloom tracking

Methodology

1. Data Collection: Algae density and CO2 emissions data were gathered from multiple open data sources specific to Alberta.
2. Geocoding: The Geocode API was used to assign geographical coordinates to sampled algae locations.
3. Data Cleaning and Formatting: Data was cleaned using MySQL and formatted into JSON using Python scripts.
4. Interactive Mapping: Using Folium, the application generates heatmaps that visualize algae populations and CO2 emissions.
5. Web Application: The project uses Flask to build a dynamic web interface that presents the data interactively.
6. Predictive Models (Future Work): Future enhancements include training predictive models using historical data on algae density and CO2 emissions.

Setup Instructions

1. Clone the repository:
   git clone https://github.com/yourusername/Algae-CO2-Prediction.git

2. Navigate to the project directory:
   cd Algae-CO2-Prediction

3. Install dependencies:
   Ensure you have Python 3.x installed and set up a virtual environment:
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

4. Run the Flask application:
   flask run

5. Open the web app:
   Navigate to http://127.0.0.1:5000/ in your browser.

Future Work

- Predictive Analysis: We plan to introduce predictive models (e.g., Linear Regression, Time Series) to forecast CO2 emissions and analyze the impact of algae on carbon sequestration.
- Satellite Imagery: Incorporating NASA's Worldview satellite imagery will enhance the accuracy of algae bloom tracking.
- Scalability: Expand the scope of the project to include all provinces in Canada, not just Alberta.

Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are reviewed actively.

License

This project is licensed under the MIT License.

Acknowledgments

- Open-source data providers
- NASA Worldview for satellite data
- ChatGPT for assistance in script development
