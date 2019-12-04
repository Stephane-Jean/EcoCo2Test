import pandas as pd

# Import the CO2 emission rate timetable we created beforehand
filename = "OpenDataEcoCO2.csv"
dfCO2 = pd.read_csv(filename)

print(dfCO2)

# Interpolate a measure every quarter of an hour instead of every half hour
dfCO2Inter = dfCO2.interpolate(method ='linear', limit_direction ='forward')

print(dfCO2Inter)