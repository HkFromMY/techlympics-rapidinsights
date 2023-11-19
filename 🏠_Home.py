import streamlit as st

def landing_page():
    """
        Landing Page
    """
    st.title("Introducing to You: RapidInsights")
    col1, col2= st.columns(2, gap='large')
    with col1:
        with st.container():
            st.header(":bar_chart:")
            st.markdown("<h3 style='height:48px;'>Interactive Dashboard</h3>", unsafe_allow_html=True)
            st.markdown("It provides a comprehensive analysis on the ridership trends which the data refreshes on a daily basis for effective operational decision making.")

    with col2:
        with st.container():
            st.header(":chart_with_upwards_trend:")
            st.markdown("<h3 style='height:48px;'>Rapid Forecast</h3>", unsafe_allow_html=True)
            st.markdown("It allows you to forecast ridership trends ahead of any number of days up to 365 to make informed decision.")

    col3, _ = st.columns(2)
    with col3:
        with st.container():
            st.header(":mag:")
            st.markdown("<h3 style='height:48px;'>Anomaly Detection</h3>", unsafe_allow_html=True)
            st.markdown("It allows you to subscribe to our services that enables daily alerting whenever there's an anomaly in the data on a daily basis.")

    st.title("Why use this product?")
    col4, col5 = st.columns(2, gap='large')
    with col4:
        with st.container():
            st.header(":crystal_ball:")
            st.markdown("<h3 style='height:84px;'>Optimizing Services</h3>", unsafe_allow_html=True)
            st.markdown("It allows the Prasarana Team to adjust the service frequency, optimise staff scheduling, plan vehicle maintenance, manage fuel consumptions and adjust ticket pricing.")

    with col5:
        with st.container():
            st.header(":evergreen_tree:")
            st.markdown("<h3 style='height:84px;'>Reducing Environmental Pollutions</h3>", unsafe_allow_html=True)
            st.markdown("It assists the governemnt in achieving the goal of 70:30 modal split between public and private transports by enhancing the overall experiences in public transit.")

    col6, _ = st.columns(2, gap='large')
    with col6:
        with st.container():
            st.header(":oncoming_bus:")
            st.markdown("<h3 style='height:84px;'>Optimizing Bus Schedules</h3>", unsafe_allow_html=True)
            st.markdown("It helps the Prasarana Team to optimize the bus and train schedules by accomodating to the demand, thus improving rider wait times and reducing the traffic congestions during peak hours.")
    
landing_page()
