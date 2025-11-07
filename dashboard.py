import streamlit as st
import pandas as pd
import numpy as np
from data_manager import DataManager
from visualizations import Visualizations
from analytics import Analytics
from ai_assistant_educational import EducationalAIAssistant
from student_profile import StudentProfile
from goal_tracker import GoalTracker


class StudentDashboard:

    def __init__(self):
        self.data_manager = DataManager()
        self.visualizations = Visualizations()
        self.analytics = Analytics()
        self.ai_assistant = EducationalAIAssistant()
        self.student_profile = StudentProfile()
        self.goal_tracker = GoalTracker()

        if 'intelligent_mode' not in st.session_state:
            st.session_state.intelligent_mode = False
        
        self.intelligent_dashboard = None

    def run(self):
        """Main dashboard application"""
        st.set_page_config(page_title="EngageMetrics: Student Performance Analytics", layout="wide")
        
        # Header
        st.title("📊 EngageMetrics: Student Performance Analytics")
        st.markdown("""
        **Empowering Education Through Data-Driven Insights**  
        This dashboard helps parents, educators, and policymakers understand the key factors influencing student success.
        """)

        # Sidebar navigation
        st.sidebar.title("🎯 Navigation")
        page = st.sidebar.radio("Select View:", 
                               ["📈 Overview & Analytics", 
                                "👤 Student Profiles", 
                                "🎯 Goal Tracking",
                                "💬 AI Assistant"])
        
        # Load data
        df = self.data_manager.get_processed_data()
        if df is None or df.empty:
            st.error("Failed to load data. Please check your data file.")
            return
        
        df_clean = self.clean_dataframe(df)

        # PAGE 1: Overview & Analytics
        if page == "📈 Overview & Analytics":
            self.render_overview_page(df_clean)
        
        # PAGE 2: Student Profiles
        elif page == "👤 Student Profiles":
            self.render_student_profiles_page(df_clean)
        
        # PAGE 3: Goal Tracking
        elif page == "🎯 Goal Tracking":
            self.render_goal_tracking_page(df_clean)
        
        # PAGE 4: AI Assistant
        elif page == "💬 AI Assistant":
            self.render_ai_assistant_page(df_clean)

    def render_overview_page(self, df):
        """Render the main overview and analytics page"""
        st.header("📊 Performance Overview")
        
        # Get comprehensive insights
        insights = self.analytics.get_performance_insights(df)
        
        # Top metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", f"{insights['total_students']:,}")
        with col2:
            st.metric("Average Score", f"{insights.get('avg_score', 0):.1f}")
        with col3:
            st.metric("At-Risk Students", f"{insights.get('at_risk_students', 0)}")
        with col4:
            st.metric("Avg Attendance", f"{insights.get('avg_attendance', 0):.1f}%")
        
        # Expanded metrics
        at_risk_df = self.analytics.predict_at_risk_students(df)
        high_risk = len(at_risk_df[at_risk_df['risk_level'] == 'High']) if not at_risk_df.empty else 0
        medium_risk = len(at_risk_df[at_risk_df['risk_level'] == 'Medium']) if not at_risk_df.empty else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Median Score", f"{insights.get('median_score', 0):.1f}")
        with col2:
            st.metric("Top 10% Threshold", f"{insights.get('top_10_percent_threshold', 0):.1f}")
        with col3:
            st.metric("High Risk", f"{high_risk}")
        with col4:
            st.metric("Medium Risk", f"{medium_risk}")

        # Interactive Filters
        st.sidebar.header("🔍 Interactive Filters")
        involvement_options = ['All'] + sorted(list(df['Parental_Involvement'].unique()))
        selected_involvement = st.sidebar.selectbox("Filter by Parental Involvement:", involvement_options)

        if 'Gender' in df.columns:
            gender_options = ['All'] + sorted(list(df['Gender'].unique()))
            selected_gender = st.sidebar.selectbox("Filter by Gender:", gender_options)
        else:
            selected_gender = 'All'

        # Apply filters
        filtered_df = df.copy()
        if selected_involvement != 'All':
            filtered_df = filtered_df[filtered_df['Parental_Involvement'] == selected_involvement]
        if selected_gender != 'All' and 'Gender' in df.columns:
            filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

        st.info(f"Showing {len(filtered_df):,} students (filtered from {len(df):,} total)")

        # Key Insights Section
        st.header("🔍 Key Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Strongest Performance Predictors")
            predictors = self.analytics._identify_strongest_predictors(filtered_df)
            for i, (factor, corr) in enumerate(predictors, 1):
                st.write(f"{i}. **{factor}**: {corr:.3f} correlation")
        
        with col2:
            st.subheader("At-Risk Student Analysis")
            at_risk = self.analytics.predict_at_risk_students(filtered_df)
            high_risk = len(at_risk[at_risk['risk_level'] == 'High'])
            medium_risk = len(at_risk[at_risk['risk_level'] == 'Medium'])
            st.write(f"**High Risk:** {high_risk} students")
            st.write(f"**Medium Risk:** {medium_risk} students")
            if high_risk > 0:
                st.warning(f"⚠️ {high_risk} students need immediate attention")

        # Intervention Impact Calculator
        st.header("💡 Intervention Impact Calculator")
        st.markdown("**Estimate the potential impact of targeted interventions**")
        
        interventions = self.analytics.calculate_intervention_impact(filtered_df)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Attendance Improvement")
            if 'improve_attendance' in interventions:
                interv = interventions['improve_attendance']
                st.metric("Students Affected", f"{interv['students_affected']}")
                st.metric("Current Avg Score", f"{interv['current_avg_score']:.1f}")
                st.metric("Expected Gain", f"+{interv['estimated_score_gain']:.2f}")
                st.info(interv['recommendation'])
            else:
                st.info("No attendance intervention needed")
        
        with col2:
            st.subheader("Parental Involvement")
            if 'increase_parental_involvement' in interventions:
                interv = interventions['increase_parental_involvement']
                st.metric("Students Affected", f"{interv['students_affected']}")
                st.metric("Current Avg Score", f"{interv['current_avg_score']:.1f}")
                st.metric("Expected Gain", f"+{interv['estimated_score_gain']:.2f}")
                st.info(interv['recommendation'])
            else:
                st.info("No parental involvement intervention needed")
        
        with col3:
            st.subheader("Study Habits")
            if 'optimize_study_habits' in interventions:
                interv = interventions['optimize_study_habits']
                st.metric("Students Affected", f"{interv['students_affected']}")
                st.metric("Current Avg Score", f"{interv['current_avg_score']:.1f}")
                st.metric("Expected Gain", f"+{interv['estimated_score_gain']:.2f}")
                st.info(interv['recommendation'])
            else:
                st.info("No study habits intervention needed")

        # Visualizations
        st.header("📊 Data Visualizations")
        
        viz_tabs = st.tabs([
            "Distribution Charts", 
            "Correlation Analysis", 
            "Performance Breakdown",
            "Advanced Analytics"
        ])
        
        # Tab 1: Distribution Charts
        with viz_tabs[0]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Parental Involvement Distribution")
                fig1 = self.visualizations.create_donut_chart(
                    filtered_df, 'Parental_Involvement', 'Parental Involvement Distribution'
                )
                st.pyplot(fig1)
            
            with col2:
                st.subheader("Performance Distribution")
                fig2 = self.visualizations.create_histogram_chart(
                    filtered_df, 'Performance_Category', 'Academic Performance Distribution'
                )
                st.pyplot(fig2)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Exam Score Distribution")
                fig3 = self.visualizations.create_histogram_chart(
                    filtered_df, 'Exam_Score', 'Distribution of Exam Scores'
                )
                st.pyplot(fig3)
            
            with col2:
                st.subheader("Attendance Distribution")
                fig4 = self.visualizations.create_histogram_chart(
                    filtered_df, 'Attendance', 'Distribution of Attendance'
                )
                st.pyplot(fig4)
        
        # Tab 2: Correlation Analysis
        with viz_tabs[1]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Correlation Heatmap")
                fig5 = self.visualizations.create_correlation_heatmap(filtered_df)
                if fig5:
                    st.pyplot(fig5)
                    st.markdown("""
                    **Interpretation:** Darker colors indicate stronger relationships. 
                    Look for high correlations with Exam_Score to identify key success factors.
                    """)
            
            with col2:
                st.subheader("Factor Importance")
                fig6 = self.visualizations.create_factor_importance_chart(filtered_df)
                if fig6:
                    st.pyplot(fig6)
                    st.markdown("""
                    **Key Insight:** This chart ranks factors by their correlation with exam scores.
                    Focus interventions on the top factors for maximum impact.
                    """)
            
            st.subheader("Scatter Plot: Study Hours vs Exam Score")
            if 'Hours_Studied' in filtered_df.columns:
                fig7 = self.visualizations.create_scatter_plot(
                    filtered_df, 'Hours_Studied', 'Exam_Score', 
                    'Study Hours vs Exam Score'
                )
                if fig7:
                    st.pyplot(fig7)
        
        # Tab 3: Performance Breakdown
        with viz_tabs[2]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Scores by Parental Involvement")
                fig8 = self.visualizations.create_bar_chart_scores_by_involvement(filtered_df)
                st.pyplot(fig8)
            
            with col2:
                st.subheader("Scores by Parental Education")
                fig9 = self.visualizations.create_bar_chart_scores_by_education(filtered_df)
                st.pyplot(fig9)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Performance Box Plot")
                fig10 = self.visualizations.create_box_plot(
                    filtered_df, 'Parental_Involvement', 'Exam_Score',
                    'Exam Scores by Parental Involvement'
                )
                if fig10:
                    st.pyplot(fig10)
            
            with col2:
                st.subheader("Performance Violin Plot")
                fig11 = self.visualizations.create_violin_plot(
                    filtered_df, 'Performance_Category', 'Exam_Score',
                    'Score Distribution by Performance Category'
                )
                if fig11:
                    st.pyplot(fig11)
        
        # Tab 4: Advanced Analytics
        with viz_tabs[3]:
            st.subheader("Multi-Factor Analysis")
            fig12 = self.visualizations.create_multi_factor_chart(filtered_df)
            if fig12:
                st.pyplot(fig12)
                st.markdown("""
                **Comprehensive View:** This 4-panel chart shows the interplay between 
                key factors: parental involvement, attendance, study hours, and exam scores.
                """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Parental Involvement Heatmap")
                fig13 = self.visualizations.create_parental_involvement_heatmap(filtered_df)
                st.pyplot(fig13)
            
            with col2:
                st.subheader("Attendance Performance Heatmap")
                fig14 = self.visualizations.create_attendance_performance_heatmap(filtered_df)
                if fig14:
                    st.pyplot(fig14)

        # Recommendations Section
        st.header("💡 Actionable Recommendations")
        recommendations = self.analytics.generate_recommendations(filtered_df)
        
        rec_tabs = st.tabs(["👨‍👩‍👧 Parents", "👨‍🏫 Educators", "🏛️ Administrators", "👨‍🎓 Students"])
        
        with rec_tabs[0]:
            st.subheader("For Parents")
            if 'for_parents' in recommendations:
                for rec in recommendations['for_parents']:
                    priority = rec.get('priority', 'Medium')
                    icon = "🔴" if priority == 'Critical' or priority == 'High' else "🟡"
                    st.markdown(f"{icon} **{rec['action']}** ({priority} Priority)")
                    st.markdown(f"   {rec['description']}")
                    if 'expected_impact' in rec:
                        st.markdown(f"   *Expected Impact: {rec['expected_impact']}*")
                    st.markdown("")
            else:
                st.info("No specific recommendations at this time.")
        
        with rec_tabs[1]:
            st.subheader("For Educators")
            if 'for_educators' in recommendations:
                for rec in recommendations['for_educators']:
                    priority = rec.get('priority', 'Medium')
                    icon = "🔴" if priority == 'Critical' or priority == 'High' else "🟡"
                    st.markdown(f"{icon} **{rec['action']}** ({priority} Priority)")
                    st.markdown(f"   {rec['description']}")
                    if 'expected_impact' in rec:
                        st.markdown(f"   *Expected Impact: {rec['expected_impact']}*")
                    st.markdown("")
            else:
                st.info("No specific recommendations at this time.")
        
        with rec_tabs[2]:
            st.subheader("For Administrators")
            if 'for_administrators' in recommendations:
                for rec in recommendations['for_administrators']:
                    priority = rec.get('priority', 'Medium')
                    icon = "🔴" if priority == 'Critical' or priority == 'High' else "🟡"
                    st.markdown(f"{icon} **{rec['action']}** ({priority} Priority)")
                    st.markdown(f"   {rec['description']}")
                    if 'expected_impact' in rec:
                        st.markdown(f"   *Expected Impact: {rec['expected_impact']}*")
                    st.markdown("")
            else:
                st.info("No specific recommendations at this time.")
        
        with rec_tabs[3]:
            st.subheader("For Students")
            if 'for_students' in recommendations:
                for rec in recommendations['for_students']:
                    priority = rec.get('priority', 'Medium')
                    icon = "🔴" if priority == 'Critical' or priority == 'High' else "🟡"
                    st.markdown(f"{icon} **{rec['action']}** ({priority} Priority)")
                    st.markdown(f"   {rec['description']}")
                    if 'expected_impact' in rec:
                        st.markdown(f"   *Expected Impact: {rec['expected_impact']}*")
                    st.markdown("")
            else:
                st.info("No specific recommendations at this time.")

        # Download button
        st.header("📥 Export Data")
        st.download_button(
            label="Download Filtered Dataset (CSV)",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name='student_performance_export.csv',
            mime='text/csv',
        )

    def render_student_profiles_page(self, df):
        """Render the student profiles page"""
        st.header("👤 Individual Student Profiles")
        st.markdown("""
        Generate comprehensive, personalized reports for individual students including:
        - Performance analysis and peer comparison
        - Strengths and challenges identification
        - Personalized recommendations
        - 30/60/90 day action plan
        """)

        # Student selection
        if 'Student_ID' in df.columns:
            student_ids = sorted(df['Student_ID'].unique())
            selected_student = st.selectbox("Select Student ID:", student_ids)
        else:
            # Create synthetic IDs if not available
            df['Student_ID'] = range(1, len(df) + 1)
            student_ids = list(df['Student_ID'].unique())
            selected_student = st.selectbox("Select Student (Row Number):", student_ids)
        
        if st.button("Generate Comprehensive Profile", type="primary"):
            with st.spinner("Generating comprehensive student profile..."):
                # Generate the full report
                report = self.student_profile.generate_comprehensive_report(
                    df, selected_student
                )
                
                if report:
                    # Display report sections
                    st.success(f"✅ Profile generated for Student #{selected_student}")
                    
                    # Overview
                    st.subheader("📊 Performance Overview")
                    perf = report['performance']
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Exam Score", f"{perf['exam_score']:.1f}")
                    with col2:
                        st.metric("Letter Grade", perf['letter_grade'])
                    with col3:
                        st.metric("Class Percentile", f"{perf['percentile']:.0f}%")
                    with col4:
                        st.metric("Status", perf['performance_status'])
                    
                    # Strengths
                    st.subheader("💪 Strengths")
                    strengths = report['strengths']
                    for strength in strengths:
                        st.success(f"✓ {strength}")
                    
                    # Challenges
                    st.subheader("⚠️ Areas for Improvement")
                    challenges = report['challenges']
                    for challenge in challenges:
                        severity = challenge.get('severity', 'Medium')
                        icon = "🔴" if severity == "High" else "🟡" if severity == "Medium" else "🟢"
                        st.warning(f"{icon} **{challenge['area']}** ({severity} priority): {challenge['description']}")
                    
                    # Peer Comparison
                    st.subheader("👥 Peer Comparison")
                    peer = report['peer_comparison']
                    st.write(f"**Class Standing:** {peer['standing']}")
                    st.write(f"**Percentile Rank:** {peer['percentile']:.0f}th percentile")
                    st.write(f"**Score vs Class Average:** {peer['vs_average']:+.1f} points")
                    
                    # Recommendations
                    st.subheader("💡 Personalized Recommendations")
                    recommendations = report['recommendations']
                    for i, rec in enumerate(recommendations, 1):
                        with st.expander(f"{i}. {rec['category']} (Priority: {rec['priority']})"):
                            st.write(rec['recommendation'])
                            if 'action_steps' in rec:
                                st.write("**Action Steps:**")
                                for step in rec['action_steps']:
                                    st.write(f"- {step}")
                    
                    # Action Plan
                    st.subheader("📅 30/60/90 Day Action Plan")
                    action_plan = report['action_plan']
                    
                    plan_tabs = st.tabs(["30 Days", "60 Days", "90 Days"])
                    
                    with plan_tabs[0]:
                        st.write("**Focus:** " + action_plan['30_day']['focus'])
                        st.write("**Goals:**")
                        for goal in action_plan['30_day']['goals']:
                            st.write(f"- {goal}")
                    
                    with plan_tabs[1]:
                        st.write("**Focus:** " + action_plan['60_day']['focus'])
                        st.write("**Goals:**")
                        for goal in action_plan['60_day']['goals']:
                            st.write(f"- {goal}")
                    
                    with plan_tabs[2]:
                        st.write("**Focus:** " + action_plan['90_day']['focus'])
                        st.write("**Goals:**")
                        for goal in action_plan['90_day']['goals']:
                            st.write(f"- {goal}")
                    
                    # Printable Summary
                    st.subheader("📄 Printable Summary")
                    summary = self.student_profile.generate_printable_summary(df, selected_student)
                    st.text_area("Parent-Friendly Report (Copy & Share)", summary, height=300)
                    
                    # Download button
                    st.download_button(
                        label="Download Profile as Text",
                        data=summary,
                        file_name=f'student_{selected_student}_profile.txt',
                        mime='text/plain',
                    )
                else:
                    st.error(f"Could not generate profile for Student #{selected_student}")

    def render_goal_tracking_page(self, df):
        """Render the goal tracking page"""
        st.header("🎯 Student Goal Tracking")
        st.markdown("""
        Set academic goals, track progress over time, and monitor milestone achievements.
        """)

        # Student selection
        if 'Student_ID' in df.columns:
            student_ids = sorted(df['Student_ID'].unique())
        else:
            df['Student_ID'] = range(1, len(df) + 1)
            student_ids = list(df['Student_ID'].unique())
        
        selected_student = st.selectbox("Select Student:", student_ids, key="goal_student")

        # Action tabs
        goal_tabs = st.tabs(["📝 Create Goal", "📊 Track Progress", "📈 View Goals", "💡 Suggested Goals"])

        # Tab 1: Create Goal
        with goal_tabs[0]:
            st.subheader("Create New Goal")
            
            goal_type = st.selectbox("Goal Type:", [
                "Exam Score",
                "Attendance",
                "Study Hours",
                "Assignment Completion",
                "Behavior",
                "Custom"
            ])
            
            col1, col2 = st.columns(2)
            with col1:
                current_value = st.number_input("Current Value:", min_value=0.0, value=0.0, step=0.1)
            with col2:
                target_value = st.number_input("Target Value:", min_value=0.0, value=100.0, step=0.1)
            
            target_date = st.date_input("Target Date:")
            description = st.text_area("Goal Description (optional):")
            
            if st.button("Create Goal", type="primary"):
                goal_id = self.goal_tracker.create_goal(
                    student_id=selected_student,
                    goal_type=goal_type,
                    target_value=target_value,
                    current_value=current_value,
                    target_date=str(target_date),
                    description=description
                )
                st.success(f"✅ Goal created successfully! (ID: {goal_id})")

        # Tab 2: Track Progress
        with goal_tabs[1]:
            st.subheader("Update Goal Progress")
            
            # Get active goals for student
            active_goals = self.goal_tracker.get_student_goals(selected_student)
            
            if active_goals:
                goal_options = {
                    f"{g['goal_type']} - Target: {g['target_value']} (ID: {g['goal_id']})": g['goal_id']
                    for g in active_goals
                }
                
                selected_goal_label = st.selectbox("Select Goal to Update:", list(goal_options.keys()))
                selected_goal_id = goal_options[selected_goal_label]
                
                new_value = st.number_input("New Current Value:", min_value=0.0, value=0.0, step=0.1)
                notes = st.text_area("Progress Notes (optional):")
                
                if st.button("Update Progress", type="primary"):
                    self.goal_tracker.update_progress(
                        goal_id=selected_goal_id,
                        new_value=new_value,
                        notes=notes
                    )
                    st.success("✅ Progress updated successfully!")
                    
                    # Show updated status
                    status = self.goal_tracker.get_goal_status(selected_goal_id)
                    st.write(f"**Progress:** {status['progress_percentage']:.1f}%")
                    st.write(f"**Status:** {status['status']}")
            else:
                st.info("No active goals found. Create a goal first!")

        # Tab 3: View Goals
        with goal_tabs[2]:
            st.subheader("All Goals Overview")
            
            active_goals = self.goal_tracker.get_student_goals(selected_student)
            
            if active_goals:
                for goal in active_goals:
                    status = self.goal_tracker.get_goal_status(goal['goal_id'])
                    
                    with st.expander(f"{goal['goal_type']} - {status['progress_percentage']:.1f}% Complete"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Current", f"{status['current_value']:.1f}")
                        with col2:
                            st.metric("Target", f"{goal['target_value']:.1f}")
                        with col3:
                            st.metric("Progress", f"{status['progress_percentage']:.1f}%")
                        
                        st.progress(min(status['progress_percentage'] / 100, 1.0))
                        st.write(f"**Status:** {status['status']}")
                        st.write(f"**Target Date:** {goal['target_date']}")
                        
                        if goal.get('description'):
                            st.write(f"**Description:** {goal['description']}")
                        
                        # Show milestones
                        if 'milestones' in goal:
                            st.write("**Milestones:**")
                            for milestone in goal['milestones']:
                                icon = "✅" if milestone.get('achieved') else "⏳"
                                st.write(f"{icon} {milestone['name']}: {milestone['target_value']}")
                
                # Show progress chart
                if len(active_goals) > 0:
                    st.subheader("Progress Visualization")
                    # Use the goal tracker's visualization
                    fig = self.visualizations.create_progress_tracking_chart(
                        student_id=selected_student,
                        goals=active_goals
                    )
                    if fig:
                        st.pyplot(fig)
            else:
                st.info("No goals found for this student. Create your first goal!")

        # Tab 4: Suggested Goals
        with goal_tabs[3]:
            st.subheader("AI-Suggested Goals")
            st.markdown("Based on student data, here are recommended goals:")
            
            if st.button("Generate Goal Suggestions"):
                with st.spinner("Analyzing student data..."):
                    suggestions = self.goal_tracker.suggest_goals(df, selected_student)
                    
                    if suggestions:
                        for i, suggestion in enumerate(suggestions, 1):
                            with st.expander(f"{i}. {suggestion['goal_type']} Goal"):
                                st.write(f"**Recommended Target:** {suggestion['target_value']:.1f}")
                                st.write(f"**Current Value:** {suggestion['current_value']:.1f}")
                                st.write(f"**Reason:** {suggestion['reason']}")
                                st.write(f"**Priority:** {suggestion['priority']}")
                                
                                if st.button(f"Create This Goal", key=f"create_goal_{i}"):
                                    goal_id = self.goal_tracker.create_goal(
                                        student_id=selected_student,
                                        goal_type=suggestion['goal_type'],
                                        target_value=suggestion['target_value'],
                                        current_value=suggestion['current_value'],
                                        description=suggestion['reason']
                                    )
                                    st.success(f"✅ Goal created! (ID: {goal_id})")
                    else:
                        st.info("No specific goal suggestions at this time.")

    def render_ai_assistant_page(self, df):
        """Render the AI assistant chat interface"""
        st.header("💬 Educational AI Assistant")
        st.markdown("""
        Ask questions about the data, get insights, and receive educational guidance from our AI assistant.
        Powered by local Ollama for privacy and data security.
        """)
        
        # Render the chat interface
        self.ai_assistant.render_chat_interface(df)

    def clean_dataframe(self, df):
        """Clean dataframe for analysis"""
        df_clean = df.copy()
        for col in df_clean.columns:
            if pd.api.types.is_categorical_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].astype(str)
            if df_clean[col].dtype == 'object':
                try:
                    non_null_vals = df_clean[col].dropna()
                    if len(non_null_vals) > 0:
                        pd.to_numeric(non_null_vals.iloc[0])
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                except (ValueError, TypeError):
                    df_clean[col] = df_clean[col].astype(str)
        for col in df_clean.columns:
            if df_clean[col].dtype in ['float64', 'int64']:
                df_clean[col] = df_clean[col].fillna(0)
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
        return df_clean
