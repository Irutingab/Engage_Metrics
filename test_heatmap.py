# Test script for the new parental involvement heatmap
import pandas as pd
import matplotlib.pyplot as plt
from visualizations import Visualizations

# Load the cleaned dataset
try:
    df = pd.read_csv('StudentPerformanceFactors_cleaned.csv')
    print("✅ Cleaned dataset loaded successfully")
    print(f"Dataset shape: {df.shape}")
    
    # Test the new heatmap
    print("\n🔍 Testing parental involvement heatmap...")
    vis = Visualizations()
    fig = vis.create_parental_involvement_heatmap(df)
    
    if fig:
        print("✅ Heatmap created successfully!")
        print("📊 Displaying the heatmap...")
        plt.show()
        
        # Show some sample data
        print("\n📈 Sample involvement vs score data:")
        sample_data = df.groupby('Parental_Involvement')['Exam_Score'].agg(['mean', 'count', 'min', 'max']).round(2)
        print(sample_data)
        
    else:
        print("❌ Failed to create heatmap")
        
except FileNotFoundError:
    print("❌ Cleaned dataset not found. Using original dataset...")
    try:
        df = pd.read_csv('StudentPerformanceFactors.csv')
        # Remove the outlier student
        df = df[df['Exam_Score'] <= 100]
        print(f"✅ Original dataset loaded and cleaned. Shape: {df.shape}")
        
        vis = Visualizations()
        fig = vis.create_parental_involvement_heatmap(df)
        
        if fig:
            print("✅ Heatmap created successfully!")
            plt.show()
        else:
            print("❌ Failed to create heatmap")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        
except Exception as e:
    print(f"❌ Error: {e}")
