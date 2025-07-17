import streamlit as st
import pandas as pd
import numpy as np
from data_manager import DataManager
from visualizations import Visualizations
from analytics import Analytics

class StudentDashboard:

    def __init__(self):
        self.data_manager = DataManager()
        self.visualizations = Visualizations()
        self.analytics = Analytics()
        self.setup_page_config()
        self.load_custom_css()
    
    def setup_page_config(self):
        """Configure Streamlit page settings"""
        st.set_page_config(
            page_title="Student Performance & Parental Engagement Dashboard",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    def load_custom_css(self):
        """Load custom CSS styling"""
        st.markdown("""
        <style>
            .main > div {
                padding: 2rem 1rem;
            }
            .metric-card {
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 0.5rem;
                border-left: 4px solid #1f77b4;
            }
            .correlation-strong { color: #28a745; font-weight: bold; }
            .correlation-moderate { color: #ffc107; font-weight: bold; }
            .correlation-weak { color: #dc3545; font-weight: bold; }
        </style>
        """, unsafe_allow_html=True)
    
    def clean_dataframe_for_streamlit(self, df):
        """Clean dataframe to ensure Arrow compatibility"""
        df_clean = df.copy()
        
        # Convert all categorical columns to strings to avoid Arrow issues
        for col in df_clean.columns:
            if pd.api.types.is_categorical_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].astype(str)
        
        # Handle mixed data types that cause Arrow issues
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                try:
                    # Check if all non-null values can be converted to numeric
                    non_null_vals = df_clean[col].dropna()
                    if len(non_null_vals) > 0:
                        # Test conversion on a sample
                        pd.to_numeric(non_null_vals.iloc[0])
                        # If successful, convert the entire column
                        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                except (ValueError, TypeError):
                    # Keep as string if conversion fails
                    df_clean[col] = df_clean[col].astype(str)
        
        # Fill any remaining NaN values
        for col in df_clean.columns:
            if df_clean[col].dtype in ['float64', 'int64']:
                df_clean[col] = df_clean[col].fillna(0)
            else:
                df_clean[col] = df_clean[col].fillna('Unknown')
        
        return df_clean
    
    def render_sidebar(self, df):
        """Render sidebar filters and return filtered data"""
        st.sidebar.header("Dashboard Filters")
        
        # Ensure data is clean before filtering
        df = self.clean_dataframe_for_streamlit(df)
        
        # Parental involvement filter
        involvement_options = df['Parental_Involvement'].unique()
        selected_involvement = st.sidebar.multiselect(
            "Select Parental Involvement Levels",
            options=involvement_options,
            default=involvement_options
        )
        
        # Apply filters and clean the result
        filtered_df = self.data_manager.apply_filters(df, selected_involvement)
        return self.clean_dataframe_for_streamlit(filtered_df)
    
    def render_executive_summary(self, filtered_df):
    
        st.header("Executive Summary")
        
        # Ensure data is clean before analytics
        filtered_df = self.clean_dataframe_for_streamlit(filtered_df)
        insights = self.analytics.get_performance_insights(filtered_df)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Students", f"{insights['total_students']:,}")
        with col2:
            st.metric("Average Exam Score", f"{insights['avg_score']:.1f}")
        with col3:
            st.metric("Average Attendance", f"{insights['avg_attendance']:.1f}%")
        with col4:
            st.metric("High Performers (>70)", f"{insights['high_performers_pct']:.1f}%")
    
    def render_distribution_charts(self, filtered_df):
        """Render engagement and performance distribution charts"""
        st.header("Engagement & Performance Distribution")
        
        # Clean data before visualization
        filtered_df = self.clean_dataframe_for_streamlit(filtered_df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                donut_involvement = self.visualizations.create_donut_chart(
                    filtered_df, 'Parental_Involvement', 
                    'Parental Involvement Distribution',
                    colors=["#16AB31", "#198C8C", "#158C4D"]
                )
                st.pyplot(donut_involvement)
            except Exception as e:
                st.error(f"Error creating involvement chart: {str(e)}")
        
        with col2:
            try:
                histogram_performance = self.visualizations.create_histogram_chart(
                    filtered_df, 'Performance_Category', 
                    'Academic Performance Distribution',
                    colors=["#0CBA6F", "#1C8E8E", "#249976", "#48A962", "#329B51"]
                )
                st.pyplot(histogram_performance)
            except Exception as e:
                st.error(f"Error creating performance chart: {str(e)}")
        
        # Second row
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                donut_attendance = self.visualizations.create_donut_chart(
                    filtered_df, 'Attendance_Category', 
                    'Attendance Level Distribution',
                    colors=["#2F8E87", "#42C85F", "#167679"]
                )
                st.pyplot(donut_attendance)
            except Exception as e:
                st.error(f"Error creating attendance chart: {str(e)}")
        
        with col2:
            try:
                donut_study = self.visualizations.create_donut_chart(
                    filtered_df, 'Study_Hours_Category', 
                    'Study Hours Distribution',
                    colors=["#0F8F76", "#36CF4F", "#5DD495"]
                )
                st.pyplot(donut_study)
            except Exception as e:
                st.error(f"Error creating stustredy hours chart: {str(e)}")
    
    def render_performance_analysis(self, filtered_df):
        """Render performance distribution and advanced analysis"""
        st.header("Performance Distribution Analysis")
        
        # Clean data before analysis
        filtered_df = self.clean_dataframe_for_streamlit(filtered_df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                hist_scores = self.visualizations.create_histogram_with_kde(
                    filtered_df, 'Exam_Score', 'Distribution of Exam Scores'
                )
                st.pyplot(hist_scores)
            except Exception as e:
                st.error(f"Error creating exam score histogram: {str(e)}")
        
        with col2:
            try:
                hist_hours = self.visualizations.create_histogram_with_kde(
                    filtered_df, 'Hours_Studied', 'Distribution of Study Hours'
                )
                st.pyplot(hist_hours)
            except Exception as e:
                st.error(f"Error creating study hours histogram: {str(e)}")
        
        # Advanced Analysis
        st.header("Advanced Performance Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                bar_chart = self.visualizations.create_bar_chart_scores_by_involvement(filtered_df)
                st.pyplot(bar_chart)
            except Exception as e:
                st.error(f"Error creating bar chart: {str(e)}")
        
        with col2:
            try:
                scatter_plot = self.visualizations.create_scatter_attendance_vs_scores(filtered_df)
                st.pyplot(scatter_plot)
            except Exception as e:
                st.error(f"Error creating scatter plot: {str(e)}")
        
        # Box plots
        st.subheader("Score Distribution by Demographics")
        try:
            box_plots = self.visualizations.create_box_plot_scores_by_education(filtered_df)
            st.pyplot(box_plots)
        except Exception as e:
            st.error(f"Error creating box plots: {str(e)}")
    
    def render_correlation_analysis(self, filtered_df):
        """Render correlation analysis section"""
        st.header("Correlation Analysis")
        
        # Clean data before correlation analysis
        filtered_df = self.clean_dataframe_for_streamlit(filtered_df)
        try:
            corr_fig = self.visualizations.create_correlation_heatmap(filtered_df)
            
            if corr_fig:
                st.pyplot(corr_fig)
                
                # Correlation insights
                correlation_data = self.analytics.get_correlation_insights(filtered_df)
                if correlation_data:
                    st.subheader("Key Correlations with Exam Performance")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Strongest Positive Factors:**")
                        for item in correlation_data:
                            st.write(f"• {item['factor']}: {item['correlation']:.3f} ({item['strength']})")
                    
                    with col2:
                        involvement_stats = filtered_df.groupby('Parental_Involvement')['Exam_Score'].agg(['mean', 'count']).round(2)
                        st.write("**Performance by Parental Involvement:**")
                        st.dataframe(involvement_stats)
        except Exception as e:
            st.error(f"Error in correlation analysis: {str(e)}")
    
    def render_parental_engagement_analysis(self, filtered_df):
        """Render comprehensive parental engagement analysis section"""
        st.header("🧑‍🏫 Parental Engagement Analysis")
        
        # Clean data before analysis
        filtered_df = self.clean_dataframe_for_streamlit(filtered_df)
        
        # Engagement Score Distribution
        st.subheader("Engagement Score Distribution")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                engagement_dist = self.visualizations.create_engagement_score_distribution(filtered_df)
                st.pyplot(engagement_dist)
            except Exception as e:
                st.error(f"Error creating engagement distribution: {str(e)}")
        
        with col2:
            try:
                engagement_insights = self.analytics.get_engagement_insights(filtered_df)
                st.metric("Average Engagement Score", f"{engagement_insights['avg_engagement_score']:.2f}")
                st.metric("Median Engagement Score", f"{engagement_insights['median_engagement_score']:.2f}")
                
                # Show distribution
                if 'engagement_distribution' in engagement_insights:
                    st.write("**Engagement Distribution:**")
                    for category, percentage in engagement_insights['engagement_distribution'].items():
                        st.write(f"• {category}: {percentage:.1f}%")
            except Exception as e:
                st.error(f"Error getting engagement insights: {str(e)}")
        
        # Engagement vs Performance Analysis
        st.subheader("📈 Performance vs. Engagement")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                scatter_plot = self.visualizations.create_engagement_score_scatter(filtered_df)
                st.pyplot(scatter_plot)
            except Exception as e:
                st.error(f"Error creating engagement scatter plot: {str(e)}")
        
        with col2:
            try:
                boxplot = self.visualizations.create_performance_vs_engagement_boxplot(filtered_df)
                st.pyplot(boxplot)
            except Exception as e:
                st.error(f"Error creating engagement boxplot: {str(e)}")
        
        # Education Level Analysis
        st.subheader("Engagement by Parental Education Level")
        try:
            education_chart = self.visualizations.create_engagement_by_education_level(filtered_df)
            st.pyplot(education_chart)
            
            st.markdown("""
            **Understanding the Chart:**
            - Shows how parental involvement varies by education level
            - Higher education levels tend to show more involvement
            - Helps identify intervention opportunities
            """)
        except Exception as e:
            st.error(f"Error creating education level chart: {str(e)}")
        
        # Engagement Correlations
        st.subheader("🔍 Engagement Factor Correlations")
        try:
            correlation_heatmap = self.visualizations.create_engagement_correlation_heatmap(filtered_df)
            st.pyplot(correlation_heatmap)
            
            # Show correlation insights
            engagement_insights = self.analytics.get_engagement_insights(filtered_df)
            if 'engagement_correlations' in engagement_insights:
                st.write("**Key Correlations with Exam Performance:**")
                correlations = engagement_insights['engagement_correlations']
                for factor, corr in correlations.items():
                    if factor != 'Exam_Score':
                        strength = "Strong" if abs(corr) > 0.5 else "Moderate" if abs(corr) > 0.3 else "Weak"
                        st.write(f"• {factor}: {corr:.3f} ({strength})")
        except Exception as e:
            st.error(f"Error in engagement correlations: {str(e)}")
    
    def render_actionable_insights(self, filtered_df):
        """Render actionable insights and recommendations based on engagement analysis"""
        st.header("💡 Actionable Insights & Recommendations")
        
        # Clean data before analysis
        filtered_df = self.clean_dataframe_for_streamlit(filtered_df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Key Findings")
            try:
                impact_analysis = self.analytics.analyze_engagement_factors_impact(filtered_df)
                
                st.write("**Impact of Engagement Factors:**")
                for factor, analysis in impact_analysis.items():
                    st.write(f"**{factor.replace('_', ' ')}:**")
                    st.write(f"• Correlation with performance: {analysis['correlation']:.3f}")
                    st.write(f"• Performance gap: {analysis['effect_size']:.1f} points")
                    
                    # Show mean scores by category
                    st.write("• Average scores by level:")
                    for level, score in analysis['mean_scores_by_category'].items():
                        st.write(f"  - {level}: {score:.1f}")
                    st.write("")
            except Exception as e:
                st.error(f"Error in impact analysis: {str(e)}")
        
        with col2:
            st.subheader("🎯 Comprehensive Recommendations")
            try:
                recommendations = self.analytics.get_engagement_recommendations(filtered_df)
                
                for i, rec in enumerate(recommendations, 1):
                    priority_color = "🔴" if rec['priority'] == 'High' else "🟡" if rec['priority'] == 'Medium' else "🟢"
                    
                    # Create expandable recommendation sections
                    with st.expander(f"{priority_color} {rec['priority']} Priority: {rec['area']}", expanded=(rec['priority'] == 'High')):
                        st.markdown(f"""
                        **📊 Finding:** {rec['recommendation']}
                        
                        **💡 Expected Impact:** {rec['expected_impact']}
                        """)
                        
                        # Show specific actions if available
                        if 'specific_actions' in rec:
                            st.markdown("**🔧 Specific Actions to Take:**")
                            for action in rec['specific_actions']:
                                st.markdown(f"• {action}")
                        
                        st.write("")
                
                if not recommendations:
                    st.info("No specific recommendations generated - current engagement levels appear optimal!")
                    
            except Exception as e:
                st.error(f"Error generating recommendations: {str(e)}")
        
        # Display detailed recommendations
        st.subheader("📋 Detailed Action Plan")
        
        for i, rec in enumerate(recommendations, 1):
            priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}[rec['priority']]
            
            with st.expander(f"{priority_color} {rec['area']} (Priority: {rec['priority']})"):
                st.write(f"**Recommendation:** {rec['recommendation']}")
                st.write(f"**Expected Impact:** {rec['expected_impact']}")
                
                st.write("**Specific Actions:**")
                for action in rec['specific_actions']:
                    st.write(f"• {action}")
    
    def render_implementation_timeline(self, df):
        """Render implementation timeline"""
        st.subheader("📅 Implementation Timeline")
        
        timeline = self.analytics.get_implementation_timeline(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Immediate Actions (0-30 days)")
            for item in timeline['immediate']:
                st.info(f"🔴 **{item['action']}**\n{item['description']}")
            
            st.write("### Short-term Goals (1-3 months)")
            for item in timeline['short_term']:
                st.warning(f"🟡 **{item['action']}**\n{item['description']}")
        
        with col2:
            st.write("### Medium-term Projects (3-6 months)")
            for item in timeline['medium_term']:
                st.success(f"🟢 **{item['action']}**\n{item['description']}")
            
            st.write("### Long-term Initiatives (6+ months)")
            for item in timeline['long_term']:
                st.info(f"🔵 **{item['action']}**\n{item['description']}")
    
    def render_success_metrics(self, df):
        """Render success metrics and KPI tracking"""
        st.subheader("📊 Success Metrics & KPI Tracking")
        
        metrics = self.analytics.get_success_metrics(df)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Current Performance")
            st.metric("Average Exam Score", f"{metrics['current']['avg_exam_score']:.1f}")
            st.metric("High Performers (%)", f"{metrics['current']['high_performers_pct']:.1f}%")
            st.metric("Low Engagement (%)", f"{metrics['current']['low_engagement_pct']:.1f}%")
            st.metric("Attendance Rate (%)", f"{metrics['current']['attendance_rate']:.1f}%")
            st.metric("High Parental Involvement (%)", f"{metrics['current']['high_involvement_pct']:.1f}%")
        
        with col2:
            st.write("### Target Metrics")
            st.metric("Target Avg Score", f"{metrics['targets']['target_avg_score']:.1f}", 
                     delta=f"+{metrics['targets']['target_avg_score'] - metrics['current']['avg_exam_score']:.1f}")
            st.metric("Target High Performers", f"{metrics['targets']['target_high_performers']:.1f}%", 
                     delta=f"+{metrics['targets']['target_high_performers'] - metrics['current']['high_performers_pct']:.1f}%")
            st.metric("Target Low Engagement", f"{metrics['targets']['target_low_engagement']:.1f}%", 
                     delta=f"{metrics['targets']['target_low_engagement'] - metrics['current']['low_engagement_pct']:.1f}%")
            st.metric("Target Attendance", f"{metrics['targets']['target_attendance']:.1f}%", 
                     delta=f"+{metrics['targets']['target_attendance'] - metrics['current']['attendance_rate']:.1f}%")
            st.metric("Target Involvement", f"{metrics['targets']['target_involvement']:.1f}%", 
                     delta=f"+{metrics['targets']['target_involvement'] - metrics['current']['high_involvement_pct']:.1f}%")
        
        st.write("### Key Performance Indicators to Track")
        for kpi in metrics['tracking_kpis']:
            st.write(f"• {kpi}")

    def run(self):
        """Main method to run the dashboard"""
        try:
            # Load data
            df = self.data_manager.get_processed_data()
            if df is None:
                st.error("Failed to load data. Please check your data file.")
                return
            
            # Clean data immediately after loading
            df = self.clean_dataframe_for_streamlit(df)
            
            # Title and description
            st.title("The power of parental involvement in student performance")
            st.markdown("""
            This dashboard analyzes the relationship between parental involvement and student performance using 
            professional visualizations including donut charts, pie charts, and histograms to provide clear insights
            for educational decision-making.
            """)
            
            # Apply filters
            filtered_df = self.render_sidebar(df)
            
            # Render all sections with error handling
            try:
                self.render_executive_summary(filtered_df)
            except Exception as e:
                st.error(f"Error in executive summary: {str(e)}")
            
            try:
                self.render_distribution_charts(filtered_df)
            except Exception as e:
                st.error(f"Error in distribution charts: {str(e)}")
            
            try:
                self.render_performance_analysis(filtered_df)
            except Exception as e:
                st.error(f"Error in performance analysis: {str(e)}")
            
            try:
                self.render_correlation_analysis(filtered_df)
            except Exception as e:
                st.error(f"Error in correlation analysis: {str(e)}")
            
            try:
                self.render_parental_engagement_analysis(filtered_df)
            except Exception as e:
                st.error(f"Error in parental engagement analysis: {str(e)}")
            
            try:
                self.render_actionable_insights(filtered_df)
            except Exception as e:
                st.error(f"Error in actionable insights: {str(e)}")
            
            try:
                self.render_export_section(filtered_df)
            except Exception as e:
                st.error(f"Error in export section: {str(e)}")
                
        except Exception as e:
            st.error(f"Critical error in dashboard: {str(e)}")
            st.write("Please check your data and try again.")
