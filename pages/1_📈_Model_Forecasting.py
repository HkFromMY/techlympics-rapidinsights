import pandas as pd
import streamlit as st

### Custom functions
from model.forecast import create_rf_model
from data.extract_data import extract_data, time_series_generator, generate_holidays
from utils.plot import plot_forecast
from streamlit_extras.app_logo import add_logo
from utils.constant import CURRENT_DIR

@st.cache_data
def load_data(field):
    ### Obtained all raw data
    data = extract_data('2022-01-01', '2022-09-30', field)
    dp = time_series_generator(data.index)
    holiday_df = generate_holidays('2022-01-01', '2023-12-31')

    return data, dp, holiday_df

@st.cache_resource
def load_model(name, data, _dp, holiday_df):
    ### Generate X and y
    X = _dp.in_sample()
    X = X.join(holiday_df)
    y = data.iloc[:, 0]

    ### Fitting
    rf_model = create_rf_model(name)
    rf_model.fit(X, y)

    return rf_model

def forecast(model, data, dp, holiday_df):
    ### Front-end for Forecasting Model
    st.write("Enter how many days you want to forecast below (Starting from 2023-01-01):")
    forecast_length = st.slider('Forecast Length', 0, 365, 14)
    if st.button('Forecast'):
        st.divider()
        st.subheader("Forecasted Results")
        ### Forecasting
        forecasted_period = dp.out_of_sample(forecast_length)
        forecasted_period = forecasted_period.join(holiday_df)
        forecasted_values = model.forecast(forecasted_period)

        ### Plot a chart to see results
        actual_values = pd.DataFrame({"date": data.index.to_timestamp(), "actual_values": data.iloc[:, 0] })
        forecasted = pd.DataFrame({"date": forecasted_period.index.to_timestamp(), "forecasted": forecasted_values })
        plot = plot_forecast(model.get_name(), actual_values, forecasted)

        ### Display the chart on the page
        st.pyplot(plot.get_figure())

def forecast_page():
    """
        Forecasting model's page
    """

    ###Titles and User Guide
    add_logo(f'{CURRENT_DIR}\\asset\\logo.png')
    st.title(":chart_with_upwards_trend: Forecast Ridership")
    st.info(
        """How to use:\n
        1. Determine your train / bus line of choice 
    2. Determine a duration you would like to forecast 
    3. Await for your results!
        """
    )

    ### Initializations
    training_lrt_kj, dp_kj, holiday_df = load_data('rail_lrt_kj')
    training_rapidkl, dp_bus, _ = load_data('bus_rkl')
    training_mrt_kj, dp_mrt, _ = load_data('rail_mrt_kajang')

    rf_model_lrt = load_model("Random Forest for LRT", training_lrt_kj, dp_kj, holiday_df)
    rf_model_rkl = load_model("Random Forest for RapidKL", training_rapidkl, dp_bus, holiday_df)
    rf_model_mrt = load_model("Random Forest for MRT", training_mrt_kj, dp_mrt, holiday_df)

    models = {
        "LRT Ridership Forecasting Model": rf_model_lrt,
        "RapidKL Buses Ridership Forecasting Model": rf_model_rkl,
        "MRT Ridership Forecasting Model": rf_model_mrt
    }

    data = {
        "LRT Ridership Forecasting Model": training_lrt_kj,
        "RapidKL Buses Ridership Forecasting Model": training_rapidkl,
        "MRT Ridership Forecasting Model": training_mrt_kj
    }

    dps = {
        "LRT Ridership Forecasting Model": dp_kj,
        "RapidKL Buses Ridership Forecasting Model": dp_bus,
        "MRT Ridership Forecasting Model": dp_mrt
    }

    model_opt = st.selectbox(
        "Please select one of these models",
        models.keys()
    )

    st.divider()
    selected_model = models[model_opt]
    selected_data = data[model_opt]
    selected_dp = dps[model_opt]

    if selected_model is not None or selected_model != "":
        forecast(selected_model, selected_data, selected_dp, holiday_df)

forecast_page()
