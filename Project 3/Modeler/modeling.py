import pandas as pd
import numpy as np
import requests 
import matplotlib.pyplot as plt
import datetime 
from fbprophet import Prophet 
from fbprophet.diagnostics import cross_validation
from fbprophet.diagnostics import performance_metrics
from fbprophet.plot import plot_cross_validation_metric

# Import data 
r = requests.get("https://api-app-pjblaypjta-uc.a.run.app/API/timeseries/usa")
response_dict = r.json()
df = pd.DataFrame.from_dict(response_dict)
df = df.rename(columns={'Totals as of Date': 'Date'})
df['Date'] = pd.to_datetime(df['Date']).dt.date
df['NewCases'] = df['Cases'] - df['Cases'].shift(1)
df['NewDeaths'] = df['Deaths'] - df['Deaths'].shift(1)

df_cases = df.loc[df["Cases"]>=200_000]
df_deaths = df.loc[df["Date"]>=datetime.date(2020,4,8)]

df_cases_fb = df_cases[["Date", "NewCases"]].rename(columns={"Date": "ds", "NewCases": "y"})
df_deaths_fb = df_deaths[["Date", "NewDeaths"]].rename(columns={"Date": "ds", "NewDeaths": "y"})

# Predicting  

def predictcases(days):

    prophet = Prophet()
    prophet.fit(df_cases_fb)

    future = prophet.make_future_dataframe(periods=days)
    forecast = prophet.predict(future)
    df_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    fig_forecast = prophet.plot(forecast)

    return df_forecast

def predictdeaths(days):

    prophet = Prophet()
    prophet.fit(df_deaths_fb)

    future = prophet.make_future_dataframe(periods=days)
    forecast = prophet.predict(future)
    df_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    fig_forecast = prophet.plot(forecast)

    return df_forecast

# Cross-validating 

def cross_validate(df):

    prophet = Prophet()
    prophet.fit(df)

    df_cv = cross_validation(prophet, initial='30 days', period='4 days', horizon='7 days')
    df_performance = performance_metrics(df_cv)
    fig_performance = plot_cross_validation_metric(df_cv, metric='mape')

    return df_performance

#print(predict(df_cases_fb))