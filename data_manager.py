import pandas as pd
import streamlit as st

class DataManager:
    
    def __init__(self, filename="student_performance_cleaned.csv"):
        self.filename = filename
        self.df = None
    
    @staticmethod
    @st.cache_data # load the csv data # Cache the data loading function to improve performance 
    def load_data(filename):
        """Loads data from a local CSV file."""
        try:
            df = pd.read_csv(filename)
            return df
        except FileNotFoundError:
            st.error(f"Error: The dataset '{filename}' was not found.")
            return None

    def categorize_data(self, df):
        """Create categories for better visualization"""
        df['Performance_Category'] = pd.cut(df['Exam_Score'], 
                                        bins=[0, 60, 70, 80, 90, 100], 
                                        labels=['F (0-59)', 'D (60-69)', 'C (70-79)', 'B (80-89)', 'A (90-100)'])
        df['Attendance_Category'] = pd.cut(df['Attendance'], 
                                        bins=[0, 70, 85, 100], 
                                        labels=['Poor (≤70%)', 'Good (71-85%)', 'Excellent (>85%)'])
        df['Study_Hours_Category'] = pd.cut(df['Hours_Studied'], 
                                        bins=[0, 10, 20, 50], 
                                        labels=['Low (≤10h)', 'Medium (11-20h)', 'High (>20h)'])
        df = self.create_parental_engagement_score(df)
        return df
    
    def create_parental_engagement_score(self, df):
        """Map involvement, education, and income to numeric columns only"""
        involvement_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        df['Involvement_Score'] = df['Parental_Involvement'].map(involvement_scores)

        education_scores = {'High School': 1, 'College': 2, 'Postgraduate': 3}
        df['Education_Score'] = df['Parental_Education_Level'].map(education_scores)

        income_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        df['Income_Score'] = df['Family_Income'].map(income_scores)

        categorical_columns = ['Performance_Category', 'Attendance_Category', 'Study_Hours_Category']
        for col in categorical_columns:
            if col in df.columns and df[col].isna().any():
                df[col] = df[col].cat.add_categories(['Unknown']).fillna('Unknown')

        return df
    
    def get_processed_data(self):
        if self.df is None:
            self.df = self.load_data(self.filename)
            if self.df is not None:
                self.df = self.categorize_data(self.df)
        return self.df




