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
print("Weekend Interpolated Mean :"+str(dfCO2Inter.loc[(dfCO2Inter['WeekDay']) >= 5]['Taux de CO2 (g/kWh)'].mean(axis=0)))
print("Weekend Mean :"+str(dfCO2.loc[(dfCO2['WeekDay']) >= 5]['Taux de CO2 (g/kWh)'].mean(axis=0, skipna=True)))

# loc allow to select only the rows that corresponds to a day of the week
print("Weekday Interpolated Mean :"+str(dfCO2Inter.loc[(dfCO2Inter['WeekDay']) <= 4]['Taux de CO2 (g/kWh)'].mean(axis=0)))
print("Weekday Mean :"+str(dfCO2.loc[(dfCO2['WeekDay']) <= 4]['Taux de CO2 (g/kWh)'].mean(axis=0, skipna=True)))


# Median for each of the 8 seasons of teh dataset
print("Winter 2017 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2017-01-01') & ((dfCO2Inter['Date']) <= '2017-03-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Spring 2017 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2017-03-21') & ((dfCO2Inter['Date']) <= '2017-06-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Summer 2017 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2017-06-21') & ((dfCO2Inter['Date']) <= '2017-09-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Fall 2017 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2017-09-21') & ((dfCO2Inter['Date']) <= '2017-12-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Winter 2018 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2017-12-21') & ((dfCO2Inter['Date']) <= '2018-03-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Spring 2018 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2018-03-21') & ((dfCO2Inter['Date']) <= '2018-06-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Summer 2018 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2018-06-21') & ((dfCO2Inter['Date']) <= '2018-09-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))
print("Fall 2018 Interpolated Median :"+str(dfCO2Inter.loc[((dfCO2Inter['Date']) >= '2018-09-21') & ((dfCO2Inter['Date']) <= '2018-12-20')]['Taux de CO2 (g/kWh)'].median(axis=0)))

print("Winter 2017 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2017-01-01') & ((dfCO2['Date']) <= '2017-03-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Spring 2017 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2017-03-21') & ((dfCO2['Date']) <= '2017-06-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Summer 2017 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2017-06-21') & ((dfCO2['Date']) <= '2017-09-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Fall 2017 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2017-09-21') & ((dfCO2['Date']) <= '2017-12-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Winter 2018 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2017-12-21') & ((dfCO2['Date']) <= '2018-03-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Spring 2018 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2018-03-21') & ((dfCO2['Date']) <= '2018-06-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Summer 2018 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2018-06-21') & ((dfCO2['Date']) <= '2018-09-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))
print("Fall 2018 Median :"+str(dfCO2.loc[((dfCO2['Date']) >= '2018-09-21') & ((dfCO2['Date']) <= '2018-12-20')]['Taux de CO2 (g/kWh)'].median(axis=0, skipna=True)))