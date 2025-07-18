import streamlit as st
from dashboard import StudentDashboard

def main():
    dashboard = StudentDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()


