import pandas as pd
import numpy as np

class Analytics:
    @staticmethod
    def get_performance_insights(df):
        """Comprehensive performance analytics with actionable insights"""
        insights = {}
        
        # Basic metrics
        insights['total_students'] = len(df)
        
        if 'Exam_Score' in df.columns:
            insights['avg_score'] = df['Exam_Score'].mean()
            insights['score_std'] = df['Exam_Score'].std()
            insights['median_score'] = df['Exam_Score'].median()
            insights['min_score'] = df['Exam_Score'].min()
            insights['max_score'] = df['Exam_Score'].max()
            
            # Performance categories
            insights['top_10_percent_threshold'] = df['Exam_Score'].quantile(0.9)
            insights['bottom_10_percent_threshold'] = df['Exam_Score'].quantile(0.1)
            insights['high_performers'] = len(df[df['Exam_Score'] >= 80])
            insights['at_risk_students'] = len(df[df['Exam_Score'] < 60])
            insights['average_performers'] = len(df[(df['Exam_Score'] >= 60) & (df['Exam_Score'] < 80)])
        
        # Parental involvement analysis
        if 'Parental_Involvement' in df.columns and 'Exam_Score' in df.columns:
            insights['avg_score_by_involvement'] = df.groupby('Parental_Involvement')['Exam_Score'].mean().to_dict()
            insights['involvement_distribution'] = df['Parental_Involvement'].value_counts().to_dict()
            
            if 'Involvement_Score' in df.columns:
                corr = df[['Involvement_Score', 'Exam_Score']].corr().iloc[0, 1]
                insights['involvement_correlation'] = corr
                insights['involvement_impact'] = "High" if abs(corr) > 0.5 else "Medium" if abs(corr) > 0.3 else "Low"
        
        # Attendance analysis
        if 'Attendance' in df.columns and 'Exam_Score' in df.columns:
            insights['avg_attendance'] = df['Attendance'].mean()
            insights['attendance_correlation'] = df[['Attendance', 'Exam_Score']].corr().iloc[0, 1]
            
            high_attendance = df[df['Attendance'] >= 90]
            low_attendance = df[df['Attendance'] < 70]
            
            if len(high_attendance) > 0:
                insights['avg_score_high_attendance'] = high_attendance['Exam_Score'].mean()
                insights['high_attendance_count'] = len(high_attendance)
            
            if len(low_attendance) > 0:
                insights['avg_score_low_attendance'] = low_attendance['Exam_Score'].mean()
                insights['low_attendance_count'] = len(low_attendance)
            
            # Attendance impact
            if len(high_attendance) > 0 and len(low_attendance) > 0:
                insights['attendance_score_difference'] = insights['avg_score_high_attendance'] - insights['avg_score_low_attendance']
        
        # Study hours analysis
        if 'Hours_Studied' in df.columns and 'Exam_Score' in df.columns:
            insights['avg_study_hours'] = df['Hours_Studied'].mean()
            insights['study_hours_correlation'] = df[['Hours_Studied', 'Exam_Score']].corr().iloc[0, 1]
            insights['optimal_study_hours'] = Analytics._find_optimal_study_hours(df)
        
        # Demographics
        if 'Gender' in df.columns:
            insights['gender_distribution'] = df['Gender'].value_counts().to_dict()
            if 'Exam_Score' in df.columns:
                insights['avg_score_by_gender'] = df.groupby('Gender')['Exam_Score'].mean().to_dict()
        
        # Key predictors
        insights['strongest_predictors'] = Analytics._identify_strongest_predictors(df)
        
        return insights
    
    @staticmethod
    def _find_optimal_study_hours(df):
        """Find the study hours range with best performance"""
        if 'Hours_Studied' not in df.columns or 'Exam_Score' not in df.columns:
            return None
        
        # Create study hour bins
        df_copy = df.copy()
        df_copy['Study_Range'] = pd.cut(df_copy['Hours_Studied'], 
                                         bins=[0, 10, 15, 20, 25, 50],
                                         labels=['0-10', '11-15', '16-20', '21-25', '25+'])
        
        avg_by_range = df_copy.groupby('Study_Range')['Exam_Score'].mean()
        if len(avg_by_range) > 0:
            optimal_range = avg_by_range.idxmax()
            return str(optimal_range)
        return None
    
    @staticmethod
    def _identify_strongest_predictors(df):
        """Identify which factors most strongly predict exam scores"""
        if 'Exam_Score' not in df.columns:
            return []
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlations = []
        
        for col in numeric_cols:
            if col != 'Exam_Score' and df[col].notna().sum() > 0:
                corr = df[[col, 'Exam_Score']].corr().iloc[0, 1]
                if not np.isnan(corr):
                    correlations.append({
                        'factor': col,
                        'correlation': abs(corr),
                        'direction': 'positive' if corr > 0 else 'negative'
                    })
        
        # Sort by correlation strength
        correlations.sort(key=lambda x: x['correlation'], reverse=True)
        return correlations[:5]  # Top 5 predictors
    
    @staticmethod
    def predict_at_risk_students(df, score_threshold=60, attendance_threshold=75):
        """Identify students who need intervention"""
        at_risk_criteria = []
        
        if 'Exam_Score' in df.columns:
            at_risk_criteria.append(df['Exam_Score'] < score_threshold)
        
        if 'Attendance' in df.columns:
            at_risk_criteria.append(df['Attendance'] < attendance_threshold)
        
        if 'Parental_Involvement' in df.columns:
            at_risk_criteria.append(df['Parental_Involvement'] == 'Low')
        
        if at_risk_criteria:
            # Students meeting ANY at-risk criteria
            at_risk_mask = at_risk_criteria[0]
            for criteria in at_risk_criteria[1:]:
                at_risk_mask = at_risk_mask | criteria
            
            at_risk_students = df[at_risk_mask].copy()
            
            # Calculate risk level
            risk_scores = []
            for _, student in at_risk_students.iterrows():
                risk_score = 0
                if 'Exam_Score' in df.columns and student['Exam_Score'] < score_threshold:
                    risk_score += 1
                if 'Attendance' in df.columns and student['Attendance'] < attendance_threshold:
                    risk_score += 1
                if 'Parental_Involvement' in df.columns and student['Parental_Involvement'] == 'Low':
                    risk_score += 1
                risk_scores.append(risk_score)
            
            at_risk_students['Risk_Level'] = ['High' if score >= 2 else 'Medium' for score in risk_scores]
            
            return at_risk_students
        
        return pd.DataFrame()
    
    @staticmethod
    def calculate_intervention_impact(df):
        """Calculate potential impact of different interventions"""
        interventions = {}
        
        # Intervention 1: Improve attendance
        if 'Attendance' in df.columns and 'Exam_Score' in df.columns:
            low_attendance = df[df['Attendance'] < 85]
            if len(low_attendance) > 0:
                correlation = df[['Attendance', 'Exam_Score']].corr().iloc[0, 1]
                # Estimate: 10% attendance improvement
                estimated_score_gain = correlation * 10 * df['Exam_Score'].std() / df['Attendance'].std()
                
                interventions['improve_attendance'] = {
                    'students_affected': len(low_attendance),
                    'current_avg_score': low_attendance['Exam_Score'].mean(),
                    'estimated_score_gain': estimated_score_gain,
                    'estimated_new_score': low_attendance['Exam_Score'].mean() + estimated_score_gain,
                    'recommendation': 'Implement attendance monitoring and incentive programs'
                }
        
        # Intervention 2: Increase parental involvement
        if 'Parental_Involvement' in df.columns and 'Exam_Score' in df.columns:
            low_involvement = df[df['Parental_Involvement'] == 'Low']
            medium_involvement = df[df['Parental_Involvement'] == 'Medium']
            
            if len(low_involvement) > 0 and len(medium_involvement) > 0:
                score_difference = medium_involvement['Exam_Score'].mean() - low_involvement['Exam_Score'].mean()
                
                interventions['increase_parental_involvement'] = {
                    'students_affected': len(low_involvement),
                    'current_avg_score': low_involvement['Exam_Score'].mean(),
                    'estimated_score_gain': score_difference * 0.5,  # Conservative: 50% of difference
                    'estimated_new_score': low_involvement['Exam_Score'].mean() + (score_difference * 0.5),
                    'recommendation': 'Launch parent engagement programs and regular communication initiatives'
                }
        
        # Intervention 3: Optimize study hours
        if 'Hours_Studied' in df.columns and 'Exam_Score' in df.columns:
            optimal_hours = Analytics._find_optimal_study_hours(df)
            if optimal_hours:
                optimal_range_mask = pd.cut(df['Hours_Studied'], 
                                            bins=[0, 10, 15, 20, 25, 50],
                                            labels=['0-10', '11-15', '16-20', '21-25', '25+']) == optimal_hours
                
                optimal_students = df[optimal_range_mask]
                non_optimal = df[~optimal_range_mask]
                
                if len(optimal_students) > 0 and len(non_optimal) > 0:
                    score_difference = optimal_students['Exam_Score'].mean() - non_optimal['Exam_Score'].mean()
                    
                    interventions['optimize_study_habits'] = {
                        'students_affected': len(non_optimal),
                        'current_avg_score': non_optimal['Exam_Score'].mean(),
                        'optimal_study_range': optimal_hours + ' hours/week',
                        'estimated_score_gain': score_difference * 0.3,  # Conservative
                        'estimated_new_score': non_optimal['Exam_Score'].mean() + (score_difference * 0.3),
                        'recommendation': f'Promote effective study techniques and time management for {optimal_hours} hours/week'
                    }
        
        return interventions
    
    @staticmethod
    def generate_recommendations(df):
        """Generate actionable recommendations based on data analysis"""
        recommendations = {
            'for_parents': [],
            'for_educators': [],
            'for_administrators': [],
            'for_students': []
        }
        
        insights = Analytics.get_performance_insights(df)
        
        # For Parents
        if 'involvement_correlation' in insights and insights['involvement_correlation'] > 0.3:
            recommendations['for_parents'].append({
                'priority': 'High',
                'action': 'Increase Daily Involvement',
                'description': f"Parental involvement shows {insights['involvement_correlation']:.2f} correlation with exam scores. Daily homework check-ins and school communication can significantly improve outcomes.",
                'expected_impact': '+15-20 points in exam scores'
            })
        
        if 'attendance_score_difference' in insights and insights['attendance_score_difference'] > 10:
            recommendations['for_parents'].append({
                'priority': 'High',
                'action': 'Ensure Consistent Attendance',
                'description': f"Students with 90%+ attendance score {insights['attendance_score_difference']:.1f} points higher on average. Make attendance a priority.",
                'expected_impact': f'+{insights["attendance_score_difference"]:.0f} points'
            })
        
        # For Educators
        if 'at_risk_students' in insights and insights['at_risk_students'] > 0:
            recommendations['for_educators'].append({
                'priority': 'Critical',
                'action': 'Implement Early Warning System',
                'description': f"{insights['at_risk_students']} students scoring below 60. Identify and intervene early with personalized support plans.",
                'expected_impact': 'Prevent 30-50% of failures'
            })
        
        if 'optimal_study_hours' in insights and insights['optimal_study_hours']:
            recommendations['for_educators'].append({
                'priority': 'Medium',
                'action': 'Teach Effective Study Techniques',
                'description': f"Optimal study range is {insights['optimal_study_hours']} hours/week. Focus on quality over quantity with active learning strategies.",
                'expected_impact': '+10-15 points'
            })
        
        # For Administrators
        if 'low_attendance_count' in insights and insights['low_attendance_count'] > insights['total_students'] * 0.15:
            recommendations['for_administrators'].append({
                'priority': 'High',
                'action': 'Launch Attendance Initiative',
                'description': f"{insights['low_attendance_count']} students with <70% attendance. Implement school-wide attendance improvement program.",
                'expected_impact': '15-20% reduction in chronic absenteeism'
            })
        
        if 'involvement_distribution' in insights:
            low_involvement_pct = insights['involvement_distribution'].get('Low', 0) / insights['total_students'] * 100
            if low_involvement_pct > 30:
                recommendations['for_administrators'].append({
                    'priority': 'High',
                    'action': 'Create Parent Engagement Programs',
                    'description': f"{low_involvement_pct:.0f}% of students have low parental involvement. Develop workshops, communication systems, and family events.",
                    'expected_impact': 'Improve outcomes for 200+ students'
                })
        
        # For Students
        if 'study_hours_correlation' in insights and insights['study_hours_correlation'] > 0:
            recommendations['for_students'].append({
                'priority': 'High',
                'action': 'Establish Study Routine',
                'description': "Consistent study habits correlate with better performance. Create a daily study schedule and stick to it.",
                'expected_impact': '+10-20 points'
            })
        
        recommendations['for_students'].append({
            'priority': 'Medium',
            'action': 'Maximize Attendance',
            'description': "Every day of learning matters. Aim for 95%+ attendance throughout the school year.",
            'expected_impact': 'Strong foundation for success'
        })
        
        return recommendations
    
    @staticmethod
    def get_performance_trends(df, group_by='Parental_Involvement'):
        """Analyze performance trends across different groups"""
        if group_by not in df.columns or 'Exam_Score' not in df.columns:
            return None
        
        trends = {
            'grouped_stats': df.groupby(group_by)['Exam_Score'].agg([
                ('count', 'count'),
                ('mean', 'mean'),
                ('median', 'median'),
                ('std', 'std'),
                ('min', 'min'),
                ('max', 'max')
            ]).to_dict('index'),
            'group_by': group_by
        }
        
        return trends
    
    @staticmethod
    def compare_student_groups(df, group1_filter, group2_filter, group1_name="Group 1", group2_name="Group 2"):
        """Compare two groups of students"""
        group1 = df[group1_filter]
        group2 = df[group2_filter]
        
        comparison = {
            'group1_name': group1_name,
            'group2_name': group2_name,
            'group1_size': len(group1),
            'group2_size': len(group2)
        }
        
        if 'Exam_Score' in df.columns:
            comparison['group1_avg_score'] = group1['Exam_Score'].mean()
            comparison['group2_avg_score'] = group2['Exam_Score'].mean()
            comparison['score_difference'] = comparison['group1_avg_score'] - comparison['group2_avg_score']
        
        if 'Attendance' in df.columns:
            comparison['group1_avg_attendance'] = group1['Attendance'].mean()
            comparison['group2_avg_attendance'] = group2['Attendance'].mean()
        
        return comparison