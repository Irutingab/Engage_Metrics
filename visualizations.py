import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualizations:
    @staticmethod
    def create_donut_chart(df, column, title, colors=None):
        value_counts = df[column].value_counts()
        if colors is None:
            colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))
        fig, ax = plt.subplots(figsize=(7, 7))  #figure sixe
        wedges, texts, autotexts = ax.pie(
            value_counts.values, labels=value_counts.index, colors=colors,
            autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.6)
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)  #text size
        ax.set_title(title, fontsize=11, fontweight='bold', pad=8)  # title size
        plt.tight_layout()
        return fig

    @staticmethod
    def create_histogram_chart(df, column, title, colors=None, bins=None):
        fig, ax = plt.subplots(figsize=(10, 6))
        if df[column].dtype == 'object' or pd.api.types.is_categorical_dtype(df[column]):
            value_counts = df[column].value_counts()
            bars = ax.bar(range(len(value_counts)), value_counts.values, 
                        color=colors[:len(value_counts)] if colors else None)
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_ylabel('Count')
            ax.set_xlabel(column)
            for bar, value in zip(bars, value_counts.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(value), ha='center', va='bottom', fontweight='bold')
        else:
            ax.hist(df[column].dropna(), bins=bins or 20, color='skyblue', alpha=0.7, edgecolor='black')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_correlation_heatmap(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return None
        
        corr_matrix = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(corr_matrix, aspect='auto', vmin=-1, vmax=1, cmap='RdBu_r')
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Correlation')
        
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr_matrix.columns)
        
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                       ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title('Correlation Matrix', fontsize=16, pad=20)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_bar_chart_scores_by_involvement(df):
        fig, ax = plt.subplots(figsize=(10, 6))
        
        involvement_order = ['Low', 'Medium', 'High']
        mean_scores = df.groupby('Parental_Involvement')['Exam_Score'].mean()
        mean_scores = mean_scores.reindex(involvement_order)
        
        bars = ax.bar(involvement_order, mean_scores, 
                    color=["#65D5A3", "#496445", "#12B02C"], edgecolor='black')
        
        for bar, value in zip(bars, mean_scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Scores by Parental Involvement', fontsize=16, fontweight='bold')
        ax.set_xlabel('Parental Involvement')
        ax.set_ylabel('Average Score')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_bar_chart_scores_by_education(df):
        """Create bar chart showing average scores by parental education and family income"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Bar chart by Parental Education Level
        if 'Parental_Education_Level' in df.columns:
            education_order = ['High School', 'College', 'Postgraduate']
            df_filtered = df[df['Parental_Education_Level'].isin(education_order)]
            
            mean_scores_education = df_filtered.groupby('Parental_Education_Level')['Exam_Score'].mean()
            mean_scores_education = mean_scores_education.reindex(education_order)
            
            colors = ["#99FFAF", "#439676", "#8BDDA7"]
            bars1 = ax1.bar(education_order, mean_scores_education, color=colors, edgecolor='black')
            
            # Add value labels on bars
            for bar, value in zip(bars1, mean_scores_education):
                if pd.notna(value):
                    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                            f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax1.set_title('Average Exam Scores by Parental Education Level', fontweight='bold')
            ax1.set_xlabel('Parental Education Level')
            ax1.set_ylabel('Average Exam Score')
            ax1.grid(True, alpha=0.3, axis='y')
        
        # Bar chart by Family Income
        if 'Family_Income' in df.columns:
            income_order = ['Low', 'Medium', 'High']
            df_filtered = df[df['Family_Income'].isin(income_order)]
            
            mean_scores_income = df_filtered.groupby('Family_Income')['Exam_Score'].mean()
            mean_scores_income = mean_scores_income.reindex(income_order)
            
            colors = ["#66FFD9", "#44946C", "#4CC09D"]
            bars2 = ax2.bar(income_order, mean_scores_income, color=colors, edgecolor='black')
            
            # Add value labels on bars
            for bar, value in zip(bars2, mean_scores_income):
                if pd.notna(value):
                    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                            f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            
            ax2.set_title('Average Exam Scores by Family Income Level', fontweight='bold')
            ax2.set_xlabel('Family Income Level')
            ax2.set_ylabel('Average Exam Score')
            ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_parental_involvement_heatmap(df):
        if 'Parental_Involvement' not in df.columns or 'Exam_Score' not in df.columns:
            return None
        
        df_temp = df.copy()
        df_temp['Score_Range'] = pd.cut(df_temp['Exam_Score'], 
                                       bins=[0, 60, 70, 80, 90, 100], 
                                       labels=['0-60', '60-70', '70-80', '80-90', '90-100'])
        
        heatmap_data = pd.crosstab(df_temp['Parental_Involvement'], df_temp['Score_Range'])
        
        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(heatmap_data.values, aspect='auto', cmap='YlOrRd')
        
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Students')
        
        ax.set_xticks(range(len(heatmap_data.columns)))
        ax.set_yticks(range(len(heatmap_data.index)))
        ax.set_xticklabels(heatmap_data.columns)
        ax.set_yticklabels(heatmap_data.index)
        
        for i in range(len(heatmap_data.index)):
            for j in range(len(heatmap_data.columns)):
                ax.text(j, i, heatmap_data.iloc[i, j], ha="center", va="center", 
                       color="black", fontweight='bold')
        
        ax.set_title('Parental Involvement vs Scores', fontsize=16, pad=20)
        ax.set_xlabel('Score Range')
        ax.set_ylabel('Parental Involvement')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_attendance_performance_heatmap(df):
        if 'Attendance_Category' not in df.columns or 'Performance_Category' not in df.columns:
            return None
        
        heatmap_data = pd.crosstab(df['Attendance_Category'], df['Performance_Category'])
        fig, ax = plt.subplots(figsize=(10, 6))
        
        im = ax.imshow(heatmap_data.values, cmap='Blues', aspect='auto')
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Students')
        
        ax.set_xticks(range(len(heatmap_data.columns)))
        ax.set_yticks(range(len(heatmap_data.index)))
        ax.set_xticklabels(heatmap_data.columns)
        ax.set_yticklabels(heatmap_data.index)
        
        for i in range(len(heatmap_data.index)):
            for j in range(len(heatmap_data.columns)):
                ax.text(j, i, heatmap_data.iloc[i, j], ha="center", va="center", 
                       color="white" if heatmap_data.iloc[i, j] > heatmap_data.values.max()/2 else "black", 
                       fontweight='bold')
        
        ax.set_title('Attendance vs Performance', fontsize=16, pad=20)
        ax.set_xlabel('Performance Category')
        ax.set_ylabel('Attendance Category')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_scatter_plot(df, x_col, y_col, color_by=None, title=None):
        """Create scatter plot with optional color coding"""
        fig, ax = plt.subplots(figsize=(10, 7))
        
        if color_by and color_by in df.columns:
            # Color-coded scatter
            categories = df[color_by].unique()
            colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
            
            for category, color in zip(categories, colors):
                mask = df[color_by] == category
                ax.scatter(df[mask][x_col], df[mask][y_col], 
                          label=category, alpha=0.6, s=50, color=color, edgecolors='black')
            
            ax.legend(title=color_by, loc='best')
        else:
            # Simple scatter
            ax.scatter(df[x_col], df[y_col], alpha=0.5, s=50, color='skyblue', edgecolors='black')
        
        # Add trend line
        if df[x_col].notna().sum() > 1 and df[y_col].notna().sum() > 1:
            z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
            p = np.poly1d(z)
            x_trend = np.linspace(df[x_col].min(), df[x_col].max(), 100)
            ax.plot(x_trend, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend')
            
            # Calculate and display correlation
            corr = df[[x_col, y_col]].corr().iloc[0, 1]
            ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                   transform=ax.transAxes, fontsize=11, verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        ax.set_xlabel(x_col, fontsize=12)
        ax.set_ylabel(y_col, fontsize=12)
        ax.set_title(title or f'{y_col} vs {x_col}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_box_plot(df, category_col, value_col, title=None):
        """Create box plot showing distribution across categories"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = df[category_col].unique()
        data_to_plot = [df[df[category_col] == cat][value_col].dropna() for cat in categories]
        
        bp = ax.boxplot(data_to_plot, labels=categories, patch_artist=True,
                        showmeans=True, meanline=True)
        
        # Color the boxes
        colors = plt.cm.Pastel1(np.linspace(0, 1, len(categories)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        # Styling
        for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], color='black')
        
        ax.set_xlabel(category_col, fontsize=12)
        ax.set_ylabel(value_col, fontsize=12)
        ax.set_title(title or f'{value_col} Distribution by {category_col}', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_violin_plot(df, category_col, value_col, title=None):
        """Create violin plot for detailed distribution analysis"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = sorted(df[category_col].unique())
        data_to_plot = [df[df[category_col] == cat][value_col].dropna().values for cat in categories]
        
        parts = ax.violinplot(data_to_plot, positions=range(len(categories)),
                             showmeans=True, showextrema=True, showmedians=True)
        
        # Color the violins
        colors = plt.cm.Set2(np.linspace(0, 1, len(categories)))
        for pc, color in zip(parts['bodies'], colors):
            pc.set_facecolor(color)
            pc.set_alpha(0.7)
        
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)
        ax.set_xlabel(category_col, fontsize=12)
        ax.set_ylabel(value_col, fontsize=12)
        ax.set_title(title or f'{value_col} Distribution by {category_col}', 
                    fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_multi_factor_chart(df):
        """Create comprehensive multi-factor analysis chart"""
        fig = plt.figure(figsize=(15, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # 1. Attendance vs Score scatter
        ax1 = fig.add_subplot(gs[0, 0])
        if 'Attendance' in df.columns and 'Exam_Score' in df.columns:
            ax1.scatter(df['Attendance'], df['Exam_Score'], alpha=0.5, s=30, color='steelblue')
            z = np.polyfit(df['Attendance'].dropna(), df['Exam_Score'].dropna(), 1)
            p = np.poly1d(z)
            x_trend = np.linspace(df['Attendance'].min(), df['Attendance'].max(), 100)
            ax1.plot(x_trend, p(x_trend), "r--", alpha=0.8)
            ax1.set_xlabel('Attendance %')
            ax1.set_ylabel('Exam Score')
            ax1.set_title('Attendance vs Performance')
            ax1.grid(True, alpha=0.3)
        
        # 2. Study Hours vs Score
        ax2 = fig.add_subplot(gs[0, 1])
        if 'Hours_Studied' in df.columns and 'Exam_Score' in df.columns:
            ax2.scatter(df['Hours_Studied'], df['Exam_Score'], alpha=0.5, s=30, color='coral')
            z = np.polyfit(df['Hours_Studied'].dropna(), df['Exam_Score'].dropna(), 1)
            p = np.poly1d(z)
            x_trend = np.linspace(df['Hours_Studied'].min(), df['Hours_Studied'].max(), 100)
            ax2.plot(x_trend, p(x_trend), "r--", alpha=0.8)
            ax2.set_xlabel('Hours Studied per Week')
            ax2.set_ylabel('Exam Score')
            ax2.set_title('Study Time vs Performance')
            ax2.grid(True, alpha=0.3)
        
        # 3. Parental Involvement Impact
        ax3 = fig.add_subplot(gs[1, 0])
        if 'Parental_Involvement' in df.columns and 'Exam_Score' in df.columns:
            involvement_order = ['Low', 'Medium', 'High']
            mean_scores = df.groupby('Parental_Involvement')['Exam_Score'].mean().reindex(involvement_order)
            bars = ax3.bar(involvement_order, mean_scores, color=['#ff9999', '#ffcc99', '#99ff99'])
            for bar, value in zip(bars, mean_scores):
                if pd.notna(value):
                    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                            f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
            ax3.set_xlabel('Parental Involvement')
            ax3.set_ylabel('Average Exam Score')
            ax3.set_title('Impact of Parental Involvement')
            ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. Performance Distribution
        ax4 = fig.add_subplot(gs[1, 1])
        if 'Exam_Score' in df.columns:
            ax4.hist(df['Exam_Score'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
            ax4.axvline(df['Exam_Score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["Exam_Score"].mean():.1f}')
            ax4.axvline(df['Exam_Score'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["Exam_Score"].median():.1f}')
            ax4.set_xlabel('Exam Score')
            ax4.set_ylabel('Frequency')
            ax4.set_title('Score Distribution')
            ax4.legend()
            ax4.grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('Comprehensive Performance Analysis', fontsize=16, fontweight='bold', y=0.995)
        return fig
    
    @staticmethod
    def create_factor_importance_chart(df):
        """Create chart showing importance of different factors"""
        if 'Exam_Score' not in df.columns:
            return None
        
        # Calculate correlations
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlations = []
        
        for col in numeric_cols:
            if col != 'Exam_Score' and df[col].notna().sum() > 0:
                corr = df[[col, 'Exam_Score']].corr().iloc[0, 1]
                if not np.isnan(corr):
                    correlations.append({'factor': col, 'correlation': abs(corr)})
        
        if not correlations:
            return None
        
        # Sort by importance
        correlations.sort(key=lambda x: x['correlation'], reverse=True)
        top_factors = correlations[:10]  # Top 10
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        factors = [f['factor'] for f in top_factors]
        values = [f['correlation'] for f in top_factors]
        
        colors = plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(factors)))
        bars = ax.barh(factors, values, color=colors, edgecolor='black')
        
        # Add value labels
        for bar, value in zip(bars, values):
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                   f'{value:.3f}', va='center', fontsize=10, fontweight='bold')
        
        ax.set_xlabel('Correlation with Exam Score (absolute value)', fontsize=12)
        ax.set_title('Top Factors Influencing Academic Performance', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 1)
        ax.grid(True, alpha=0.3, axis='x')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_progress_tracking_chart(baseline, current, target, metric_name="Exam Score"):
        """Create progress tracking visualization"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Baseline', 'Current', 'Target']
        values = [baseline, current, target]
        colors = ['#ff9999', '#ffcc99', '#99ff99']
        
        bars = ax.bar(categories, values, color=colors, edgecolor='black', width=0.6)
        
        # Add value labels
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                   f'{value:.1f}', ha='center', va='bottom', fontsize=14, fontweight='bold')
        
        # Add progress line
        ax.plot([0, 1], [baseline, current], 'b-', linewidth=3, marker='o', markersize=10, label='Progress')
        ax.plot([1, 2], [current, target], 'b--', linewidth=2, alpha=0.5, label='Goal')
        
        # Calculate progress percentage
        total_improvement_needed = target - baseline
        current_improvement = current - baseline
        progress_pct = (current_improvement / total_improvement_needed * 100) if total_improvement_needed != 0 else 0
        
        ax.text(0.5, 0.95, f'Progress: {progress_pct:.1f}% of goal achieved', 
               transform=ax.transAxes, fontsize=12, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
               ha='center', fontweight='bold')
        
        ax.set_ylabel(metric_name, fontsize=12)
        ax.set_title(f'{metric_name} Progress Tracking', fontsize=14, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_intervention_impact_chart(interventions_dict):
        """Visualize potential impact of different interventions"""
        if not interventions_dict:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        intervention_names = []
        current_scores = []
        projected_scores = []
        students_affected = []
        
        for name, data in interventions_dict.items():
            intervention_names.append(name.replace('_', ' ').title())
            current_scores.append(data['current_avg_score'])
            projected_scores.append(data['estimated_new_score'])
            students_affected.append(data['students_affected'])
        
        x = np.arange(len(intervention_names))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, current_scores, width, label='Current Avg Score', color='#ff9999')
        bars2 = ax.bar(x + width/2, projected_scores, width, label='Projected Score', color='#99ff99')
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=9)
        
        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Add students affected as text
        for i, count in enumerate(students_affected):
            ax.text(i, ax.get_ylim()[1] * 0.95, f'{count} students',
                   ha='center', fontsize=9, style='italic')
        
        ax.set_xlabel('Intervention Type', fontsize=12)
        ax.set_ylabel('Exam Score', fontsize=12)
        ax.set_title('Projected Impact of Interventions', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(intervention_names, rotation=15, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        return fig