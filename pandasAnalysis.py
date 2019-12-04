import pandas as pd
import math

# Import the CO2 emission rate timetable we created beforehand
filename = "OpenDataEcoCO2.csv"
dfCO2 = pd.read_csv(filename)


# Interpolate a measure every quarter of an hour instead of every half hour
dfCO2Inter = dfCO2.interpolate(method ='linear', limit_direction ='forward')


# Add a column weekday to both dataframe
dfCO2['WeekDay'] = pd.DatetimeIndex(dfCO2['Date']).weekday
dfCO2Inter['WeekDay'] = pd.DatetimeIndex(dfCO2Inter['Date']).weekday


# loc allow to select only the rows that corresponds to a weekend
print(dfCO2Inter.loc[(dfCO2Inter['WeekDay']) >= 5]['Taux de CO2 (g/kWh)'].mean(axis=0))
print(dfCO2.loc[(dfCO2['WeekDay']) >= 5]['Taux de CO2 (g/kWh)'].mean(axis=0, skipna=True))

# loc allow to select only the rows that corresponds to a day of the week
print(dfCO2Inter.loc[(dfCO2Inter['WeekDay']) <= 4]['Taux de CO2 (g/kWh)'].mean(axis=0))
print(dfCO2.loc[(dfCO2['WeekDay']) <= 4]['Taux de CO2 (g/kWh)'].mean(axis=0, skipna=True))