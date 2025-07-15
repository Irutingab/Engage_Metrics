# Quick test script for the updated dashboard
import pandas as pd
from dashboard import StudentDashboard

def test_dashboard():
    print("🧪 Testing updated dashboard with parental engagement features...")
    
    try:
        # Test data loading and processing
        dashboard = StudentDashboard()
        df = dashboard.data_manager.get_processed_data()
        
        if df is not None:
            print(f"✅ Data loaded successfully: {len(df)} students")
            print(f"📊 Columns: {list(df.columns)}")
            
            # Check for new engagement columns
            engagement_cols = ['Parental_Engagement_Score', 'Engagement_Category', 'Involvement_Score']
            for col in engagement_cols:
                if col in df.columns:
                    print(f"✅ {col} column created successfully")
                else:
                    print(f"❌ {col} column missing")
            
            # Test categorical data cleaning
            clean_df = dashboard.clean_dataframe_for_streamlit(df)
            print(f"✅ Data cleaning completed: {len(clean_df)} students")
            
            # Check engagement score statistics
            if 'Parental_Engagement_Score' in clean_df.columns:
                print(f"📈 Engagement Score Stats:")
                print(f"   Mean: {clean_df['Parental_Engagement_Score'].mean():.2f}")
                print(f"   Min: {clean_df['Parental_Engagement_Score'].min():.2f}")
                print(f"   Max: {clean_df['Parental_Engagement_Score'].max():.2f}")
            
            print("\n🎉 Dashboard test completed successfully!")
            print("🚀 Ready to run: streamlit run main.py")
            
        else:
            print("❌ Failed to load data")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_dashboard()
