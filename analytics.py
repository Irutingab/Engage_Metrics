import pandas as pd
import numpy as np

class Analytics:
    @staticmethod
    def get_performance_insights(df):
        insights = {}
        insights['total_students'] = len(df)
        insights['avg_score'] = df['Average_Score'].mean()
        insights['avg_attendance'] = df['Attendance'].mean()
        insights['high_performers_pct'] = (df['Average_Score'] >= 70).mean() * 100
        insights['high_involvement_pct'] = (df['parental level of education'] == 'master\'s degree').mean() * 100
        high_involvement = df[df['parental level of education'] == 'master\'s degree']['Average_Score'].mean()
        low_involvement = df[df['parental level of education'] == 'some high school']['Average_Score'].mean()
        if not pd.isna(high_involvement) and not pd.isna(low_involvement):
            insights['involvement_impact'] = high_involvement - low_involvement
            insights['high_involvement_mean'] = high_involvement
            insights['low_involvement_mean'] = low_involvement
            insights['summary'] = (
                f"Students with high parental involvement score {high_involvement:.1f} on average, "
                f"while those with low involvement score {low_involvement:.1f}. "
                f"This {high_involvement-low_involvement:.1f}-point gap highlights the impact of parental engagement on performance."
            )
        high_performers = df[df['Average_Score'] >= 70]
        if len(high_performers) > 0:
            insights['high_perf_traits'] = {
                'High Parental Involvement': (high_performers['parental level of education'] == 'master\'s degree').mean() * 100,
                'Excellent Attendance': (high_performers['Attendance'] > 85).mean() * 100,
                'High Study Hours': (high_performers['Hours_Studied'] > 20).mean() * 100
            }
        return insights

    @staticmethod
    def get_engagement_recommendations(df):
        recommendations = []
        # 4. Attendance
        low_attendance_students = df[df['Attendance'] < 85]
        if len(low_attendance_students) > 0:
            low_attendance_pct = (len(low_attendance_students) / len(df)) * 100
            avg_score_low_attendance = low_attendance_students['Average_Score'].mean()
            avg_score_high_attendance = df[df['Attendance'] >= 85]['Average_Score'].mean()
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
        # 5. Study Habits
        if 'Hours_Studied' in df.columns:
            high_study_hours = df[df['Hours_Studied'] > 20]['Average_Score'].mean()
            low_study_hours = df[df['Hours_Studied'] <= 10]['Average_Score'].mean()
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
      
        # 8. Overall Performance
        avg_score = df['Average_Score'].mean()
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