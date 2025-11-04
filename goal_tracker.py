"""
Goal Setting and Progress Tracking System
Allows students, parents, and educators to set goals and track progress
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class GoalTracker:
    """Manage academic goals and track progress over time"""
    
    def __init__(self, student_id=None):
        self.student_id = student_id
        self.goals = []
    
    def create_goal(self, goal_type, current_value, target_value, timeline_days=90, 
                   description="", priority="medium"):
        """
        Create a new academic goal
        
        Args:
            goal_type: Type of goal ('exam_score', 'attendance', 'study_hours', etc.)
            current_value: Starting value
            target_value: Desired end value
            timeline_days: Number of days to achieve goal
            description: Custom description
            priority: 'high', 'medium', or 'low'
        """
        goal = {
            'id': len(self.goals) + 1,
            'student_id': self.student_id,
            'goal_type': goal_type,
            'current_value': current_value,
            'target_value': target_value,
            'baseline_value': current_value,
            'timeline_days': timeline_days,
            'description': description or f"Improve {goal_type} from {current_value} to {target_value}",
            'priority': priority,
            'created_date': datetime.now(),
            'target_date': datetime.now() + timedelta(days=timeline_days),
            'status': 'active',
            'milestones': self._generate_milestones(current_value, target_value, timeline_days),
            'progress_history': [{'date': datetime.now(), 'value': current_value}]
        }
        
        self.goals.append(goal)
        return goal
    
    def _generate_milestones(self, current, target, days):
        """Generate intermediate milestones (30/60/90 day checkpoints)"""
        milestones = []
        difference = target - current
        
        checkpoints = [30, 60, 90] if days >= 90 else [days // 3, 2 * days // 3, days]
        
        for i, day in enumerate(checkpoints, 1):
            if day <= days:
                progress_pct = day / days
                milestone_value = current + (difference * progress_pct)
                milestones.append({
                    'day': day,
                    'target_value': milestone_value,
                    'achieved': False,
                    'achievement_date': None
                })
        
        return milestones
    
    def update_progress(self, goal_id, new_value, date=None):
        """Update progress for a goal"""
        goal = next((g for g in self.goals if g['id'] == goal_id), None)
        if not goal:
            return {"error": "Goal not found"}
        
        update_date = date or datetime.now()
        
        # Add to progress history
        goal['progress_history'].append({
            'date': update_date,
            'value': new_value
        })
        
        # Update current value
        goal['current_value'] = new_value
        
        # Check milestones
        for milestone in goal['milestones']:
            if not milestone['achieved'] and new_value >= milestone['target_value']:
                milestone['achieved'] = True
                milestone['achievement_date'] = update_date
        
        # Check if goal is achieved
        if new_value >= goal['target_value']:
            goal['status'] = 'achieved'
            goal['achievement_date'] = update_date
        
        # Calculate progress percentage
        total_improvement = goal['target_value'] - goal['baseline_value']
        current_improvement = new_value - goal['baseline_value']
        goal['progress_percentage'] = (current_improvement / total_improvement * 100) if total_improvement != 0 else 100
        
        return goal
    
    def get_goal_status(self, goal_id):
        """Get detailed status of a goal"""
        goal = next((g for g in self.goals if g['id'] == goal_id), None)
        if not goal:
            return None
        
        days_elapsed = (datetime.now() - goal['created_date']).days
        days_remaining = (goal['target_date'] - datetime.now()).days
        
        progress_pct = goal.get('progress_percentage', 0)
        expected_progress = (days_elapsed / goal['timeline_days'] * 100) if goal['timeline_days'] > 0 else 0
        
        status = {
            'goal': goal,
            'days_elapsed': days_elapsed,
            'days_remaining': max(0, days_remaining),
            'progress_percentage': progress_pct,
            'expected_progress': expected_progress,
            'on_track': progress_pct >= expected_progress,
            'pace': 'ahead' if progress_pct > expected_progress + 10 else 'on track' if progress_pct >= expected_progress - 10 else 'behind',
            'next_milestone': next((m for m in goal['milestones'] if not m['achieved']), None)
        }
        
        return status
    
    def get_all_active_goals(self):
        """Get all active goals"""
        return [g for g in self.goals if g['status'] == 'active']
    
    def get_achievement_summary(self):
        """Get summary of all goals"""
        total_goals = len(self.goals)
        achieved = len([g for g in self.goals if g['status'] == 'achieved'])
        active = len([g for g in self.goals if g['status'] == 'active'])
        
        return {
            'total_goals': total_goals,
            'achieved': achieved,
            'active': active,
            'achievement_rate': (achieved / total_goals * 100) if total_goals > 0 else 0,
            'goals': self.goals
        }
    
    def generate_progress_report(self, goal_id):
        """Generate detailed progress report for a goal"""
        status = self.get_goal_status(goal_id)
        if not status:
            return "Goal not found"
        
        goal = status['goal']
        
        report = f"""
GOAL PROGRESS REPORT
{'=' * 60}
Goal: {goal['description']}
Priority: {goal['priority'].upper()}
Created: {goal['created_date'].strftime('%Y-%m-%d')}
Target Date: {goal['target_date'].strftime('%Y-%m-%d')}

CURRENT STATUS:
{'-' * 60}
Baseline Value: {goal['baseline_value']}
Current Value: {goal['current_value']}
Target Value: {goal['target_value']}
Progress: {status['progress_percentage']:.1f}%

