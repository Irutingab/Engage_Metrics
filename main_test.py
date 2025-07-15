#!/usr/bin/env python3
# Simple main.py to test the dashboard
import streamlit as st
import sys
import os

# Ensure the current directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        from dashboard import StudentDashboard
        
        # Create and run dashboard
        dashboard = StudentDashboard()
        dashboard.run()
        
    except Exception as e:
        st.error(f"Critical error: {str(e)}")
        st.write("Error details:")
        import traceback
        st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
