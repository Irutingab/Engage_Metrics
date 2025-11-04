"""
Student Profile Generator
Creates detailed individual student reports with personalized recommendations
"""

import pandas as pd
import numpy as np
from datetime import datetime

class StudentProfile:
    """Generate comprehensive student profiles with insights and recommendations"""
    
    def __init__(self, student_data, class_data):
        """
        Args:
            student_data: Series or dict with individual student information
            class_data: DataFrame with all students for comparison
        """
        self.student = student_data if isinstance(student_data, dict) else student_data.to_dict()
        self.class_data = class_data
        self.class_avg = class_data.mean(numeric_only=True)
        
    def generate_comprehensive_report(self):
        """Generate complete student profile report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'student_info': self._get_student_info(),
            'performance_summary': self._analyze_performance(),
            'strengths': self._identify_strengths(),
            'challenges': self._identify_challenges(),
            'peer_comparison': self._compare_to_peers(),
            'factor_analysis': self._analyze_contributing_factors(),
            'recommendations': self._get_personalized_recommendations(),
            'action_plan': self._create_action_plan(),
            'progress_metrics': self._define_progress_metrics()
        }
        return report
    
    def _get_student_info(self):
        """Extract basic student information"""
        info = {}
        
        # Core identifiers
        if 'Student_ID' in self.student:
            info['id'] = self.student['Student_ID']
        
        # Demographics
        for field in ['Gender', 'Age', 'Ethnicity']:
            if field in self.student:
                info[field.lower()] = self.student[field]
        
        # Family background
        for field in ['Parental_Education_Level', 'Family_Income', 'Parental_Involvement']:
            if field in self.student:
                info[field.lower()] = self.student[field]
        
        return info
    
    def _analyze_performance(self):
        """Comprehensive performance analysis"""
        analysis = {}
        
        if 'Exam_Score' in self.student:
            score = self.student['Exam_Score']
            class_avg = self.class_avg.get('Exam_Score', 0)
            class_std = self.class_data['Exam_Score'].std()
            
            # Performance level
            if score >= class_avg + class_std:
                status = "Exceeding Expectations"
                level = "High Performer"
            elif score >= class_avg:
                status = "Meeting Expectations"
                level = "Average Performer"
            elif score >= class_avg - class_std:
                status = "Approaching Expectations"
                level = "Below Average"
            else:
                status = "Needs Significant Support"
                level = "At Risk"
            
            # Percentile calculation
            percentile = (self.class_data['Exam_Score'] < score).sum() / len(self.class_data) * 100
            
            # Letter grade
            if score >= 90:
                grade = 'A'
            elif score >= 80:
                grade = 'B'
            elif score >= 70:
                grade = 'C'
            elif score >= 60:
                grade = 'D'
            else:
                grade = 'F'
            
            analysis['exam_score'] = score
            analysis['class_average'] = class_avg
            analysis['difference_from_average'] = score - class_avg
            analysis['percentile'] = percentile
            analysis['performance_status'] = status
            analysis['performance_level'] = level
            analysis['letter_grade'] = grade
            analysis['standard_deviations_from_mean'] = (score - class_avg) / class_std if class_std > 0 else 0
        
        # Attendance analysis
        if 'Attendance' in self.student:
            attendance = self.student['Attendance']
            class_avg_attendance = self.class_avg.get('Attendance', 0)
            
            if attendance >= 95:
                attendance_rating = "Excellent"
            elif attendance >= 90:
                attendance_rating = "Good"
            elif attendance >= 80:
                attendance_rating = "Fair"
            elif attendance >= 70:
                attendance_rating = "Poor"
            else:
                attendance_rating = "Critical"
            
            analysis['attendance_rate'] = attendance
            analysis['attendance_rating'] = attendance_rating
            analysis['attendance_vs_class'] = attendance - class_avg_attendance
            analysis['days_missed_estimate'] = int((100 - attendance) * 1.8)  # Assuming 180 school days
        
        # Study habits
        if 'Hours_Studied' in self.student:
            study_hours = self.student['Hours_Studied']
            class_avg_study = self.class_avg.get('Hours_Studied', 0)
            
            analysis['study_hours_per_week'] = study_hours
            analysis['study_hours_vs_class'] = study_hours - class_avg_study
            
            if study_hours >= 20:
                study_rating = "Dedicated"
            elif study_hours >= 15:
                study_rating = "Good"
            elif study_hours >= 10:
                study_rating = "Moderate"
            else:
                study_rating = "Insufficient"
            
            analysis['study_habits_rating'] = study_rating
        
        return analysis
    
    def _identify_strengths(self):
        """Identify student's key strengths"""
        strengths = []
        
        # Academic performance
        if 'Exam_Score' in self.student:
            score = self.student['Exam_Score']
            if score >= 85:
                strengths.append({
                    'area': 'Academic Excellence',
                    'description': f'Consistently high exam scores ({score}/100)',
                    'evidence': 'Top performer in class'
                })
        
        # Attendance
        if 'Attendance' in self.student:
            if self.student['Attendance'] >= 95:
                strengths.append({
                    'area': 'Excellent Attendance',
                    'description': f'{self.student["Attendance"]:.1f}% attendance rate',
                    'evidence': 'Rarely misses school'
                })
        
        # Parental involvement
        if 'Parental_Involvement' in self.student:
            if self.student['Parental_Involvement'] == 'High':
                strengths.append({
                    'area': 'Strong Family Support',
                    'description': 'High parental involvement',
                    'evidence': 'Parents actively engaged in education'
                })
        
        # Study habits
        if 'Hours_Studied' in self.student:
            if self.student['Hours_Studied'] >= 20:
                strengths.append({
                    'area': 'Strong Work Ethic',
                    'description': f'{self.student["Hours_Studied"]} hours studied per week',
                    'evidence': 'Dedicated study routine'
                })
        
        # Extracurricular
        if 'Extracurricular_Activities' in self.student:
            if self.student['Extracurricular_Activities'] == 'Yes':
                strengths.append({
                    'area': 'Well-Rounded Development',
                    'description': 'Participates in extracurricular activities',
                    'evidence': 'Balanced academic and personal growth'
                })
        
        # Motivation
        if 'Motivation_Level' in self.student:
            if self.student['Motivation_Level'] == 'High':
                strengths.append({
                    'area': 'High Motivation',
                    'description': 'Self-driven and engaged',
                    'evidence': 'Shows initiative in learning'
                })
        
        return strengths
    
    def _identify_challenges(self):
        """Identify areas needing improvement"""
        challenges = []
        
        # Low scores
        if 'Exam_Score' in self.student:
            score = self.student['Exam_Score']
            if score < 60:
                challenges.append({
                    'area': 'Academic Performance',
                    'severity': 'High',
                    'description': f'Exam score of {score} indicates significant struggles',
                    'impact': 'Risk of course failure'
                })
            elif score < 70:
                challenges.append({
                    'area': 'Academic Performance',
                    'severity': 'Medium',
                    'description': f'Exam score of {score} below proficiency',
                    'impact': 'May struggle with advanced concepts'
                })
        
        # Attendance issues
        if 'Attendance' in self.student:
            attendance = self.student['Attendance']
            if attendance < 80:
                challenges.append({
                    'area': 'Chronic Absenteeism',
                    'severity': 'High',
                    'description': f'Only {attendance:.1f}% attendance rate',
                    'impact': 'Missing critical instruction time'
                })
            elif attendance < 90:
                challenges.append({
                    'area': 'Attendance Concerns',
                    'severity': 'Medium',
                    'description': f'{attendance:.1f}% attendance needs improvement',
                    'impact': 'Gaps in learning continuity'
                })
        
        # Low parental involvement
        if 'Parental_Involvement' in self.student:
            if self.student['Parental_Involvement'] == 'Low':
                challenges.append({
                    'area': 'Limited Family Support',
                    'severity': 'Medium',
                    'description': 'Low parental involvement in education',
                    'impact': 'Reduced accountability and support at home'
                })
        
        # Insufficient study time
        if 'Hours_Studied' in self.student:
            if self.student['Hours_Studied'] < 10:
                challenges.append({
                    'area': 'Inadequate Study Time',
                    'severity': 'Medium',
                    'description': f'Only {self.student["Hours_Studied"]} hours studied per week',
                    'impact': 'Insufficient practice and review'
                })
        
        # Sleep issues
        if 'Sleep_Hours' in self.student:
            if self.student['Sleep_Hours'] < 7:
                challenges.append({
                    'area': 'Sleep Deprivation',
                    'severity': 'Medium',
                    'description': f'Only {self.student["Sleep_Hours"]} hours of sleep',
                    'impact': 'Affects concentration and memory'
                })
        
        # Low motivation
        if 'Motivation_Level' in self.student:
            if self.student['Motivation_Level'] == 'Low':
                challenges.append({
                    'area': 'Low Motivation',
                    'severity': 'High',
                    'description': 'Student shows low engagement',
                    'impact': 'Unlikely to put in necessary effort'
                })
        
        return challenges
    
    def _compare_to_peers(self):
        """Compare student to classmates"""
        comparison = {}
        
        numeric_fields = ['Exam_Score', 'Attendance', 'Hours_Studied', 'Sleep_Hours']
        
        for field in numeric_fields:
            if field in self.student and field in self.class_data.columns:
                student_value = self.student[field]
                class_mean = self.class_data[field].mean()
                class_median = self.class_data[field].median()
                percentile = (self.class_data[field] < student_value).sum() / len(self.class_data) * 100
                
                # Determine standing
                if percentile >= 90:
                    standing = "Top 10%"
                elif percentile >= 75:
                    standing = "Upper Quarter"
                elif percentile >= 50:
                    standing = "Above Average"
                elif percentile >= 25:
                    standing = "Below Average"
                else:
                    standing = "Bottom Quarter"
                
                comparison[field] = {
                    'student_value': student_value,
                    'class_mean': class_mean,
                    'class_median': class_median,
                    'percentile': percentile,
                    'standing': standing,
                    'difference_from_mean': student_value - class_mean
                }
        
        return comparison
    
    def _analyze_contributing_factors(self):
        """Analyze what factors are helping or hurting performance"""
        factors = {
            'positive_factors': [],
            'negative_factors': [],
            'neutral_factors': []
        }
        
        # Analyze each factor
        factor_analysis = [
            ('Attendance', 90, 'positive'),
            ('Parental_Involvement', 'High', 'positive'),
            ('Hours_Studied', 15, 'positive'),
            ('Motivation_Level', 'High', 'positive'),
            ('Sleep_Hours', 7, 'positive'),
            ('Internet_Access', 'Yes', 'positive'),
            ('Tutoring_Sessions', 1, 'positive'),
        ]
        
        for factor_name, threshold, category in factor_analysis:
            if factor_name in self.student:
                value = self.student[factor_name]
                
                if isinstance(threshold, (int, float)):
                    if value >= threshold:
                        factors['positive_factors'].append({
                            'factor': factor_name,
                            'value': value,
                            'impact': 'Supporting academic success'
                        })
                    else:
                        factors['negative_factors'].append({
                            'factor': factor_name,
                            'value': value,
                            'impact': 'May be limiting performance'
                        })
                else:
                    if value == threshold:
                        factors['positive_factors'].append({
                            'factor': factor_name,
                            'value': value,
                            'impact': 'Supporting academic success'
                        })
                    else:
                        factors['negative_factors'].append({
                            'factor': factor_name,
                            'value': value,
                            'impact': 'May be limiting performance'
                        })
        
        return factors
    
    def _get_personalized_recommendations(self):
        """Generate personalized recommendations"""
        recommendations = []
        
        challenges = self._identify_challenges()
        
        # Sort by severity
        high_severity = [c for c in challenges if c.get('severity') == 'High']
        medium_severity = [c for c in challenges if c.get('severity') == 'Medium']
        
        # Address high severity first
        for challenge in high_severity:
            if 'Academic Performance' in challenge['area']:
                recommendations.append({
                    'priority': 1,
                    'area': 'Academic Support',
                    'action': 'Immediate Intervention Required',
                    'specific_steps': [
                        'Schedule meeting with teacher and counselor',
                        'Enroll in tutoring program',
                        'Create personalized learning plan',
                        'Daily progress monitoring'
                    ],
                    'timeline': 'Immediate (this week)'
                })
            
            elif 'Absenteeism' in challenge['area']:
                recommendations.append({
                    'priority': 1,
                    'area': 'Attendance',
                    'action': 'Address Attendance Barriers',
                    'specific_steps': [
                        'Identify root causes of absences',
                        'Create attendance contract',
                        'Set up daily check-in system',
                        'Connect family with support services if needed'
                    ],
                    'timeline': 'Immediate (this week)'
                })
        
        # Address medium severity
        for challenge in medium_severity:
            if 'Study Time' in challenge['area']:
                recommendations.append({
                    'priority': 2,
                    'area': 'Study Habits',
                    'action': 'Develop Structured Study Routine',
                    'specific_steps': [
                        'Create daily study schedule (goal: 15-20 hrs/week)',
                        'Designate quiet study space at home',
                        'Use Pomodoro technique (25 min focus, 5 min break)',
                        'Track study time and subject focus'
                    ],
                    'timeline': 'Within 2 weeks'
                })
            
            elif 'Family Support' in challenge['area']:
                recommendations.append({
                    'priority': 2,
                    'area': 'Parental Involvement',
                    'action': 'Increase Family Engagement',
                    'specific_steps': [
                        'Weekly parent-teacher communication',
                        'Daily homework review (15 minutes)',
                        'Attend parent workshops',
                        'Celebrate small wins together'
                    ],
                    'timeline': 'Ongoing'
                })
        
        # Always include general recommendations
        recommendations.append({
            'priority': 3,
            'area': 'Overall Well-being',
            'action': 'Optimize Learning Conditions',
            'specific_steps': [
                'Ensure 8-9 hours of sleep nightly',
                'Maintain consistent daily routine',
                'Limit screen time during study hours',
                'Encourage extracurricular participation'
            ],
            'timeline': 'Ongoing'
        })
        
        return sorted(recommendations, key=lambda x: x['priority'])
    
    def _create_action_plan(self):
        """Create 30/60/90 day action plan"""
        plan = {
            '30_days': [],
            '60_days': [],
            '90_days': []
        }
        
        challenges = self._identify_challenges()
        
        # 30 days: Address immediate concerns
        plan['30_days'] = [
            'Establish baseline metrics (current scores, attendance)',
            'Implement daily study routine',
            'Set up weekly progress check-ins',
            'Address any attendance issues'
        ]
        
        if any('Academic' in c['area'] for c in challenges):
            plan['30_days'].append('Begin tutoring or extra help sessions')
        
        # 60 days: Build momentum
        plan['60_days'] = [
            'Evaluate progress on 30-day goals',
            'Adjust study strategies based on what\'s working',
            'Improve parental involvement practices',
            'Target specific subject weaknesses'
        ]
        
        # 90 days: Sustain and optimize
        plan['90_days'] = [
            'Achieve target exam score improvement',
            'Maintain 90%+ attendance rate',
            'Establish sustainable study habits',
            'Demonstrate consistent progress'
        ]
        
        return plan
    
    def _define_progress_metrics(self):
        """Define measurable progress indicators"""
        metrics = []
        
        if 'Exam_Score' in self.student:
            current_score = self.student['Exam_Score']
            target_score = min(current_score + 15, 95)  # Aim for +15 points or 95, whichever is lower
            
            metrics.append({
                'metric': 'Exam Score',
                'current': current_score,
                'target_30_days': current_score + 5,
                'target_60_days': current_score + 10,
                'target_90_days': target_score,
                'measurement': 'Next exam or assessment'
            })
        
        if 'Attendance' in self.student:
            current_attendance = self.student['Attendance']
            target_attendance = min(current_attendance + 10, 98)
            
            metrics.append({
                'metric': 'Attendance Rate',
                'current': f'{current_attendance:.1f}%',
                'target_30_days': f'{min(current_attendance + 3, 98):.1f}%',
                'target_60_days': f'{min(current_attendance + 6, 98):.1f}%',
                'target_90_days': f'{target_attendance:.1f}%',
                'measurement': 'Weekly attendance tracking'
            })
        
        if 'Hours_Studied' in self.student:
            current_hours = self.student['Hours_Studied']
            target_hours = min(current_hours + 10, 25)
            
            metrics.append({
                'metric': 'Weekly Study Hours',
                'current': current_hours,
                'target_30_days': min(current_hours + 3, 25),
                'target_60_days': min(current_hours + 6, 25),
                'target_90_days': target_hours,
                'measurement': 'Student study log'
            })
        
        return metrics
    
    def generate_printable_summary(self):
        """Generate a parent-friendly summary"""
        report = self.generate_comprehensive_report()
        
        summary = f"""
STUDENT PERFORMANCE REPORT
Generated: {datetime.now().strftime('%B %d, %Y')}
{'=' * 60}

PERFORMANCE OVERVIEW:
{'-' * 60}
"""
        
        perf = report['performance_summary']
        if 'exam_score' in perf:
            summary += f"Exam Score: {perf['exam_score']}/100 (Class Avg: {perf['class_average']:.1f})\n"
            summary += f"Performance Level: {perf['performance_level']}\n"
            summary += f"Class Percentile: {perf['percentile']:.0f}th\n"
        
        if 'attendance_rate' in perf:
            summary += f"Attendance: {perf['attendance_rate']:.1f}% ({perf['attendance_rating']})\n"
        
        summary += f"\nSTRENGTHS ({len(report['strengths'])}):\n{'-' * 60}\n"
        for i, strength in enumerate(report['strengths'][:3], 1):
            summary += f"{i}. {strength['area']}: {strength['description']}\n"
        
        summary += f"\nAREAS FOR IMPROVEMENT ({len(report['challenges'])}):\n{'-' * 60}\n"
        for i, challenge in enumerate(report['challenges'][:3], 1):
            summary += f"{i}. {challenge['area']} ({challenge['severity']} priority)\n"
            summary += f"   {challenge['description']}\n"
        
        summary += f"\nTOP RECOMMENDATIONS:\n{'-' * 60}\n"
        for i, rec in enumerate(report['recommendations'][:3], 1):
            summary += f"{i}. {rec['action']}\n"
            for step in rec['specific_steps'][:2]:
                summary += f"   • {step}\n"
        
        return summary