TIME TRACKING:
{'-' * 60}
Days Elapsed: {status['days_elapsed']}
Days Remaining: {status['days_remaining']}
Pace: {status['pace'].upper()}
On Track: {'✓ YES' if status['on_track'] else '✗ NO'}

MILESTONES:
{'-' * 60}
"""
        
        for i, milestone in enumerate(goal['milestones'], 1):
            status_icon = '✓' if milestone['achieved'] else '○'
            report += f"{status_icon} Day {milestone['day']}: Target {milestone['target_value']:.1f}"
            if milestone['achieved']:
                report += f" (Achieved on {milestone['achievement_date'].strftime('%Y-%m-%d')})"
            report += "\n"
        
        report += f"\nRECOMMENDATIONS:\n{'-' * 60}\n"
        
        if status['pace'] == 'behind':
            report += "• URGENT: Increase effort to get back on track\n"
            report += "• Consider additional support or tutoring\n"
            report += "• Review and adjust study strategies\n"
        elif status['pace'] == 'ahead':
            report += "• EXCELLENT: Continue current strategies\n"
            report += "• Consider setting more ambitious goals\n"
            report += "• Share successful strategies with others\n"
        else:
            report += "• GOOD: Maintain current pace\n"
            report += "• Stay focused on daily habits\n"
            report += "• Prepare for next milestone\n"
        
        return report
    
    def suggest_goals(self, student_data, class_data):
        """Suggest goals based on student performance"""
        suggestions = []
        
        # Exam score goal
        if 'Exam_Score' in student_data:
            current_score = student_data['Exam_Score']
            class_avg = class_data['Exam_Score'].mean()
            
            if current_score < 70:
                target = 70
                priority = 'high'
                description = "Reach passing grade (70)"
            elif current_score < class_avg:
                target = class_avg + 5
                priority = 'medium'
                description = f"Score above class average ({class_avg:.1f})"
            else:
                target = min(current_score + 10, 98)
                priority = 'medium'
                description = "Maintain excellence and aim for top performance"
            
            suggestions.append({
                'goal_type': 'exam_score',
                'current_value': current_score,
                'target_value': target,
                'timeline_days': 90,
                'description': description,
                'priority': priority,
                'expected_impact': 'High - Direct impact on grades'
            })
        
        # Attendance goal
        if 'Attendance' in student_data:
            current_attendance = student_data['Attendance']
            
            if current_attendance < 85:
                target = 90
                priority = 'high'
                description = "Achieve 90% attendance (critical for success)"
            elif current_attendance < 95:
                target = 95
                priority = 'medium'
                description = "Reach 95% attendance (excellent)"
            else:
                target = 98
                priority = 'low'
                description = "Maintain near-perfect attendance"
            
            suggestions.append({
                'goal_type': 'attendance',
                'current_value': current_attendance,
                'target_value': target,
                'timeline_days': 60,
                'description': description,
                'priority': priority,
                'expected_impact': 'High - Attendance strongly correlates with performance'
            })
        
        # Study hours goal
        if 'Hours_Studied' in student_data:
            current_hours = student_data['Hours_Studied']
            
            if current_hours < 15:
                target = 18
                priority = 'high'
                description = "Increase to recommended 15-20 hours/week"
            elif current_hours < 20:
                target = 20
                priority = 'medium'
                description = "Optimize study time to 20 hours/week"
            else:
                target = current_hours
                priority = 'low'
                description = "Maintain consistent study schedule"
            
            suggestions.append({
                'goal_type': 'study_hours',
                'current_value': current_hours,
                'target_value': target,
                'timeline_days': 30,
                'description': description,
                'priority': priority,
                'expected_impact': 'Medium - Quality matters more than quantity'
            })
        
        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        suggestions.sort(key=lambda x: priority_order[x['priority']])
        
        return suggestions
    
    def export_goals_to_json(self, filename='goals.json'):
        """Export goals to JSON file"""
        # Convert datetime objects to strings
        export_data = []
        for goal in self.goals:
            goal_copy = goal.copy()
            goal_copy['created_date'] = goal_copy['created_date'].isoformat()
            goal_copy['target_date'] = goal_copy['target_date'].isoformat()
            if 'achievement_date' in goal_copy and goal_copy['achievement_date']:
                goal_copy['achievement_date'] = goal_copy['achievement_date'].isoformat()
            
            # Convert progress history dates
            for entry in goal_copy['progress_history']:
                entry['date'] = entry['date'].isoformat()
            
            # Convert milestone dates
            for milestone in goal_copy['milestones']:
                if milestone['achievement_date']:
                    milestone['achievement_date'] = milestone['achievement_date'].isoformat()
            
            export_data.append(goal_copy)
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def calculate_goal_metrics(self):
        """Calculate overall goal achievement metrics"""
        if not self.goals:
            return None
        
        active_goals = [g for g in self.goals if g['status'] == 'active']
        achieved_goals = [g for g in self.goals if g['status'] == 'achieved']
        
        metrics = {
            'total_goals': len(self.goals),
            'active_goals': len(active_goals),
            'achieved_goals': len(achieved_goals),
            'achievement_rate': len(achieved_goals) / len(self.goals) * 100 if self.goals else 0,
            'average_progress': np.mean([g.get('progress_percentage', 0) for g in active_goals]) if active_goals else 0,
            'goals_on_track': len([g for g in active_goals if self.get_goal_status(g['id'])['on_track']]),
            'goals_behind': len([g for g in active_goals if not self.get_goal_status(g['id'])['on_track']])
        }
        
        return metrics
