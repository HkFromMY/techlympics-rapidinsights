import streamlit as st
from streamlit_extras.app_logo import add_logo

def dashboard_page():
    add_logo('C:\\Users\\wyeye\\Downloads\\techlympics-rapidinsights\\asset\\logo.png')
    st.title(":bar_chart: Power BI Interactive Dashboard")
    st.text("""For better experience, kindly adjust dashboard view via the Zoom function present 
below""")
    st.markdown("<iframe width=\"1080\" height=\"1080\" src=\"https://app.powerbi.com/view?r=eyJrIjoiNDFhYzEzMWQtOTZjYi00MzUxLTgxOTUtMWUwMmM3YmY1ZGEzIiwidCI6IjBmZWQwM2EzLTQwMmQtNDYzMy1hOGNkLThiMzA4ODIyMjUzZSIsImMiOjEwfQ%3D%3D\" title=\"Good Power BI Dashboard\"></iframe>", unsafe_allow_html=True)

dashboard_page()