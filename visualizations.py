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
            value_counts.values, labels=value_counts.index, colors=colors,
            autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.6)
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
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
    def create_box_plot_scores_by_education(df):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        
        df_temp = df.copy()
        df_temp['Score_Category'] = pd.cut(df_temp['Exam_Score'], 
                                         bins=[0, 60, 70, 80, 90, 100], 
                                         labels=['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'])
        
        colors = ["#FF6B6B", "#FFE66D", "#4ECDC4", "#45B7D1", "#96CEB4"]
        
        # High School
        hs_data = df_temp[df_temp['Parental_Education_Level'] == 'High School']['Score_Category'].value_counts()
        if not hs_data.empty:
            ax1.pie(hs_data.values, labels=hs_data.index, colors=colors[:len(hs_data)], autopct='%1.1f%%')
        ax1.set_title('High School Education')
        
        # College
        college_data = df_temp[df_temp['Parental_Education_Level'] == 'College']['Score_Category'].value_counts()
        if not college_data.empty:
            ax2.pie(college_data.values, labels=college_data.index, colors=colors[:len(college_data)], autopct='%1.1f%%')
        ax2.set_title('College Education')
        
        # Low Income
        low_income_data = df_temp[df_temp['Family_Income'] == 'Low']['Score_Category'].value_counts()
        if not low_income_data.empty:
            ax3.pie(low_income_data.values, labels=low_income_data.index, colors=colors[:len(low_income_data)], autopct='%1.1f%%')
        ax3.set_title('Low Income')
        
        # High Income
        high_income_data = df_temp[df_temp['Family_Income'] == 'High']['Score_Category'].value_counts()
        if not high_income_data.empty:
            ax4.pie(high_income_data.values, labels=high_income_data.index, colors=colors[:len(high_income_data)], autopct='%1.1f%%')
        ax4.set_title('High Income')
        
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