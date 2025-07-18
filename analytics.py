import pandas as pd
import numpy as np

class Analytics:
    @staticmethod
    def analyze_parental_involvement_correlation(df):
        """Analyze correlation between parental involvement and student performance"""
        involvement_mapping = {'Low': 1, 'Medium': 2, 'High': 3}
        df_analysis = df.copy()
        df_analysis['Parental_Involvement_Numeric'] = df_analysis['Parental_Involvement'].map(involvement_mapping)
        correlation = df_analysis['Parental_Involvement_Numeric'].corr(df_analysis['Exam_Score'])
        n = len(df_analysis)
        if n > 30:
            p_value = 0.001 if abs(correlation) > 0.3 else 0.05 if abs(correlation) > 0.2 else 0.1
        else:
            p_value = 0.01 if abs(correlation) > 0.5 else 0.1
        return correlation, p_value

    @staticmethod
    def get_performance_insights(df):
        insights = {}
        insights['total_students'] = len(df)
        insights['avg_score'] = df['Exam_Score'].mean()
        insights['avg_attendance'] = df['Attendance'].mean()
        insights['high_performers_pct'] = (df['Exam_Score'] >= 70).mean() * 100
        insights['high_involvement_pct'] = (df['Parental_Involvement'] == 'High').mean() * 100
        high_involvement = df[df['Parental_Involvement'] == 'High']['Exam_Score'].mean()
        low_involvement = df[df['Parental_Involvement'] == 'Low']['Exam_Score'].mean()
        if not pd.isna(high_involvement) and not pd.isna(low_involvement):
            insights['involvement_impact'] = high_involvement - low_involvement
            insights['high_involvement_mean'] = high_involvement
            insights['low_involvement_mean'] = low_involvement
            insights['summary'] = (
                f"Students with high parental involvement score {high_involvement:.1f} on average, "
                f"while those with low involvement score {low_involvement:.1f}. "
                f"This {high_involvement-low_involvement:.1f}-point gap highlights the impact of parental engagement on performance."
            )
        high_performers = df[df['Exam_Score'] >= 70]
        if len(high_performers) > 0:
            insights['high_perf_traits'] = {
                'High Parental Involvement': (high_performers['Parental_Involvement'] == 'High').mean() * 100,
                'Excellent Attendance': (high_performers['Attendance'] > 85).mean() * 100,
                'High Study Hours': (high_performers['Hours_Studied'] > 20).mean() * 100
            }
        return insights

    @staticmethod
    def get_plot_explanations(df):
        explanations = {}
        counts = df['Parental_Involvement'].value_counts()
        explanations['Parental Involvement Distribution'] = (
            f"This donut chart shows the proportion of students with Low, Medium, and High parental involvement. "
            f"High involvement: {counts.get('High',0)} students ({(counts.get('High',0)/len(df)*100):.1f}%). "
            f"Low involvement: {counts.get('Low',0)} students ({(counts.get('Low',0)/len(df)*100):.1f}%). "
            "Higher parental involvement is associated with better student outcomes."
        )
        perf_counts = df['Performance_Category'].value_counts()
        explanations['Academic Performance Distribution'] = (
            f"This bar chart shows the distribution of student grades. Most students fall in the following categories: "
            + ", ".join([f"{cat}: {count}" for cat, count in perf_counts.items()]) + ". "
            "A higher proportion of A/B grades is a positive sign."
        )
        att_counts = df['Attendance_Category'].value_counts()
        explanations['Attendance Level Distribution'] = (
            f"This bar chart shows attendance levels. Excellent attendance: {att_counts.get('Excellent (>85%)',0)} students. "
            f"Poor attendance: {att_counts.get('Poor (≤70%)',0)} students. "
            "Students with excellent attendance tend to perform better."
        )
        mean_score = df['Exam_Score'].mean()
        explanations['Distribution of Exam Scores'] = (
            f"This histogram shows the spread of exam scores. The average score is {mean_score:.1f}. "
            "A right-skewed distribution indicates more high performers."
        )
        return explanations

    @staticmethod
    def get_engagement_recommendations(df):
        recommendations = []
        # 4. Attendance
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
        # 5. Study Habits
        if 'Hours_Studied' in df.columns:
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
      
        # 8. Overall Performance
        avg_score = df['Exam_Score'].mean()
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