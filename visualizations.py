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
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(
            value_counts.values,
            labels=value_counts.index,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops=dict(width=0.6)
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        return fig

    @staticmethod
    def create_histogram_chart(df, column, title, colors=None, bins=None):
        """Plots a histogram for numerical data or a bar chart for categorical data."""
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
            n, bins, patches = ax.hist(df[column].dropna(), bins=bins or 20, 
                                    color=colors[0] if colors else 'skyblue', 
                                    alpha=0.7, edgecolor='black')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_correlation_heatmap(df):
        """Plots a heatmap of the correlation matrix for all numeric columns."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return None
        
        corr_matrix = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(12, 8))
        
        im = ax.imshow(corr_matrix, aspect='auto', vmin=-1, vmax=1)
        
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Correlation Coefficient')
        
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr_matrix.columns)
        
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                text = ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                            ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title('Correlation Matrix: Student Performance Factors', fontsize=16, pad=20)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_bar_chart_scores_by_involvement(df):
        """Create bar chart showing average exam scores by parental involvement"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        involvement_order = ['Low', 'Medium', 'High']
        mean_scores = df.groupby('Parental_Involvement')['Exam_Score'].mean()
        mean_scores = mean_scores.reindex(involvement_order)
        
        bars = ax.bar(involvement_order, mean_scores, 
                    color=["#65D5A3", "#496445", "#12B02C"],
                    edgecolor='black', linewidth=1.2)
        
        for bar, value in zip(bars, mean_scores):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        
        ax.set_title('Average Exam Scores by Parental Involvement Level', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Parental Involvement Level', fontsize=12)
        ax.set_ylabel('Average Exam Score', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        ax.set_ylim(0, max(mean_scores) * 1.1)
                
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_box_plot_scores_by_education(df):
        """Create clear donut charts showing score distributions by demographics"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 14))
        
        # Create score categories
        df_temp = df.copy()
        df_temp['Score_Category'] = pd.cut(df_temp['Exam_Score'], 
                                         bins=[0, 60, 70, 80, 90, 100], 
                                         labels=['Poor (0-60)', 'Fair (60-70)', 'Good (70-80)', 'Very Good (80-90)', 'Excellent (90-100)'])
        
        # Education Level - High School
        hs_data = df_temp[df_temp['Parental_Education_Level'] == 'High School']['Score_Category'].value_counts()
        colors_hs = ["#008B48", "#99FF00", "#FFD700", "#32CD32", "#006400"]
        
        if not hs_data.empty:
            wedges1, texts1, autotexts1 = ax1.pie(hs_data.values, labels=None,
                                                 colors=colors_hs[:len(hs_data)],
                                                 autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                                                 startangle=90,
                                                 wedgeprops=dict(width=0.6),
                                                 pctdistance=0.85)
            for autotext in autotexts1:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add legend instead of labels on pie
            ax1.legend(wedges1, [f'{label}: {val}' for label, val in zip(hs_data.index, hs_data.values)], 
                      loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        
        ax1.set_title('High School Education\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        # Education Level - College
        college_data = df_temp[df_temp['Parental_Education_Level'] == 'College']['Score_Category'].value_counts()
        
        if not college_data.empty:
            wedges2, texts2, autotexts2 = ax2.pie(college_data.values, labels=None,
                                                 colors=colors_hs[:len(college_data)],
                                                 autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                                                 startangle=90,
                                                 wedgeprops=dict(width=0.6),
                                                 pctdistance=0.85)
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add legend instead of labels on pie
            ax2.legend(wedges2, [f'{label}: {val}' for label, val in zip(college_data.index, college_data.values)], 
                      loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        
        ax2.set_title('College Education\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        # Income Level - Low
        low_income_data = df_temp[df_temp['Family_Income'] == 'Low']['Score_Category'].value_counts()
        colors_income = ["#549B63", "#1F642B", "#70DBC9", "#049D46", "#98E898"]
        
        if not low_income_data.empty:
            wedges3, texts3, autotexts3 = ax3.pie(low_income_data.values, labels=None,
                                                 colors=colors_income[:len(low_income_data)],
                                                 autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                                                 startangle=90,
                                                 wedgeprops=dict(width=0.6),
                                                 pctdistance=0.85)
            for autotext in autotexts3:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add legend instead of labels on pie
            ax3.legend(wedges3, [f'{label}: {val}' for label, val in zip(low_income_data.index, low_income_data.values)], 
                      loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        
        ax3.set_title('Low Income\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        # Income Level - High
        high_income_data = df_temp[df_temp['Family_Income'] == 'High']['Score_Category'].value_counts()
        
        if not high_income_data.empty:
            wedges4, texts4, autotexts4 = ax4.pie(high_income_data.values, labels=None,
                                                 colors=colors_income[:len(high_income_data)],
                                                 autopct=lambda pct: f'{pct:.1f}%' if pct > 5 else '',
                                                 startangle=90,
                                                 wedgeprops=dict(width=0.6),
                                                 pctdistance=0.85)
            for autotext in autotexts4:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)
            
            # Add legend instead of labels on pie
            ax4.legend(wedges4, [f'{label}: {val}' for label, val in zip(high_income_data.index, high_income_data.values)], 
                      loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)
        
        ax4.set_title('High Income\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        plt.suptitle('Score Distribution by Demographics', fontsize=18, fontweight='bold', y=0.95)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        return fig
    
    @staticmethod

    def create_parental_involvement_heatmap(df):
        """Create a focused heatmap showing the relationship between parental involvement and student performance metrics."""
        # Create score bins for better visualization
        df_copy = df.copy()
        
        # Create score ranges
        score_bins = [0, 60, 70, 80, 90, 100]
        score_labels = ['Below 60', '60-69', '70-79', '80-89', '90-100']
        df_copy['Score_Range'] = pd.cut(df_copy['Exam_Score'], bins=score_bins, labels=score_labels, include_lowest=True)
        
        # Create pivot table for heatmap
        heatmap_data = pd.crosstab(df_copy['Parental_Involvement'], df_copy['Score_Range'], normalize='index') * 100
        
        # Ensure proper order
        involvement_order = ['Low', 'Medium', 'High']
        heatmap_data = heatmap_data.reindex(involvement_order)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create heatmap
        im = ax.imshow(heatmap_data.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Percentage of Students (%)', rotation=270, labelpad=20)
        
        # Set ticks and labels
        ax.set_xticks(range(len(heatmap_data.columns)))
        ax.set_yticks(range(len(heatmap_data.index)))
        ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right')
        ax.set_yticklabels(heatmap_data.index)
        
        # Add percentage text in cells
        for i in range(len(heatmap_data.index)):
            for j in range(len(heatmap_data.columns)):
                value = heatmap_data.iloc[i, j]
                text_color = 'white' if value < 50 else 'black'
                ax.text(j, i, f'{value:.1f}%', ha="center", va="center", 
                       color=text_color, fontweight='bold', fontsize=10)
        
        ax.set_title('Parental Involvement vs Student Score Distribution', fontsize=16, pad=20)
        ax.set_xlabel('Exam Score Ranges', fontsize=10)
        ax.set_ylabel('Parental Involvement Level', fontsize=12)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_engagement_correlation_heatmap(df):
        """Create correlation heatmap focused on engagement factors"""
        engagement_cols = ['Parental_Engagement_Score', 'Involvement_Score', 'Education_Score', 
                          'Income_Score', 'Exam_Score', 'Attendance', 'Hours_Studied']
        
        # Select only engagement-related columns
        engagement_df = df[engagement_cols].select_dtypes(include=[np.number])
        corr_matrix = engagement_df.corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create heatmap
        im = ax.imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Correlation Coefficient', rotation=270, labelpad=20)
        
        # Set ticks and labels
        ax.set_xticks(range(len(corr_matrix.columns)))
        ax.set_yticks(range(len(corr_matrix.columns)))
        ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
        ax.set_yticklabels(corr_matrix.columns)
        
        # Add correlation values in cells
        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                value = corr_matrix.iloc[i, j]
                text_color = 'white' if abs(value) > 0.5 else 'black'
                ax.text(j, i, f'{value:.3f}', ha="center", va="center", 
                       color=text_color, fontweight='bold', fontsize=10)
        
        ax.set_title('Parental Engagement Factors Correlation Matrix', fontsize=16, pad=20)
        plt.tight_layout()
        return fig
