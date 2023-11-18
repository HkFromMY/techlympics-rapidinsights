import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_forecast(actual, forecast):
    start_forecast_date = np.min(forecast['date'])
    end_forecast_date = np.max(forecast['date'])

    plt.figure(figsize=(14, 8))
    plt.title(f"Forecasted Values between {start_forecast_date.date()} and {end_forecast_date.date()}")
    ax = sns.lineplot(data=actual, x='date', y='actual_values', marker='o', label='actual-values')
    ax = sns.lineplot(ax=ax, data=forecast, x='date', y='forecasted', marker='o', label='forecasted')
    plt.ylabel("Ridership")
    plt.xlabel("Date")

    return ax