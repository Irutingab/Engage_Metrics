"""
Goal Setting and Progress Tracking System
Allows students, parents, and educators to set goals and track progress
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class GoalTracker:
    """Manage academic goals and track progress over time - Multi-student support"""
    
    def __init__(self):
        """Initialize goal tracker for managing goals across all students"""
        self.goals = []
        self.next_goal_id = 1
    
    def create_goal(self, student_id, goal_type, current_value, target_value, 
                   timeline_days=90, description="", priority="medium", target_date=None):
        """
        Create a new academic goal for a student
        
        Args:
            student_id: ID of the student
            goal_type: Type of goal ('Exam Score', 'Attendance', 'Study Hours', etc.)
            current_value: Starting value
            target_value: Desired end value
            timeline_days: Number of days to achieve goal (default: 90)
            description: Custom description
            priority: 'high', 'medium', or 'low'
            target_date: Optional target date string
        
        Returns:
            goal_id: ID of created goal
        """
        goal_id = self.next_goal_id
        self.next_goal_id += 1
        
        # Parse target date if provided, otherwise calculate from timeline_days
        if target_date:
            try:
                t_date = datetime.fromisoformat(str(target_date)) if isinstance(target_date, str) else target_date
            except:
                t_date = datetime.now() + timedelta(days=timeline_days)
        else:
            t_date = datetime.now() + timedelta(days=timeline_days)
        
        goal = {
            'goal_id': goal_id,
            'student_id': student_id,
            'goal_type': goal_type,
            'current_value': current_value,
            'target_value': target_value,
            'baseline_value': current_value,
            'timeline_days': timeline_days,
            'description': description or f"Improve {goal_type} from {current_value} to {target_value}",
            'priority': priority,
            'created_date': datetime.now(),
            'target_date': t_date,
            'status': 'active',
            'milestones': self._generate_milestones(current_value, target_value, timeline_days),
            'progress_history': [{'date': datetime.now().isoformat(), 'value': current_value}]
        }
        
        self.goals.append(goal)
        return goal_id
    
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
    
    def update_progress(self, goal_id, new_value, notes="", date=None):
        """
        Update progress for a goal
        
        Args:
            goal_id: ID of the goal
            new_value: New progress value
            notes: Optional progress notes
            date: Optional date (defaults to now)
        """
        goal = next((g for g in self.goals if g['goal_id'] == goal_id), None)
        if not goal:
            return {"error": "Goal not found"}
        
        update_date = date or datetime.now()
        update_date_str = update_date.isoformat() if isinstance(update_date, datetime) else str(update_date)
        
        # Add to progress history
        goal['progress_history'].append({
            'date': update_date_str,
            'value': new_value,
            'notes': notes
        })
        
        # Update current value
        goal['current_value'] = new_value
        
        # Check milestones
        for milestone in goal['milestones']:
            if not milestone['achieved'] and new_value >= milestone['target_value']:
                milestone['achieved'] = True
                milestone['achievement_date'] = update_date_str
        
        # Check if goal is achieved
        if new_value >= goal['target_value']:
            goal['status'] = 'achieved'
            goal['achievement_date'] = update_date_str
        elif update_date > goal['target_date'] and new_value < goal['target_value']:
            goal['status'] = 'missed'
        
        return {"success": True, "goal_id": goal_id, "new_value": new_value}
    
    def get_goal_status(self, goal_id):
        """Get detailed status of a goal"""
        goal = next((g for g in self.goals if g['goal_id'] == goal_id), None)
        if not goal:
            return None
        
        created_date = datetime.fromisoformat(goal['created_date']) if isinstance(goal['created_date'], str) else goal['created_date']
        target_date = datetime.fromisoformat(goal['target_date']) if isinstance(goal['target_date'], str) else goal['target_date']
        
        days_elapsed = (datetime.now() - created_date).days
        days_remaining = (target_date - datetime.now()).days
        
        # Calculate progress percentage
        total_improvement = goal['target_value'] - goal['baseline_value']
        current_improvement = goal['current_value'] - goal['baseline_value']
        progress_pct = (current_improvement / total_improvement * 100) if total_improvement != 0 else 100
        
        expected_progress = (days_elapsed / goal['timeline_days'] * 100) if goal['timeline_days'] > 0 else 0
        
        status = {
            'goal': goal,
            'goal_id': goal_id,
            'current_value': goal['current_value'],
            'target_value': goal['target_value'],
            'progress_percentage': progress_pct,
            'days_elapsed': days_elapsed,
            'days_remaining': max(0, days_remaining),
            'progress_percentage': progress_pct,
            'expected_progress': expected_progress,
            'on_track': progress_pct >= expected_progress,
            'pace': 'ahead' if progress_pct > expected_progress + 10 else 'on track' if progress_pct >= expected_progress - 10 else 'behind',
            'next_milestone': next((m for m in goal['milestones'] if not m['achieved']), None)
        }
        
        return status
    
    def get_student_goals(self, student_id, status_filter=None):
        """
        Get all goals for a specific student
        
        Args:
            student_id: ID of the student
            status_filter: Optional filter ('active', 'achieved', 'missed')
        
        Returns:
            List of goals for the student
        """
        student_goals = [g for g in self.goals if g['student_id'] == student_id]
        
        if status_filter:
            student_goals = [g for g in student_goals if g['status'] == status_filter]
        
        return student_goals
    
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
    
    def suggest_goals(self, df, student_id):
        """
        Suggest goals based on student performance
        
        Args:
            df: DataFrame with all student data
            student_id: ID of the student
        
        Returns:
            List of suggested goals
        """
        # Find student data
        if 'Student_ID' in df.columns:
            student_data = df[df['Student_ID'] == student_id]
        else:
            student_data = df.iloc[[student_id - 1]] if student_id <= len(df) else None
        
        if student_data is None or len(student_data) == 0:
            return []
        
        student_row = student_data.iloc[0]
        suggestions = []
        
        # Exam score goal
        if 'Exam_Score' in df.columns:
            current_score = student_row['Exam_Score']
            class_avg = df['Exam_Score'].mean()
            
            if current_score < 70:
                target = 70
                priority = 'High'
                reason = "Reach passing grade (70) - Essential for academic progress"
            elif current_score < class_avg:
                target = class_avg + 5
                priority = 'Medium'
                reason = f"Score above class average ({class_avg:.1f}) - Shows improvement"
            else:
                target = min(current_score + 10, 98)
                priority = 'Medium'
                reason = "Maintain excellence and aim for top performance"
            
            suggestions.append({
                'goal_type': 'Exam Score',
                'current_value': float(current_score),
                'target_value': float(target),
                'timeline_days': 90,
                'reason': reason,
                'priority': priority
            })
        
        # Attendance goal
        if 'Attendance' in df.columns:
            current_attendance = student_row['Attendance']
            
            if current_attendance < 85:
                target = 90
                priority = 'High'
                reason = "Achieve 90% attendance - Critical for academic success"
            elif current_attendance < 95:
                target = 95
                priority = 'Medium'
                reason = "Reach 95% attendance - Excellent performance level"
            else:
                target = 98
                priority = 'Low'
                reason = "Maintain near-perfect attendance"
            
            suggestions.append({
                'goal_type': 'Attendance',
                'current_value': float(current_attendance),
                'target_value': float(target),
                'timeline_days': 60,
                'reason': reason,
                'priority': priority
            })
        
        # Study hours goal
        if 'Hours_Studied' in df.columns:
            current_hours = student_row['Hours_Studied']
            
            if current_hours < 15:
                target = 18
                priority = 'High'
                reason = "Increase to recommended 15-20 hours/week for better results"
            elif current_hours < 20:
                target = 20
                priority = 'Medium'
                reason = "Optimize study time to 20 hours/week for maximum effectiveness"
            else:
                target = current_hours
                priority = 'Low'
                reason = "Maintain consistent study schedule"
            
            suggestions.append({
                'goal_type': 'Study Hours',
                'current_value': float(current_hours),
                'target_value': float(target),
                'timeline_days': 30,
                'reason': reason,
                'priority': priority
            })
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        suggestions.sort(key=lambda x: priority_order.get(x['priority'], 2))
        
        return suggestions
        
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
