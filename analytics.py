import pandas as pd
import numpy as np

class Analytics:
    @staticmethod
    def get_performance_insights(df):
        insights = {}
        insights['total_students'] = len(df)
        return insights

