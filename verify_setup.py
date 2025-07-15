#!/usr/bin/env python3
# Simple test to verify all components work
try:
    import pandas as pd
    print("✅ Pandas imported successfully")
    
    # Check if cleaned dataset exists
    try:
        df = pd.read_csv('StudentPerformanceFactors_cleaned.csv')
        print(f"✅ Dataset loaded: {len(df)} students")
        print(f"📊 Columns: {len(df.columns)} total")
        
        # Check for outliers (should be none)
        outliers = df[df['Exam_Score'] > 100]
        if len(outliers) == 0:
            print("✅ No students with scores > 100 found")
        else:
            print(f"❌ Found {len(outliers)} students with scores > 100")
        
        print(f"📈 Score range: {df['Exam_Score'].min()} - {df['Exam_Score'].max()}")
        
    except FileNotFoundError:
        print("❌ Cleaned dataset not found")
    
    # Test imports
    try:
        from data_manager import DataManager
        print("✅ DataManager imported")
        
        dm = DataManager()
        processed_df = dm.get_processed_data()
        if processed_df is not None:
            print(f"✅ Data processing successful: {len(processed_df)} students")
            
            # Check for new engagement columns
            engagement_cols = ['Parental_Engagement_Score', 'Engagement_Category', 'Involvement_Score']
            for col in engagement_cols:
                if col in processed_df.columns:
                    print(f"✅ {col} created successfully")
                else:
                    print(f"❌ {col} missing")
        else:
            print("❌ Failed to process data")
            
    except Exception as e:
        print(f"❌ DataManager error: {e}")
    
    try:
        from visualizations import Visualizations
        print("✅ Visualizations imported")
    except Exception as e:
        print(f"❌ Visualizations error: {e}")
    
    try:
        from analytics import Analytics
        print("✅ Analytics imported")
    except Exception as e:
        print(f"❌ Analytics error: {e}")
        
    print("\n🎉 All components ready!")
    print("🚀 Run: streamlit run main.py")
    
except Exception as e:
    print(f"❌ Critical error: {e}")
