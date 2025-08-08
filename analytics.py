import pandas as pd

class Analytics:
    @staticmethod
    def get_performance_insights(df):
        insights = {}
        insights['total_students'] = len(df)
        return insights