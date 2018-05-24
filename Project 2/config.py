base_columns = [
    'Year',
    'Date',
    'State',
    'State_Abbrev'
]

variables = [
    'Gas_Per_Gallon',
    'MENTHLTH',
    'PHYSHLTH',
    'Median_Income',
    'TAVG',
    'TMIN',
    'TMAX',
    'INJURIES_DIRECT',
    'INJURIES_INDIRECT',
    'DEATHS_DIRECT',
    'DEATHS_INDIRECT',
    'DAMAGE_PROPERTY',
    'DAMAGE_CROPS',
    'SPI',
    'Population']

crime_types_original = [
    'violent_crime',
    'homicide',
    'rape_legacy',
    'robbery',
    'aggravated_assault',
    'property_crime',
    'burglary',
    'larceny',
    'motor_vehicle_theft']

# Make crime types human readable
crime_types = [' '.join(cr.split('_')).title() for cr in
               crime_types_original]
