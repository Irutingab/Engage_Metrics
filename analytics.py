import pandas as pd
import numpy as np

class Analytics:
    @staticmethod
    def analyze_parental_involvement_correlation(df):
        """Analyze correlation between parental involvement and student performance"""
        
        # Convert parental involvement to numeric for correlation
        involvement_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        df_analysis = df.copy()
        df_analysis['Parental_Involvement_Numeric'] = df_analysis['Parental_Involvement'].map(involvement_mapping)
        
        # Calculate correlation coefficient using pandas
        correlation = df_analysis['Parental_Involvement_Numeric'].corr(df_analysis['Exam_Score'])
        
        # Simple significance estimation based on correlation strength and sample size
        n = len(df_analysis)
        if n > 30:  # Large sample
            p_value = 0.001 if abs(correlation) > 0.3 else 0.05 if abs(correlation) > 0.2 else 0.1
        else:  # Small sample 
            p_value = 0.01 if abs(correlation) > 0.5 else 0.1
        
        return correlation, p_value
    
    @staticmethod
    def get_performance_insights(df):
        """Get key performance insights and statistics"""
        insights = {}
        
        # Basic statistics
        insights['total_students'] = len(df)
        insights['avg_score'] = df['Exam_Score'].mean()
        insights['avg_attendance'] = df['Attendance'].mean()
        insights['high_performers_pct'] = (df['Exam_Score'] >= 70).mean() * 100
        insights['high_involvement_pct'] = (df['Parental_Involvement'] == 'High').mean() * 100
        
        # Parental involvement impact
        high_involvement = df[df['Parental_Involvement'] == 'High']['Exam_Score'].mean()
        low_involvement = df[df['Parental_Involvement'] == 'Low']['Exam_Score'].mean()
        
        if not pd.isna(high_involvement) and not pd.isna(low_involvement):
            insights['involvement_impact'] = high_involvement - low_involvement
            insights['high_involvement_mean'] = high_involvement
            insights['low_involvement_mean'] = low_involvement
        
        # High performer traits
        high_performers = df[df['Exam_Score'] >= 70]
        if len(high_performers) > 0:
            insights['high_perf_traits'] = {
                'High Parental Involvement': (high_performers['Parental_Involvement'] == 'High').mean() * 100,
                'Excellent Attendance': (high_performers['Attendance'] > 85).mean() * 100,
                'High Study Hours': (high_performers['Hours_Studied'] > 20).mean() * 100
            }
        return insights
    
    @staticmethod
    def get_correlation_insights(df):
        """Get correlation insights for numeric features"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if 'Exam_Score' not in numeric_cols:
            return None
            
        correlations = df[numeric_cols].corr()['Exam_Score'].abs().sort_values(ascending=False)
        
        # Get top factors (excluding Exam_Score itself)
        top_factors = correlations.drop('Exam_Score').head(5)
        
        correlation_data = []
        for factor, corr in top_factors.items():
            strength = "Strong" if corr > 0.3 else "Moderate" if corr > 0.1 else "Weak"
            correlation_data.append({
                'factor': factor,
                'correlation': corr,
                'strength': strength
            })
        
        return correlation_data
    
    @staticmethod
    def create_correlation_heatmap(df):
        """Create a correlation heatmap including Parental_Involvement as numeric."""
        df_corr = df.copy()
        # Map Parental_Involvement to numeric for correlation
        involvement_map = {'Low': 1, 'Medium': 2, 'High': 3}
        if 'Parental_Involvement' in df_corr.columns:
            df_corr['Parental_Involvement_Num'] = df_corr['Parental_Involvement'].map(involvement_map)
        # Select only numeric columns for correlation
        numeric_cols = df_corr.select_dtypes(include=['number']).columns.tolist()
        # Ensure Parental_Involvement_Num is included
        if 'Parental_Involvement_Num' in df_corr.columns and 'Parental_Involvement_Num' not in numeric_cols:
            numeric_cols.append('Parental_Involvement_Num')
        corr = df_corr[numeric_cols].corr()

        import matplotlib.pyplot as plt
        import seaborn as sns
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
        ax.set_title("Correlation Heatmap (including Parental Involvement)")
        return fig
    
    @staticmethod
    def get_engagement_insights(df):
        """Get comprehensive parental engagement insights"""
        engagement_insights = {}
        
        # Engagement score statistics
        engagement_insights['avg_engagement_score'] = df['Parental_Engagement_Score'].mean()
        engagement_insights['median_engagement_score'] = df['Parental_Engagement_Score'].median()
        engagement_insights['std_engagement_score'] = df['Parental_Engagement_Score'].std()
        
        # Distribution by engagement categories
        engagement_dist = df['Engagement_Category'].value_counts(normalize=True) * 100
        engagement_insights['engagement_distribution'] = engagement_dist.to_dict()
        
        # Performance by engagement level
        engagement_performance = df.groupby('Engagement_Category')['Exam_Score'].agg(['mean', 'count', 'std']).round(2)
        engagement_insights['performance_by_engagement'] = engagement_performance.to_dict()
        
        # Education level impact
        education_performance = df.groupby('Parental_Education_Level')['Exam_Score'].mean().round(2)
        engagement_insights['performance_by_education'] = education_performance.to_dict()
        
        # Income level impact
        income_performance = df.groupby('Family_Income')['Exam_Score'].mean().round(2)
        engagement_insights['performance_by_income'] = income_performance.to_dict()
        
        # Correlation analysis
        engagement_correlations = df[['Parental_Engagement_Score', 'Involvement_Score', 
                                    'Education_Score', 'Income_Score', 'Exam_Score']].corr()['Exam_Score'].round(3)
        engagement_insights['engagement_correlations'] = engagement_correlations.to_dict()
        
        # Top factors for high performers
        high_performers = df[df['Exam_Score'] > 70]
        if len(high_performers) > 0:
            engagement_insights['high_performer_engagement_traits'] = {
                'avg_engagement_score': high_performers['Parental_Engagement_Score'].mean(),
                'high_involvement_pct': (high_performers['Parental_Involvement'] == 'High').mean() * 100,
                'postgraduate_parents_pct': (high_performers['Parental_Education_Level'] == 'Postgraduate').mean() * 100,
                'high_income_pct': (high_performers['Family_Income'] == 'High').mean() * 100
            }
        
        return engagement_insights
    
    @staticmethod
    def analyze_engagement_factors_impact(df):
        """Analyze the impact of different engagement factors on performance"""
        impact_analysis = {}
        
        # Individual factor analysis
        factors = {
            'Parental_Involvement': {'Low': 1, 'Medium': 2, 'High': 3},
            'Parental_Education_Level': {'High School': 1, 'College': 2, 'Postgraduate': 3},
            'Family_Income': {'Low': 1, 'Medium': 2, 'High': 3}
        }
        
        for factor, mapping in factors.items():
            df_temp = df.copy()
            df_temp[f'{factor}_Numeric'] = df_temp[factor].map(mapping)
            
            # Calculate correlation with exam scores
            correlation = df_temp[f'{factor}_Numeric'].corr(df_temp['Exam_Score'])
            
            # Calculate mean scores by category
            mean_scores = df.groupby(factor)['Exam_Score'].mean().round(2)
            
            # Calculate effect size (difference between highest and lowest)
            effect_size = mean_scores.max() - mean_scores.min()
            
            impact_analysis[factor] = {
                'correlation': correlation,
                'mean_scores_by_category': mean_scores.to_dict(),
                'effect_size': effect_size
            }
        
        return impact_analysis
    
    @staticmethod
    def get_engagement_recommendations(df):
        """Generate comprehensive actionable recommendations based on engagement analysis"""
        recommendations = []
        
        # Analyze current state
        low_engagement_pct = (df['Engagement_Category'] == 'Low Engagement').mean() * 100
        high_involvement_performance = df[df['Parental_Involvement'] == 'High']['Exam_Score'].mean()
        low_involvement_performance = df[df['Parental_Involvement'] == 'Low']['Exam_Score'].mean()
        avg_score = df['Exam_Score'].mean()
        
        # 1. PARENTAL ENGAGEMENT RECOMMENDATIONS
        if low_engagement_pct > 30:
            recommendations.append({
                'priority': 'High',
                'area': 'Parent Engagement Programs',
                'recommendation': f'Implement targeted parent engagement programs - {low_engagement_pct:.1f}% of families show low engagement',
                'expected_impact': 'Could improve average scores by 3-5 points',
                'specific_actions': [
                    'Monthly parent-teacher conferences',
                    'Home visit programs for low-engagement families',
                    'Parent education workshops on supporting student learning',
                    'Digital communication platforms for regular updates'
                ]
            })
        
        if high_involvement_performance - low_involvement_performance > 3:
            recommendations.append({
                'priority': 'High',
                'area': 'Family Communication Enhancement',
                'recommendation': f'High involvement parents see {high_involvement_performance - low_involvement_performance:.1f} point advantage - expand communication channels',
                'expected_impact': 'Could reduce achievement gap by 20-30%',
                'specific_actions': [
                    'Weekly progress reports via SMS/email',
                    'Parent portal for real-time grade tracking',
                    'Bilingual communication for diverse families',
                    'Regular celebration of student achievements'
                ]
            })
        
        # 2. EDUCATION LEVEL BASED RECOMMENDATIONS
        education_scores = df.groupby('Parental_Education_Level')['Exam_Score'].mean()
        if 'Postgraduate' in education_scores.index and 'High School' in education_scores.index:
            education_gap = education_scores['Postgraduate'] - education_scores['High School']
            if education_gap > 5:
                recommendations.append({
                    'priority': 'High',
                    'area': 'Educational Equity Support',
                    'recommendation': f'Address {education_gap:.1f}-point achievement gap between education levels',
                    'expected_impact': 'Could improve scores for 40% of students by 4-6 points',
                    'specific_actions': [
                        'Tutoring programs for students with less-educated parents',
                        'Academic enrichment workshops for parents',
                        'Homework help centers with trained volunteers',
                        'College preparation support regardless of parent background'
                    ]
                })
        
        # 3. INCOME-BASED RECOMMENDATIONS
        income_scores = df.groupby('Family_Income')['Exam_Score'].mean()
        if 'High' in income_scores.index and 'Low' in income_scores.index:
            income_gap = income_scores['High'] - income_scores['Low']
            if income_gap > 3:
                recommendations.append({
                    'priority': 'High',
                    'area': 'Resource Equity Initiative',
                    'recommendation': f'Bridge {income_gap:.1f}-point gap between income levels through resource support',
                    'expected_impact': 'Could improve equity and boost overall performance by 3-4 points',
                    'specific_actions': [
                        'Free technology lending program (laptops, tablets)',
                        'Subsidized internet access for low-income families',
                        'Free school supplies and educational materials',
                        'Breakfast and lunch programs to ensure basic needs are met'
                    ]
                })
        
        # 4. ATTENDANCE-BASED RECOMMENDATIONS
        low_attendance_students = df[df['Attendance'] < 85]
        if len(low_attendance_students) > 0:
            low_attendance_pct = (len(low_attendance_students) / len(df)) * 100
            avg_score_low_attendance = low_attendance_students['Exam_Score'].mean()
            avg_score_high_attendance = df[df['Attendance'] >= 85]['Exam_Score'].mean()
            attendance_gap = avg_score_high_attendance - avg_score_low_attendance
            
            recommendations.append({
                'priority': 'Medium',
                'area': 'Attendance Improvement',
                'recommendation': f'{low_attendance_pct:.1f}% of students have attendance <85% - {attendance_gap:.1f} point performance gap',
                'expected_impact': 'Could improve overall performance by 2-3 points',
                'specific_actions': [
                    'Early intervention for attendance issues',
                    'Transportation support for struggling families',
                    'Flexible scheduling for working student families',
                    'Attendance rewards and recognition programs'
                ]
            })
        
        # 5. STUDY HABITS RECOMMENDATIONS
        high_study_hours = df[df['Hours_Studied'] > 20]['Exam_Score'].mean()
        low_study_hours = df[df['Hours_Studied'] <= 10]['Exam_Score'].mean()
        study_gap = high_study_hours - low_study_hours
        
        if study_gap > 4:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Study Skills Development',
                'recommendation': f'Students studying >20hrs score {study_gap:.1f} points higher - enhance study skills training',
                'expected_impact': 'Could improve time management and academic performance',
                'specific_actions': [
                    'Study skills workshops for students and parents',
                    'Time management training sessions',
                    'Study group facilitation programs',
                    'Academic coaching for struggling students'
                ]
            })
        
        # 6. MOTIVATION-BASED RECOMMENDATIONS
        high_motivation = df[df['Motivation_Level'] == 'High']['Exam_Score'].mean()
        low_motivation = df[df['Motivation_Level'] == 'Low']['Exam_Score'].mean()
        motivation_gap = high_motivation - low_motivation
        
        if motivation_gap > 5:
            recommendations.append({
                'priority': 'Medium',
                'area': 'Student Motivation Enhancement',
                'recommendation': f'High motivation students outperform by {motivation_gap:.1f} points - boost student engagement',
                'expected_impact': 'Could increase intrinsic motivation and long-term success',
                'specific_actions': [
                    'Career exploration and mentorship programs',
                    'Goal-setting workshops with students',
                    'Peer tutoring and support networks',
                    'Recognition programs for academic improvement'
                ]
            })
        
        # 7. TECHNOLOGY ACCESS RECOMMENDATIONS
        internet_yes = df[df['Internet_Access'] == 'Yes']['Exam_Score'].mean()
        internet_no = df[df['Internet_Access'] == 'No']['Exam_Score'].mean()
        internet_gap = internet_yes - internet_no
        
        if internet_gap > 2:
            no_internet_pct = (df['Internet_Access'] == 'No').mean() * 100
            recommendations.append({
                'priority': 'Medium',
                'area': 'Digital Equity',
                'recommendation': f'{no_internet_pct:.1f}% lack internet access - {internet_gap:.1f} point performance gap',
                'expected_impact': 'Could modernize learning and improve digital literacy',
                'specific_actions': [
                    'Partner with ISPs for discounted internet access',
                    'Mobile hotspot lending programs',
                    'Computer labs with extended hours',
                    'Digital literacy training for families'
                ]
            })
        
        # 8. OVERALL PERFORMANCE RECOMMENDATIONS
        if avg_score < 70:
            recommendations.append({
                'priority': 'High',
                'area': 'Comprehensive Academic Support',
                'recommendation': f'Overall average score is {avg_score:.1f} - implement multi-faceted improvement strategy',
                'expected_impact': 'Could raise overall performance to target levels',
                'specific_actions': [
                    'Comprehensive needs assessment for each student',
                    'Individualized learning plans',
                    'Extended learning time programs',
                    'Multi-tiered intervention system'
                ]
            })
        
        return recommendations
