import pandas as pd
from data_manager import DataManager

# Load and process data
dm = DataManager()
df = dm.get_processed_data()

print('=== PARENTAL ENGAGEMENT vs STUDENT PERFORMANCE ===')
print(f'Total Students: {len(df):,}')
print(f'Overall Average Score: {df["Exam_Score"].mean():.1f}')
print()

# Performance by involvement level
high_inv = df[df['Parental_Involvement'] == 'High']['Exam_Score'].mean()
med_inv = df[df['Parental_Involvement'] == 'Medium']['Exam_Score'].mean()
low_inv = df[df['Parental_Involvement'] == 'Low']['Exam_Score'].mean()

print('PERFORMANCE BY PARENTAL INVOLVEMENT:')
print(f'High Involvement: {high_inv:.1f} points')
print(f'Medium Involvement: {med_inv:.1f} points') 
print(f'Low Involvement: {low_inv:.1f} points')
print()
print(f'PERFORMANCE GAP: {high_inv - low_inv:.1f} points')
print()

# Correlation
involvement_map = {'Low': 1, 'Medium': 2, 'High': 3}
df['Involvement_Numeric'] = df['Parental_Involvement'].map(involvement_map)
correlation = df['Involvement_Numeric'].corr(df['Exam_Score'])
print(f'CORRELATION: {correlation:.3f}')

# High performers by engagement
high_perf_high = (df[(df['Exam_Score'] > 70) & (df['Parental_Involvement'] == 'High')].shape[0] / df[df['Parental_Involvement'] == 'High'].shape[0]) * 100
high_perf_low = (df[(df['Exam_Score'] > 70) & (df['Parental_Involvement'] == 'Low')].shape[0] / df[df['Parental_Involvement'] == 'Low'].shape[0]) * 100

print(f'High Performers (>70) with High Involvement: {high_perf_high:.1f}%')
print(f'High Performers (>70) with Low Involvement: {high_perf_low:.1f}%')
print()

# Answer the main question
if correlation > 0.3:
    strength = "STRONG"
elif correlation > 0.1:
    strength = "MODERATE"
else:
    strength = "WEAK"

print('=== ANSWER TO YOUR QUESTION ===')
print(f'YES! There is a {strength} positive correlation ({correlation:.3f})')
print(f'Students with highly engaged parents score {high_inv - low_inv:.1f} points higher')
print(f'{high_perf_high:.1f}% of high-involvement students are high performers')
print(f'vs {high_perf_low:.1f}% of low-involvement students')
