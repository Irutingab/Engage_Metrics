import pandas as pd
import streamlit as st

class DataManager:
    
    def __init__(self, filename="StudentPerformanceFactors_cleaned.csv"):
        self.filename = filename
        self.df = None
    
    @st.cache_data # Cache the data loading function to improve performance
    def load_data(_self):
        try:
            df = pd.read_csv(_self.filename)
            return df
        except FileNotFoundError:
            st.error(f"Dataset '{_self.filename}' not found.")
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
        
        # Create Parental Engagement Score
        df = self.create_parental_engagement_score(df)
        return df
    
    def create_parental_engagement_score(self, df):
        """Create a comprehensive Parental Engagement Score combining multiple indicators"""
        
        # Map parental involvement to numeric values
        involvement_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        df['Involvement_Score'] = df['Parental_Involvement'].map(involvement_scores)
        
        # Map parental education to numeric values
        education_scores = {'High School': 1, 'College': 2, 'Postgraduate': 3}
        df['Education_Score'] = df['Parental_Education_Level'].map(education_scores)
        
        # Map family income to numeric values
        income_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        df['Income_Score'] = df['Family_Income'].map(income_scores)
        
        # Calculate weighted engagement score (involvement weighted more heavily)
        df['Parental_Engagement_Score'] = (
            df['Involvement_Score'] * 0.5 +  # 50% weight for direct involvement
            df['Education_Score'] * 0.3 +    # 30% weight for education level
            df['Income_Score'] * 0.2          # 20% weight for family income
        )
        
        # Create engagement categories (handle NaN values first)
        df['Engagement_Category'] = pd.cut(df['Parental_Engagement_Score'], 
                                         bins=[0, 1.5, 2.5, 3], 
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
            self.df = self.load_data()
            if self.df is not None:
                self.df = self.categorize_data(self.df)
        return self.df


