
import streamlit as st
import pandas as pd
import numpy as np
from data_manager import DataManager
from visualizations import Visualizations
from analytics import Analytics

class StudentDashboard:

    def __init__(self):
        self.data_manager = DataManager()
        self.visualizations = Visualizations()
        self.analytics = Analytics()

    def run(self):
        """Main method to run the dashboard with Streamlit UI"""
        st.set_page_config(page_title="Student Performance & Parental Engagement Dashboard", layout="wide")
        df = self.data_manager.get_processed_data()
        if df is None:
            st.error("Failed to load data. Please check your data file.")
            return
        df = self.clean_dataframe(df)
        st.title("Student Performance & Parental Engagement Analysis")
        insights = self.analytics.get_performance_insights(df)
        st.metric("Total Students", f"{insights['total_students']}")

        # Add all visualizations
        
        st.subheader("Parental Involvement Distribution")
        fig1 = self.visualizations.create_donut_chart(df, 'Parental_Involvement', 'Parental Involvement Distribution')
        st.pyplot(fig1)
        st.markdown("""
**What this shows:**  
This chart displays how many students have low, medium, or high parental involvement.  
**Why it matters:**  
Higher parental involvement is often linked to better student outcomes.  
**Takeaway:**  
Encouraging more parents to be actively involved could help more students succeed.
""")

        st.subheader("Academic Performance Distribution")
        fig2 = self.visualizations.create_histogram_chart(df, 'Performance_Category', 'Academic Performance Distribution')
        st.pyplot(fig2)
        st.markdown("""
**What this shows:**  
This chart breaks down student grades into categories (A, B, C, D, F).  
**Why it matters:**  
It helps identify how many students are excelling and how many may need extra support.  
**Takeaway:**  
Targeted interventions can be designed for students in lower performance categories.
""")

        st.subheader("Attendance Level Distribution")
        fig3 = self.visualizations.create_histogram_chart(df, 'Attendance_Category', 'Attendance Level Distribution')
        st.pyplot(fig3)
        st.markdown("""
**What this shows:**  
This chart shows how many students have poor, good, or excellent attendance.  
**Why it matters:**  
Regular attendance is a strong predictor of academic success.  
**Takeaway:**  
Improving attendance rates should be a priority for boosting performance.
""")

        st.subheader("Distribution of Exam Scores")
        fig4 = self.visualizations.create_histogram_chart(df, 'Exam_Score', 'Distribution of Exam Scores')
        st.pyplot(fig4)
        st.markdown("""
**What this shows:**  
This histogram shows the spread of exam scores across all students.  
**Why it matters:**  
It reveals whether most students are performing well or if there are many struggling.  
**Takeaway:**  
Understanding the distribution helps in designing support programs for those who need it most.
""")

        st.subheader("Correlation Heatmap")
        fig5 = self.visualizations.create_correlation_heatmap(df)
        if fig5:
            st.pyplot(fig5)
            st.markdown("""
**What this shows:**  
This heatmap shows how different factors (like attendance, study hours, parental involvement) are related to each other and to exam scores.  
**Why it matters:**  
It highlights which factors have the strongest impact on academic performance.  
**Takeaway:**  
Focus on the factors with the highest correlation to exam scores for the biggest impact.
""")

        st.subheader("Bar Chart: Scores by Parental Involvement")
        fig6 = self.visualizations.create_bar_chart_scores_by_involvement(df)
        st.pyplot(fig6)
        st.markdown("""
**What this shows:**  
This bar chart compares average exam scores for students with low, medium, and high parental involvement.  
**Why it matters:**  
It directly shows the positive impact of parental involvement on student achievement.  
**Takeaway:**  
Encouraging and supporting parental involvement can lead to higher student performance.
""")

        st.subheader("Distribution of Attendance")
        fig7 = self.visualizations.create_histogram_chart(df, 'Attendance', 'Distribution of Attendance')
        st.pyplot(fig7)
        st.markdown("""
**What this shows:**  
This chart shows the distribution of attendance rates among students.  
**Why it matters:**  
Spotting patterns in attendance can help identify students at risk.  
**Takeaway:**  
Improving attendance is a key step toward better academic outcomes.
""")

        st.subheader("Box Plot: Scores by Education")
        fig8 = self.visualizations.create_box_plot_scores_by_education(df)
        st.pyplot(fig8)
        st.markdown("""
**What this shows:**  
This plot shows how exam scores are distributed based on parental education and family income.  
**Why it matters:**  
It reveals disparities and helps identify groups that may need more support.  
**Takeaway:**  
Programs can be tailored to help students from lower-income or lower-education backgrounds.
""")

        st.subheader("Parental Involvement Heatmap")
        fig10 = self.visualizations.create_parental_involvement_heatmap(df)
        st.pyplot(fig10)
        st.markdown("""
**What this shows:**  
This heatmap shows the relationship between parental involvement and student score ranges.  
**Why it matters:**  
It visually demonstrates that higher parental involvement is linked to better scores.  
**Takeaway:**  
Parental engagement is a key area for intervention.
""")


        # Recommendations Section
        st.header("Actionable Recommendations")
        st.markdown("""
### For Parents
- **Stay Involved:** Regularly check your child’s attendance and grades. Even small actions—like asking about school or helping with homework—can make a big difference.
- **Encourage Good Study Habits:** Set aside time and a quiet space for studying.
- **Communicate with Teachers:** Stay in touch with your child’s teachers to catch issues early.

### For Educators
- **Engage Parents:** Provide regular updates and easy ways for parents to get involved.
- **Identify At-Risk Students:** Use attendance and performance data to offer early support.
- **Promote Attendance:** Recognize and reward good attendance, and work with families facing challenges.

### For Policymakers
- **Support Family Engagement Programs:** Fund initiatives that help parents get involved in their children’s education.
- **Address Barriers:** Provide resources for families facing economic or language challenges.
- **Monitor Key Metrics:** Track attendance, engagement, and performance to guide policy.

### For Students
- **Ask for Help:** If you’re struggling, reach out to teachers, counselors, or family.
- **Build Good Habits:** Attend school regularly and set goals for improvement.
- **Get Involved:** Participate in extracurriculars and seek support when needed.
""")

        # Download button(this helps users export the dataset)
        st.header("")
        st.download_button(
            label="Download Dataset",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='student_performance_export.csv',
            mime='text/csv',
        )
    def clean_dataframe(self, df):
        """Clean dataframe for analysis"""
        df_clean = df.copy()
        for col in df_clean.columns:
            if pd.api.types.is_categorical_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].astype(str)
            if df_clean[col].dtype == 'object':
                try:
                    non_null_vals = df_clean[col].dropna()
                    if len(non_null_vals) > 0:
                        pd.to_numeric(non_null_vals.iloc[0])
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                except (ValueError, TypeError):
                    df_clean[col] = df_clean[col].astype(str)
        for col in df_clean.columns:
            if df_clean[col].dtype in ['float64', 'int64']:
                df_clean[col] = df_clean[col].fillna(0)
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
        return df_clean

