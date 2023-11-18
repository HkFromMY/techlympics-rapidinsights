import pandas as pd
import streamlit as st

### Custom functions
from model.forecast import create_rf_model
from data.extract_data import extract_data, time_series_generator, generate_holidays
from utils.plot import plot_forecast

@st.cache_data
def load_data():
    ### Obtained all raw data
    training_lrt_kj = extract_data('2022-01-01', '2022-09-30')
    dp = time_series_generator(training_lrt_kj.index)
    holiday_df = generate_holidays('2022-01-01', '2023-12-31')

    return training_lrt_kj, dp, holiday_df

@st.cache_resource
def load_model(training_lrt_kj, _dp, holiday_df):
    ### Generate X and y
    X = _dp.in_sample()
    X = X.join(holiday_df)
    y = training_lrt_kj['rail_lrt_kj']

    ### Fitting
    rf_model = create_rf_model("Random Forest for LRT")
    rf_model.fit(X, y)

    return rf_model

def forecast_page():
    """
        Forecasting model's page
    """
    ### Initializations
    training_lrt_kj, dp, holiday_df = load_data()
    rf_model = load_model(training_lrt_kj, dp, holiday_df)

    ### Front-end for Forecasting Model
    st.write("Enter how many days you want to forecast below (Starting from 2023-01-01):")
    forecast_length = st.slider('Forecast Length', 0, 365, 14)
    if st.button('Forecast'):
        ### Forecasting
        forecasted_period = dp.out_of_sample(forecast_length)
        forecasted_period = forecasted_period.join(holiday_df)
        forecasted_values = rf_model.forecast(forecasted_period)

        ### Plot a chart to see results
        actual_values = pd.DataFrame({"date": training_lrt_kj.index.to_timestamp(), "actual_values": training_lrt_kj['rail_lrt_kj'] })
        forecasted = pd.DataFrame({"date": forecasted_period.index.to_timestamp(), "forecasted": forecasted_values })
        plot = plot_forecast(actual_values, forecasted)

        ### Display the chart on the page
        st.pyplot(plot.get_figure())

forecast_page()
