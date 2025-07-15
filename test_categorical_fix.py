#!/usr/bin/env python3
# Test the categorical fix
import pandas as pd
import streamlit as st
from data_manager import DataManager

def test_categorical_fix():
    print("🧪 Testing categorical data handling fix...")
    
    try:
        # Initialize data manager
        dm = DataManager()
        df = dm.get_processed_data()
        
        if df is not None:
            print(f"✅ Data loaded: {len(df)} students")
            
            # Check categorical columns
            categorical_cols = ['Performance_Category', 'Attendance_Category', 'Study_Hours_Category', 'Engagement_Category']
            
            for col in categorical_cols:
                if col in df.columns:
                    print(f"📊 {col}:")
                    print(f"   Type: {df[col].dtype}")
                    print(f"   Categories: {df[col].cat.categories.tolist() if pd.api.types.is_categorical_dtype(df[col]) else 'Not categorical'}")
                    print(f"   NaN count: {df[col].isna().sum()}")
                    print(f"   Value counts: {df[col].value_counts()}")
                    print()
            
            # Test dashboard cleaning
            print("🧹 Testing dashboard data cleaning...")
            from dashboard import StudentDashboard
            dashboard = StudentDashboard()
            
            clean_df = dashboard.clean_dataframe_for_streamlit(df)
            print(f"✅ Data cleaning successful: {len(clean_df)} students")
            
            # Check if categorical columns are now strings
            for col in categorical_cols:
                if col in clean_df.columns:
                    print(f"📝 {col}: {clean_df[col].dtype} - Sample: {clean_df[col].iloc[0]}")
            
            print("\n🎉 Categorical fix test completed!")
            
        else:
            print("❌ Failed to load data")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_categorical_fix()
