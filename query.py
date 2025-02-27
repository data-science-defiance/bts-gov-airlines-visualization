import os
import sys
# from pprint import pprint
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname=os.getenv('AIRLINES_VISUALIZATION_DB_NAME'),
    user=os.getenv('AIRLINES_VISUALIZATION_DB_USER'),
    password=os.getenv('AIRLINES_VISUALIZATION_DB_PASS'),
    host=os.getenv('AIRLINES_VISUALIZATION_DB_HOST'),
    port=os.getenv('AIRLINES_VISUALIZATION_DB_PORT'),
)
cur = conn.cursor()
# cur.execute('''
#     SELECT * 
#     FROM ics484.routes
# ''')
# df = pd.DataFrame(cur.fetchall())
# df.columns = [desc[0] for desc in cur.description]
# print(df)
# print(df.columns)
# df.to_json('data/AllFlights.json', orient='columns')

# Query to get all flights in Hawaii
if 'hawaii' in sys.argv:
    cur.execute('''
        SELECT SUM(departures_performed) as departures, 
            SUM(passengers) as pass_sum, 
            origin, 
            oa.latitude as origin_lat, 
            oa.longitude as origin_long, 
            dest, 
            da.latitude as dest_lat, 
            da.longitude as dest_long
        FROM ics484.routes
        JOIN ics484.airports as oa on origin=oa.iata
        JOIN ics484.airports as da on dest=da.iata
        WHERE (ORIGIN_STATE_ABR = 'HI' OR DEST_STATE_ABR = 'HI') AND passengers > 0 AND departures_performed > 10
        GROUP BY origin, dest, oa.latitude, oa.longitude, da.latitude, da.longitude
        ORDER BY departures desc
    ''')
    df = pd.DataFrame(cur.fetchall())
    df.columns = [desc[0] for desc in cur.description]
    print(df)
    print(df.columns)
    df.to_json('data/HawaiiFlights.json', orient='records')

# Getting Airports
if 'airports' in sys.argv:
    cur.execute('''
        SELECT SUM(departures_performed) as departures, 
            SUM(passengers) as pass_sum,
            origin,
            dest,
            year,
            quarter
        FROM ics484.routes
        JOIN ics484.airports as oa on origin=oa.iata
        JOIN ics484.airports as da on dest=da.iata
        WHERE passengers > 0 AND departures_performed > 10
        GROUP BY origin, dest, year, quarter
    ''')
    df = pd.DataFrame(cur.fetchall())
    print('Constructed DataFrame')
    df.columns = [desc[0] for desc in cur.description]
    df['origin'] += ':' + df['dest'] + ':' + df['year'].astype(str) + ':' + df['quarter'].astype(str)
    df = df.set_index(['origin'])
    df = df[~df.index.duplicated(keep='first')]
    # print(df)
    df.to_json('data/FlightPathStats.json', orient='index')

if 'flights' in sys.argv:
    cur.execute('''
        SELECT oa.iata, oa.latitude as lat, oa.longitude as long
        FROM ics484.routes
        JOIN ics484.airports as oa on origin=oa.iata
        WHERE passengers > 0 AND departures_performed > 10
        GROUP BY oa.iata, lat, long
    ''')
    df = pd.DataFrame(cur.fetchall())
    print('Constructed DataFrame')
    df.columns = [desc[0] for desc in cur.description]
    df = df.set_index('iata')
    df = df[~df.index.duplicated(keep='first')]
    # print(df)
    df.to_json('data/Airports.json', orient='index')

if 'states' in sys.argv:
    cur.execute('''
        SELECT oa.iata, origin_state_abr as origin
        FROM ics484.routes
        JOIN ics484.airports as oa on origin=oa.iata
        WHERE passengers > 0 AND departures_performed > 10
        GROUP BY oa.iata, origin_state_abr
    ''')
    df = pd.DataFrame(cur.fetchall())
    print('Constructed DataFrame')
    df.columns = [desc[0] for desc in cur.description]
    df = df.groupby('origin')['iata'].apply(list).apply(lambda row: sorted(row))
    print(df)
    df.to_json('data/StatesToAirports.json', orient='index')
    
if 'reindex' in sys.argv:
    df = pd.read_json('data/USAFlights.json', orient='records')
    df['origin_abr'] += ':' + df['dest_abr'] + ':' + df['year'].astype(str) + ':' + df['quarter'].astype(str)
    df = df.set_index(['origin_abr'])
    df = df[~df.index.duplicated(keep='first')]
    df.to_json('data/Flights.json', orient='index')

if 'all' in sys.argv:
    cur.execute('''
        SELECT SUM(departures_performed) as departures, 
            SUM(passengers) as pass_sum, 
            origin, 
            oa.latitude as origin_lat, 
            oa.longitude as origin_long, 
            dest, 
            da.latitude as dest_lat, 
            da.longitude as dest_long,
            origin_state_abr as origin_state,
            dest_state_abr as dest_state,
            quarter,
            year
        FROM ics484.routes
        JOIN ics484.airports as oa on origin=oa.iata
        JOIN ics484.airports as da on dest=da.iata
        WHERE passengers > 0 AND departures_performed > 10
        GROUP BY origin, dest, oa.latitude, oa.longitude, da.latitude, da.longitude, origin_state_abr, dest_state_abr, quarter, year
        ORDER BY departures desc
    ''')
    df = pd.DataFrame(cur.fetchall())
    df.columns = [desc[0] for desc in cur.description]
    print(df)
    print(df.columns)
    df.to_json('data/AllFlights.json', orient='records')


# df = df.set_index('origin').join(df_airports.set_index('iata')).reset_index().rename(columns={'index': 'origin'})
# print(df)


