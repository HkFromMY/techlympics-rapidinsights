# Techlympcis: A Data-Driven Approach to Enhance Malaysia's Transportation System

### Tech Stacks Used:
1. Streamlit
2. Power BI
3. Python Scikit-learn (for modelling)

### Dependencies (for Python):
1. `pip install xgboost`
2. `pip install streamlit`
3. `pip install sklearn`
4. `pip install numpy`
5. `pip install pandas`

### Slide Resources
Link to [Presentation Slides](https://www.canva.com/design/DAF1JT2WQcE/3sP20E03ApkSChl3OdkAhg/edit?utm_content=DAF1JT2WQcE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

### Problem Statement
Each Malaysian spends 59.8 minutes on average in commuting with public transport (including LRT, MRT, and buses) which is time-consuming. This is because of the inefficient public transport system which the headway frequency for buses is around half an hour that can be affected by the punctuality as well. Not only that, old rails such as LRT are also prone to breakdown issues which can affect up to 16 stations. Hence, this has caused public transport to be a less preferred choice among Malaysians the schedule cannot be estimated accurately which can cause inconvenience to the commuters.  

![image](https://github.com/HkFromMY/techlympics-rapidinsights/assets/48499555/db6cf6b9-0b90-4777-a62c-72ca43fc5ca2)  
By analysing the data from government website, we can see that there is an upward trend of public transport usage during the post-covid period, when the workers are coming back to the office. However, there is still a 24% drop in ridership that can be seen when comparing the pre-covid period with the post-covid period which means lesser people are adopting to the public transports. Therefore, the goal of this project is to make public transport more accessible and sustainable through the following 2 initiatives:
1. Enhance the **efficiency of the maintenance effort** to increase ridership convenience
2. Enhance **resource allocation** initiatives such as staff scheduling and trains frequency via ridership demand.

### Features of RapidInsights
Rapid Insights is an all-in-one interactable solutions to make better decisions which includes the following features:
1. Interactive dashboard that is built on Power BI and embed into the application.
2. A forecasting model, known as RapidForecast, that is built with Random Forest algorithm that allows the decision makers to forecast certain number of days ahead up to 365 days of any train/bus line of choice.
3. An anomaly detection model that powers the email alerting system that allows the decision makers to configure and get alert on anamlous activities on a daily basis so that they can take approrpriate and swift actions to minimize business losses.

### Insights from the Analysis
Insights are found by analyzing the data with the charts from the Power BI Dashboard, more insights can be viewed via the link shared above, but here are some of them:
1. The average ridership for buses of all lines is lower on day of 29 and 30 for each month which makes the end of every month an ideal time for bus maintenance due to lesser bus demand.
2. The demand for Rapid Penang and Rapid Kuantan is the highest on Friday, while for Rapid KL, the bus demand is the highest on Wednesday as the employees are most likely to return to office on that day.
3. For LRT, MRT, and Monorail, ideal maintenance days would be on the weekends as these lines aims to provide its services towards the workers, thus weekends will be having less ridership demand.

### Forecasting Model
- Algorithm Used: Random Forest algorithm is used to provide reliable predictions with less bias and variance.
- Dataset Used: LRT, MRT, and Rapid KL buses from 2022-01-01 and 2022-12-31 are used for training and testing sets. For development phase, LRT from 2022-01-01 and 2022-09-30 is used to train the data, while the remaining dates are used for forecasting and testing purposes. 
- Coefficient of Determination: 0.8237
- Mean Absolute Error: 12908.14
- Mean Absolute Percentage Error: 0.08, which means there is an average of 8% deviation between the forecasted and actual values.

### Impacts
This solution are expected to impact at least 5 millions people using public transport in Malaysia by:
- Optimizing the service planning and operations
- Reducing environmental pollutions by achieving 70:30 modal split between public and private transports.
- Optimizing train and bus frequencies to accomodate the changing ridership demand.

### Future Enhancement
There is a few suggestions that can improve this project:
- Have access to breakdown/shutdown data to better forecast the demand by anticipating the accident
- Have hourly ridership data to do peak hour analysis to help the decision makers to better understand the demand on a more granular level.
- Have access to more historical data of pre-covid period to make better forecasting because there is a very huge difference in data between pre-covid and post-covid periods.

### Data Sources
Please visit [Data.Gov](https://data.gov.my/)
