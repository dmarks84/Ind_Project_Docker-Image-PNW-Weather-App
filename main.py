# https://www.weather.gov/documentation/services-web-api
# Import necessary libraries and functions
import requests
import time
from time import sleep
from csv import writer
import sqlite3
from sql_funcs import *

# Define funciton to return the data from a given NOAA NWS endpoint
def get_data(api_endpoint):
    try:
        response = requests.get((api_endpoint))
        data = response.json()
        # print('Data recorded')
        return data
    except KeyboardInterrupt:
        print('Interupted')
        return False
    except Exception as error:
        print("Unable to get data from API endpoint:",error)
        return False

# Convert the data into a format that will be more useable later
def convert_data(data_):
    alerts = []
    try:
        for alert_ in data_['features']:
            d = dict()
            props_ = alert_['properties']
            d['id'] = props_['id']
            zones = props_['affectedZones']
            d['zones'] = ';'.join(zones)
            d['sent'] = props_['sent']
            d['onset'] = props_['onset']
            d['ends'] = props_['ends']
            d['status'] = props_['status']
            d['msg_type'] = props_['messageType']
            d['severity'] = props_['severity']
            d['certainty'] = props_['certainty']
            d['urgency'] = props_['urgency']
            d['type'] = props_['event']
            d['headline'] = props_['headline']
            d['description'] = props_['description']
            d['recorded_date'] = time.strftime("%m/%d/%y",time.localtime())
            d['recorded_time'] = time.strftime("%H:%M:%S",time.localtime())
            alerts.append(d)
        # print('Alerts parsed')
        return alerts
    except KeyboardInterrupt:
        print('Interupted')
        return False
    except Exception as error:
        print("Unable to convert data:",error)
        return False

# Condense the data into the most relevant pieces for our app
def reduce_data(alerts_):
    alerts = []
    try:
        for alert_ in alerts_:
            if alert_['status'] == 'Actual':
                alerts.append({'zones':alert_['zones'],
                            'severity':alert_['severity'],
                            'headline':alert_['headline']})
        # print('Alerts data reduced to main information')
        return alerts
    except KeyboardInterrupt:
        print('Interupted')
        return False
    except Exception as error:
        print('Alert data unable to be reduced:',error)
        return False

# Pull out the endpiont for the geography from a given state alert endpoint
def get_coords(zone_api):
    try:
        data_ = get_data(zone_api)
        # print('Zone coordinates obtained')
        typ = data_['geometry']['type']
        coords = data_['geometry']['coordinates']
        return typ, coords
    except KeyboardInterrupt:
        print('Interupted')
        return False
    except Exception as error:
        print('Zone coordindates  NOT obtained:',error)
        return False

# Save the alerts to a database, only saving those that are not already
# in the database
def save_db(latests):
    try:
        conn = sqlite3.connect(database)
        # Get all existing alert ids
        query = """SELECT id FROM alerts"""
        olds_ids = get_query(conn, query)
        olds_ids = [i[0] for i in olds_ids]
        latests_ids = [latest['id'] for latest in latests]
        newests = []
        # If the latest ids are not in the list of old ones, save them
        for idx, id in enumerate(latests_ids):
            if id in olds_ids:
                continue
            else:
                d = latests[idx]
                newests.append(d)
                command = """INSERT INTO alerts 
                VALUES(:id, :zones, :sent, :onset, :ends,
                :status, :msg_type, :severity, :certainty,
                :urgency, :type, :headline, :description,
                :recorded_date, :recorded_time);"""
                insert_row(conn, command, d)
        conn.commit()
        conn.close()
        # print('Newest alerted identified and saved in database')
        return newests
    except KeyboardInterrupt:
        print('Interupted')
        return False
    except Exception as error:
        print('Alerts NOT recorded in SQLite database:',error)
        return False

# Save the alerts (all of them) into a csv file
def save_csv(newests):
    try:
        with open('alerts.csv', 'a', newline='') as f:
            wrt = writer(f)
            for alert in newests:
                wrt.writerow(list(alert.values()))
            f.close()
        # print('Newest alerts saved in backup csv')
        return True
    except KeyboardInterrupt:
        print('Interupted')
        return False
    except Exception as error:
        print('Unable to update alert log csv file:',error)
        return False

# This will run during testing, when this script is called directly
if __name__ == '__main__':
    api_endpoint = 'https://api.weather.gov/alerts/active/area/OR'
    api_get = True
    database = 'alerts.db'
    cont = True
    wait = 3
    try:
        conn = sqlite3.connect(database)
        with open("table_init.txt") as file:
            command = file.read()
        create_table(conn, command)
    except:
        print('Could not connect to the database')
        api_get = False
    
    newests = []
    while api_get:
        try:
            print('----------------')
            print('Pulling alerts:',
                  time.strftime("%m/%d/%y %H:%M:%S",time.localtime()))
            data = get_data(api_endpoint)
            if data:
                latests = convert_data(data)
            if latests:
                print(latests)
                newests = save_db(latests)
            if newests:
                cont = save_csv(newests)
                api_get = cont
                print("Issue during process -- closing application")
            else:
                print(f"Paused for {wait} seconds until next pull")
                sleep(3)
        except KeyboardInterrupt:
            api_get = False
            print('Interupted')
    print('Program Closed')