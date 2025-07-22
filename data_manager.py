import pandas as pd
import streamlit as st

class DataManager:
    
    def __init__(self):
        # IMPORTANT: This is a public URL for the dataset
        self.data_url = "https://raw.githubusercontent.com/Poojanarkhede22/Student_Performance_data/master/StudentsPerformance.csv"
        self.df = None
    
    @staticmethod
    @st.cache_data # Cache the data loading function to improve performance
    def load_data(url):
        """Loads data from a URL and caches it."""
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            st.error(f"Error loading data from URL: {e}")
            return None

    def categorize_data(self, df):
        """Create categories for better visualization"""
        # Calculate average score
        df['Average_Score'] = df[['math score', 'reading score', 'writing score']].mean(axis=1)

        df['Performance_Category'] = pd.cut(df['Average_Score'], 
                                        bins=[0, 60, 70, 80, 90, 100], 
                                        labels=['F (0-59)', 'D (60-69)', 'C (70-79)', 'B (80-89)', 'A (90-100)'])
        df['Attendance_Category'] = pd.cut(df['Attendance'], 
                                        bins=[0, 70, 85, 100], 
                                        labels=['Poor (≤70%)', 'Good (71-85%)', 'Excellent (>85%)'])
        df['Study_Hours_Category'] = pd.cut(df['Hours_Studied'], 
                                        bins=[0, 10, 20, 50], 
                                        labels=['Low (≤10h)', 'Medium (11-20h)', 'High (>20h)'])
        # Create Parental Engagement Score
        df = self.create_parental_engagement_score(df)
        # Optionally, create a histogram column for Attendance vs Exam Score
        # This is just a placeholder for your dashboard to use create_histogram_chart
        return df
    
    def create_parental_engagement_score(self, df):
        """Create a comprehensive Parental Engagement Score combining multiple indicators"""
        
        # Map parental involvement to numeric values
        involvement_scores = {'some high school': 1, 'high school': 2, 'some college': 3, "associate's degree": 4, "bachelor's degree": 5, "master's degree": 6}
        df['Involvement_Score'] = df['parental level of education'].map(involvement_scores)
        
        # Map parental education to numeric values
        education_scores = {'some high school': 1, 'high school': 2, 'some college': 3, "associate's degree": 4, "bachelor's degree": 5, "master's degree": 6}
        df['Education_Score'] = df['parental level of education'].map(education_scores)
        
        # Map family income to numeric values (assuming 'lunch' is a proxy for income)
        income_scores = {'standard': 2, 'free/reduced': 1}
        df['Income_Score'] = df['lunch'].map(income_scores)
        
        # Calculate weighted engagement score (involvement weighted more heavily)
        df['Parental_Engagement_Score'] = (
            df['Involvement_Score'] * 0.5 +  # 50% weight for direct involvement
            df['Education_Score'] * 0.3 +    # 30% weight for education level
            df['Income_Score'] * 0.2          # 20% weight for family income
        )
        
        # Create engagement categories (handle NaN values first)
        df['Engagement_Category'] = pd.cut(df['Parental_Engagement_Score'], 
                                         bins=[0, 2, 4, 6], 
                                         labels=['Low Engagement', 'Medium Engagement', 'High Engagement'])
        
        # Handle any NaN values in categorical columns
        categorical_columns = ['Performance_Category', 'Attendance_Category', 'Study_Hours_Category', 'Engagement_Category']
        for col in categorical_columns:
            if col in df.columns:
                # Add 'Unknown' as a category if there are NaN values
                if df[col].isna().any():
                    df[col] = df[col].cat.add_categories(['Unknown']).fillna('Unknown')
        
        return df
    
    def get_processed_data(self):
        if self.df is None:
            self.df = self.load_data(self.data_url)
            if self.df is not None:
                self.df = self.categorize_data(self.df)
        return self.df




