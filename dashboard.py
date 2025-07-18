
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

    # ...existing code...
    def run(self):
        """Main method to run the dashboard with Streamlit UI"""
        st.set_page_config(page_title="Student Performance & Parental Engagement Dashboard", layout="wide")
        df = self.data_manager.get_processed_data()
        if df is None:
            st.error("Failed to load data. Please check your data file.")
            return
        df = self.clean_dataframe(df)
        st.title("Student Performance & Parental Engagement Analysis")
        st.write(f"Total Records: {len(df)}")
        insights = self.analytics.get_performance_insights(df)
        st.metric("Total Students", f"{insights['total_students']}")
        st.metric("Average Exam Score", f"{insights['avg_score']:.1f}")
        st.metric("Average Attendance", f"{insights['avg_attendance']:.1f}%")
        st.metric("High Performers (>70)", f"{insights['high_performers_pct']:.1f}%")

        # Add all visualizations
        st.subheader("Parental Involvement Distribution")
        fig1 = self.visualizations.create_donut_chart(df, 'Parental_Involvement', 'Parental Involvement Distribution')
        st.pyplot(fig1)

        st.subheader("Academic Performance Distribution")
        fig2 = self.visualizations.create_histogram_chart(df, 'Performance_Category', 'Academic Performance Distribution')
        st.pyplot(fig2)

        st.subheader("Attendance Level Distribution")
        fig3 = self.visualizations.create_histogram_chart(df, 'Attendance_Category', 'Attendance Level Distribution')
        st.pyplot(fig3)

        st.subheader("Distribution of Exam Scores")
        fig4 = self.visualizations.create_histogram_chart(df, 'Exam_Score', 'Distribution of Exam Scores')
        st.pyplot(fig4)

        st.subheader("Correlation Heatmap")
        fig5 = self.visualizations.create_correlation_heatmap(df)
        if fig5:
            st.pyplot(fig5)

        st.subheader("Bar Chart: Scores by Parental Involvement")
        fig6 = self.visualizations.create_bar_chart_scores_by_involvement(df)
        st.pyplot(fig6)

        st.subheader("Scatter: Attendance vs Exam Scores")
        fig7 = self.visualizations.create_scatter_attendance_vs_scores(df)
        st.pyplot(fig7)

        st.subheader("Box Plot: Scores by Education")
        fig8 = self.visualizations.create_box_plot_scores_by_education(df)
        st.pyplot(fig8)

        st.subheader("Parental Involvement Analysis")
        fig9 = self.visualizations.create_parental_involvement_analysis(df)
        st.pyplot(fig9)

        st.subheader("Parental Involvement Heatmap")
        fig10 = self.visualizations.create_parental_involvement_heatmap(df)
        st.pyplot(fig10)

        st.subheader("Engagement Score Scatter")
        fig11 = self.visualizations.create_engagement_score_scatter(df)
        st.pyplot(fig11)

        st.subheader("Engagement by Education Level")
        fig12 = self.visualizations.create_engagement_by_education_level(df)
        st.pyplot(fig12)

        st.subheader("Engagement Correlation Heatmap")
        fig14 = self.visualizations.create_engagement_correlation_heatmap(df)
        st.pyplot(fig14)

        st.subheader("Engagement Score Distribution")
        fig15 = self.visualizations.create_histogram_chart(df, 'Parental_Engagement_Score', 'Engagement Score Distribution')
        st.pyplot(fig15)

        # Recommendations Section
        st.header("Actionable Recommendations")
        recommendations = self.analytics.get_engagement_recommendations(df)
        if recommendations:
            for rec in recommendations:
                st.markdown(f"**{rec['priority']} Priority: {rec['area']}**")
                st.write(rec['recommendation'])
                st.write(f"_Expected Impact:_ {rec['expected_impact']}")
                st.write("**Specific Actions:**")
                for action in rec['specific_actions']:
                    st.write(f"- {action}")
                st.markdown("---")
        else:
            st.info("No specific recommendations generated for this dataset.")

        # ...existing code...
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
