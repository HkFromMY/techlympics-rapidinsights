import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# statsmodels library to generate time-series features
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess

# web scraping tools
from bs4 import BeautifulSoup
import re
from datetime import datetime

DATA_DIR = "data"

def extract_holiday(year):
    """
        Extract holiday information and returns a dataframe from the website
    """
    soup = BeautifulSoup(open(f"{DATA_DIR}\\holiday_{year}.txt", 'r').read(), features='lxml')
    rows = soup.find('table').find('tbody').find_all('tr')

    ### Extract data
    data = []
    for row in rows:
        # get cells
        cells = row.find_all('td')

        # extract information (only national holiday or kl/selangor)
        if len(cells) == 4:
            if re.match(r"(\bNational\b|\bKuala Lumpur\b|\bSelangor\b)", cells[3].get_text()):
                date = datetime.strptime(cells[0].get_text(), '%d %b').replace(year=year).strftime('%Y-%m-%d')
                holiday = cells[2].get_text()
                data.append({ "date": date, "holiday": holiday })

    holiday = pd.DataFrame(data)
    return holiday

def determine_working_days(row):
    """
        Determine working days based on weekends and holidays
    """
    ### categorize weekend & holiday as the same thing
    if (row['dayofweek'] in (5, 6)) or (row['holiday'] != 'No holiday'):
        return 0
    
    return 1

def generate_holidays(start_date, end_date):
    """
        Scrape holiday data from the text file (extracted from a website)
        Then, prepare a range of date time df, and join the holidays with the range of date time df
    """

    ### Concat holiday data from the text files
    holiday = pd.concat(
        [
            extract_holiday(2022), 
            extract_holiday(2023)
        ], 
        ignore_index=True
    )
    holiday['date'] = pd.to_datetime(holiday['date'])

    ### Join with the new date range df
    daterange_df = pd.DataFrame(pd.date_range(start_date, end_date)).rename(columns={ 0: 'date' })
    holiday_df = pd.merge(holiday, daterange_df, on='date', how='right')
    holiday_df = holiday_df.fillna('No holiday')
    holiday_df['dayofweek'] = holiday_df['date'].dt.dayofweek
    holiday_df['working_day'] = holiday_df.apply(determine_working_days, axis=1)
    holiday_df = holiday_df.drop(['dayofweek', 'holiday'], axis=1)
    holiday_df = holiday_df.drop_duplicates()

    return holiday_df.set_index('date').to_period('D') # make the index a PeriodIndex object

def time_series_generator(date_index):
    """
        Create a DeterministicProcess object and returns to the client
    """
    ### generate time series features
    fourier = CalendarFourier(freq='Q', order=24)
    dp = DeterministicProcess(
        index=date_index,
        constant=True,
        order=1,
        seasonal=True,
        additional_terms=[fourier],
        drop=True
    )

    return dp

def extract_data(start_date='2022-01-01', end_date='2022-09-30'):
    """
        Extract and prepare the data for LRT Kelana Jaya line from the CSV files provided
        Needs start and end date to determine which data (in terms of date range) to extract
    """

    ### Get LRT Kelana Jaya Line data in 2022
    df = pd.read_csv(f"{DATA_DIR}\\ridership_headline.csv", parse_dates=['date'])
    lrt_kj = df[['date', 'rail_lrt_kj']].copy(deep=True)
    lrt_kj = lrt_kj.loc[(lrt_kj['date'] >= start_date) & (lrt_kj['date'] <= end_date)]
    lrt_kj = lrt_kj.set_index('date').to_period('D')
    lrt_kj = lrt_kj.loc[~(('2022-11-09' <= lrt_kj.index) & (lrt_kj.index <= '2022-11-15'))]

    return lrt_kj
