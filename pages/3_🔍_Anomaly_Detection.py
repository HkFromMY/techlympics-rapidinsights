import streamlit as st

### Custom functions 
from data.extract_data import extract_data, time_series_generator, generate_holidays
from model.forecast import create_rf_model
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
def load_model(name, training_lrt_kj, _dp, holiday_df):
    ### Generate X and y
    X = _dp.in_sample()
    X = X.join(holiday_df)
    y = training_lrt_kj[training_lrt_kj.columns[0]]

    ### Fitting
    rf_model = create_rf_model(name)
    rf_model.fit(X, y)

    return rf_model

def initialize_models():
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

    return models, data, dps

def subscribe_to_anomaly():
    add_logo(f'{CURRENT_DIR}\\asset\\logo.png')
    st.title(":mag: Anomaly Alert")

subscribe_to_anomaly()