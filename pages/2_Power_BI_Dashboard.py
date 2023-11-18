import streamlit as st

def dashboard_page():
    st.title("Power BI Interactive Dashboard")
    st.markdown("<iframe width=\"1080\" height=\"1080\" src=\"https://app.powerbi.com/view?r=eyJrIjoiNDFhYzEzMWQtOTZjYi00MzUxLTgxOTUtMWUwMmM3YmY1ZGEzIiwidCI6IjBmZWQwM2EzLTQwMmQtNDYzMy1hOGNkLThiMzA4ODIyMjUzZSIsImMiOjEwfQ%3D%3D\" title=\"Good Power BI Dashboard\"></iframe>", unsafe_allow_html=True)

dashboard_page()