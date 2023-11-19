import streamlit as st
import pandas as pd

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
def load_model(name, data, _dp, holiday_df):
    ### Generate X and y
    X = _dp.in_sample()
    X = X.join(holiday_df)
    y = data.iloc[:, 0]

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

    fields = {
        "LRT Ridership Forecasting Model": 'rail_lrt_kj',
        "RapidKL Buses Ridership Forecasting Model": 'bus_rkl',
        "MRT Ridership Forecasting Model": 'rail_mrt_kajang'
    }

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

    return models, data, dps, fields

def generate_anomalies_table(model, dp, holiday_df, y_test, sensitivity):
    X_test = dp.out_of_sample(steps=92)
    X_test = X_test.join(holiday_df)

    anomaly_table = pd.DataFrame(
        {
            "date": X_test.index.to_timestamp(),
            'actual': y_test.reset_index().iloc[:, 1],
            'forecasted': model.forecast(X_test).round(0).astype(int)
        }
    )

    anomaly_table['forecasted_upper'] = anomaly_table['forecasted'] * 1.1
    anomaly_table['forecasted_lower'] = anomaly_table['forecasted'] * 0.9

    def flag_anomaly(row):

        if sensitivity == 'high':
            if (row['actual'] < (row['forecasted_lower'] * 0.95)) or (row['actual'] > (row['forecasted_upper'] * 1.05)):
                return 1
            
        elif sensitivity == 'medium':
            if (row['actual'] < (row['forecasted_lower'] * 0.9)) or (row['actual'] > (row['forecasted_upper'] * 1.1)):
                return 1
            
        elif sensitivity == 'low':
            if (row['actual'] < (row['forecasted_lower'] * 0.85)) or (row['actual'] > (row['forecasted_upper'] * 1.15)):
                return 1
            
        return 0
    
    anomaly_table['is_anomaly'] = anomaly_table.apply(flag_anomaly, axis=1)
    anomaly_table['difference_in_percentage'] = (((anomaly_table['actual'] - anomaly_table['forecasted']) / anomaly_table['actual']) * 100).round(2).astype(str) + '%'

    anomaly_table = anomaly_table.loc[anomaly_table['is_anomaly'] == 1][['date', 'actual', 'forecasted', 'difference_in_percentage']]
    anomaly_table['date'] = pd.to_datetime(anomaly_table['date']).dt.strftime('%Y-%m-%d')
    anomaly_table = anomaly_table.rename(columns={ 'date': 'Date', 'actual': 'Actual', 'forecasted': 'Forecasted', 'difference_in_percentage': 'Difference in Percentage' })
    st.table(anomaly_table)  

def subscribe_to_anomaly():
    add_logo(f'{CURRENT_DIR}\\asset\\logo.png')
    st.title(":mag: Anomaly Alert")

    ### Legends and User Guide
    st.markdown("The table displays all of the anomalies that has happened within the selected bus/train lines in Q4 of 2022.")
    st.info("""Legend:\n
                1. Date - Date of the anomaly
    2. Actual - The actual number of ridership.
    3. Forecasted - The forecasted number of ridership.
    4. Difference in Percentage - The difference of the actual and forecasted.
       number of ridership in percentage format.""")

    models, data, dps, fields = initialize_models()
    holiday_df = generate_holidays('2022-01-01', '2023-12-31')

    col1, col2 = st.columns(2, gap='medium')
    with col1:
        model_opt = st.selectbox(
            "Please select one of the models",
            models.keys()
        )

    with col2:
        sensitivity_opt = st.selectbox(
            "Please select the sensitivity of the model",
            ("High", "Medium", "Low")
        )

    ### Tables of anomalies flagged
    selected_model = models[model_opt]
    selected_dp = dps[model_opt]
    selected_field = fields[model_opt]

    y_test = extract_data('2022-10-01', '2022-12-31', selected_field).iloc[:, 0]
    generate_anomalies_table(selected_model, selected_dp, holiday_df, y_test, sensitivity_opt.lower())

    ### Template of the email sent
    st.divider()
    st.subheader("Example Email Message:")
    st.markdown("The below message is an example of the daily alerting email that aims to provide an immediate alerts to service providers. This is to encourage service providers to take appropriate actions towards the issues swiftly by identifying the root cause to the anomalies.")
    st.markdown("""
    <div style="background-color: #EBEDEF; border-radius: 10px; padding: 16px;">
        The latest value for the ridership in MRT Kajang Line is 46292, is lower than expected 349.25%. This anamalous activity is likely to start on 9th November, 2022.
    </div>
""", unsafe_allow_html=True)

subscribe_to_anomaly()