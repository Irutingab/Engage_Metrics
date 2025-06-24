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
            # For categorical data, create a bar chart
            value_counts = df[column].value_counts()
            bars = ax.bar(range(len(value_counts)), value_counts.values, 
                        color=colors[:len(value_counts)] if colors else None)
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_ylabel('Count')
            ax.set_xlabel(column)
            # Add value labels on bars
            for bar, value in zip(bars, value_counts.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    str(value), ha='center', va='bottom', fontweight='bold')
        else:
            # For numerical data, create a histogram
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
    def create_histogram_with_kde(df, column, title, bins=20):
        """Plots a histogram for a numerical column 
        and overlays a vertical line for the mean."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        n, bins, patches = ax.hist(df[column].dropna(), bins=bins, alpha=0.7, 
                                color='skyblue', edgecolor='black')
        
        mean_val = df[column].mean()
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                label=f'Mean: {mean_val:.1f}')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        ax.legend()
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
                    color=["#0D056A", "#484564", "#090D4F"],
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
    def create_scatter_attendance_vs_scores(df):
        """Create scatter plot of Attendance vs Exam_Score colored by Parental_Involvement"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        colors = {'Low': "#25203A", 'Medium': "#3E0EE9", 'High': "#1E1276"}
        
        for involvement in ['Low', 'Medium', 'High']:
            subset = df[df['Parental_Involvement'] == involvement]
            ax.scatter(subset['Attendance'], subset['Exam_Score'], 
                    c=colors[involvement], label=f'{involvement} Involvement',
                    alpha=0.7, s=50, edgecolors='black', linewidth=0.5)
        
        z = np.polyfit(df['Attendance'], df['Exam_Score'], 1)
        p = np.poly1d(z)
        ax.plot(df['Attendance'], p(df['Attendance']), "r--", alpha=0.8, linewidth=2, label='Trend Line')
        
        ax.set_title('Attendance vs Exam Score (by Parental Involvement)', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Attendance (%)', fontsize=12)
        ax.set_ylabel('Exam Score', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_box_plot_scores_by_education(df):
        """Create clear donut charts showing score distributions by demographics"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        # Create score categories
        df_temp = df.copy()
        df_temp['Score_Category'] = pd.cut(df_temp['Exam_Score'], 
                                         bins=[0, 60, 70, 80, 90, 100], 
                                         labels=['Poor (0-60)', 'Fair (60-70)', 'Good (70-80)', 'Very Good (80-90)', 'Excellent (90-100)'])
        
        # Education Level - High School
        hs_data = df_temp[df_temp['Parental_Education_Level'] == 'High School']['Score_Category'].value_counts()
        colors_hs = ["#8B0000", "#FF4500", "#FFD700", "#32CD32", "#006400"]
        
        if not hs_data.empty:
            wedges1, texts1, autotexts1 = ax1.pie(hs_data.values, labels=hs_data.index,
                                                 colors=colors_hs[:len(hs_data)],
                                                 autopct='%1.1f%%', startangle=90,
                                                 wedgeprops=dict(width=0.6))
            for autotext in autotexts1:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        
        ax1.set_title('High School Education\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        # Education Level - College
        college_data = df_temp[df_temp['Parental_Education_Level'] == 'College']['Score_Category'].value_counts()
        
        if not college_data.empty:
            wedges2, texts2, autotexts2 = ax2.pie(college_data.values, labels=college_data.index,
                                                 colors=colors_hs[:len(college_data)],
                                                 autopct='%1.1f%%', startangle=90,
                                                 wedgeprops=dict(width=0.6))
            for autotext in autotexts2:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        
        ax2.set_title('College Education\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        # Income Level - Low
        low_income_data = df_temp[df_temp['Family_Income'] == 'Low']['Score_Category'].value_counts()
        colors_income = ["#4B0082", "#8A2BE2", "#9370DB", "#BA55D3", "#DA70D6"]
        
        if not low_income_data.empty:
            wedges3, texts3, autotexts3 = ax3.pie(low_income_data.values, labels=low_income_data.index,
                                                 colors=colors_income[:len(low_income_data)],
                                                 autopct='%1.1f%%', startangle=90,
                                                 wedgeprops=dict(width=0.6))
            for autotext in autotexts3:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        
        ax3.set_title('Low Income\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        # Income Level - High
        high_income_data = df_temp[df_temp['Family_Income'] == 'High']['Score_Category'].value_counts()
        
        if not high_income_data.empty:
            wedges4, texts4, autotexts4 = ax4.pie(high_income_data.values, labels=high_income_data.index,
                                                 colors=colors_income[:len(high_income_data)],
                                                 autopct='%1.1f%%', startangle=90,
                                                 wedgeprops=dict(width=0.6))
            for autotext in autotexts4:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        
        ax4.set_title('High Income\nScore Distribution', fontsize=12, fontweight='bold', pad=20)
        
        plt.suptitle('Score Distribution by Demographics', fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        return fig
    
    @staticmethod
    def create_parental_involvement_analysis(df):
        """Create detailed analysis of parental involvement impact"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        involvement_order = ['Low', 'Medium', 'High']
        df_ordered = df[df['Parental_Involvement'].isin(involvement_order)]
        
        box_data = [df_ordered[df_ordered['Parental_Involvement'] == level]['Exam_Score'].values 
                    for level in involvement_order]
        
        ax1.boxplot(box_data, labels=involvement_order)
        ax1.set_title('Exam Scores by Parental Involvement Level', fontweight='bold')
        ax1.set_xlabel('Parental Involvement Level')
        ax1.set_ylabel('Exam Score')
        ax1.grid(True, alpha=0.3)
        
        mean_scores = df.groupby('Parental_Involvement')['Exam_Score'].mean().reindex(involvement_order)
        bars = ax2.bar(involvement_order, mean_scores, color=["#12042B", "#9A99AA", "#060673"])
        ax2.set_title('Average Exam Scores by Parental Involvement', fontweight='bold')
        ax2.set_xlabel('Parental Involvement Level')
        ax2.set_ylabel('Average Exam Score')
        
        for bar, value in zip(bars, mean_scores):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                    f'{value:.1f}', ha='center', va='bottom', fontweight='bold')
        
        performance_by_involvement = pd.crosstab(df['Parental_Involvement'], df['Performance_Category'], normalize='index') * 100
        performance_by_involvement.plot(kind='bar', ax=ax3, stacked=True, 
                                    color=["#05000B", "#0F06BC", "#84838A", "#4E4D56", "#2D04B4"])
        ax3.set_title('Performance Distribution by Parental Involvement (%)', fontweight='bold')
        ax3.set_xlabel('Parental Involvement Level')
        ax3.set_ylabel('Percentage')
        ax3.legend(title='Performance Grade', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.tick_params(axis='x', rotation=45)
        
        involvement_numeric = df['Parental_Involvement'].map({'Low': 1, 'Medium': 2, 'High': 3})
        ax4.scatter(involvement_numeric, df['Exam_Score'], alpha=0.6, color="#116274")
        
        z = np.polyfit(involvement_numeric, df['Exam_Score'], 1)
        p = np.poly1d(z)
        ax4.plot([1, 2, 3], p([1, 2, 3]), "r--", alpha=0.8, linewidth=2)
        
        ax4.set_title('Exam Score vs Parental Involvement (with trend)', fontweight='bold')
        ax4.set_xlabel('Parental Involvement Level\n(1=Low, 2=Medium, 3=High)')
        ax4.set_ylabel('Exam Score')
        ax4.set_xticks([1, 2, 3])
        ax4.set_xticklabels(['Low', 'Medium', 'High'])
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
