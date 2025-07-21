# EngageMetrics

**EngageMetrics** is an interactive dashboard and analytics suite built with Python (Pandas, Matplotlib, NumPy, Streamlit, and OOP principles). It provides deep analysis and visualizations of the public dataset **StudentPerformanceFactors**, aiming to uncover the major factors that contribute to students' academic success—especially the role of parental involvement.

## Project Purpose

The dashboard is designed to help educators, policymakers, and parents understand:
- What factors most strongly influence student academic performance.
- Whether and how parental engagement impacts student outcomes.
- What actionable steps can be taken to improve student performance, based on data-driven insights.

## Dataset

The project uses the `StudentPerformanceFactors` dataset, which includes features such as:
- Hours Studied
- Attendance
- Parental Involvement
- Access to Resources
- Extracurricular Activities
- Sleep Hours
- Previous Scores
- Motivation Level
- Internet Access
- Tutoring Sessions
- Family Income
- Teacher Quality
- School Type
- Peer Influence
- Physical Activity
- Learning Disabilities
- Parental Education Level
- Distance from Home
- Gender
- Exam Score

## Features

- **Data Cleaning & Management:**  
  The `DataManager` class loads, cleans, and categorizes the data, creating new features such as performance categories, attendance categories, and a composite Parental Engagement Score.

- **Analytics:**  
  The `Analytics` class provides:
  - Correlation analysis between parental involvement and exam scores.
  - Insights into high-performing students and the impact of various factors.
  - Actionable recommendations for improving student outcomes.

- **Visualizations:**  
  The `Visualizations` class generates:
  - Donut charts for parental involvement and score distributions.
  - Histograms and bar charts for performance, attendance, and engagement.
  - Correlation heatmaps.
  - Scatter plots and box plots for deeper analysis by demographic factors.

- **Interactive Dashboard:**  
  The `StudentDashboard` class (run via Streamlit) brings everything together, displaying metrics, visualizations, and recommendations in an easy-to-use web interface.

## How to Run the application\dashboard

1. **Install Requirements:**  
   Make sure you have Python 3.7+ and install the required packages:
   ```
   pip install pandas numpy matplotlib streamlit
   ```

2. **Prepare the Dataset:**  
   Place the cleaned dataset file (`StudentPerformanceFactors_cleaned.csv`) in the project directory.  
   (You can use the notebook to download and clean the original dataset, or just download it from the dashhboard where you can find a button that helps download the cleaned csv file used for this analysis.)

3. **Start the Dashboard:**  
   Run the following command in your terminal:
   ```
   streamlit run main.py
   ```
   This will launch the dashboard in your browser.

## File Structure

- `main.py` — Entry point; launches the Streamlit dashboard.
- `dashboard.py` — Dashboard logic and UI.
- `data_manager.py` — Data loading, cleaning, and feature engineering.
- `analytics.py` — Analytical computations and recommendations.
- `visualizations.py` — All plotting and visualization functions.
- `EngageMetrics.ipynb` — Jupyter notebook for data exploration(DE) and cleaning.
- `README.md` — Project documentation.

## Example Insights

- Students with high parental involvement score significantly higher on average.
- Excellent attendance and more study hours are common traits among top performers.
- Actionable recommendations are generated, such as improving attendance, supporting study skills, and targeting comprehensive academic support for low-performing groups.

## License

This project is for educational and research purposes.