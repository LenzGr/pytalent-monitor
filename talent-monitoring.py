#!/bin/env python3

import argparse
import logging
import os
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://www.talent-monitoring.com/prod-api"
timezone = "+02:00"
token = None

class AuthenticationError(Exception):
    pass

def get_credentials():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=False, help="Username to log in")
    parser.add_argument('-p', '--password', required=False, help="Password to log in")
    args = parser.parse_args()

    if args.username and args.password:
        return args.username, args.password

    username_env = os.environ.get('TALENT_USERNAME')
    password_env = os.environ.get('TALENT_PASSWORD')
    if username_env and password_env:
        return username_env, password_env

    raise ValueError("Credentials not provided via command line arguments or environment variables.")

def login(username, password):
    global token
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    response_data = response.json()
    if "token" in response_data:
        token = response_data["token"]
        logging.debug("Login successful - received token: %s", token)
    else:
        logging.error("Login failed. Got status code %s", response.status_code)
        raise AuthenticationError("Authentication failed")

def get_data(endpoint):
    global token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
    if response.status_code == 401:  # Unauthorized, token might be expired
        logging.debug("Token expired. Refreshing token...")
        login(username="your_username", password="your_password")
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        debug.error("Failed to fetch data. Status Code: %s", response.status_code)
        return None

if __name__ == "__main__":
    username, password = get_credentials()
    login(username = username, password = password)

    data = get_data(endpoint="system/station/list")
    if data:
        status = data['rows'][0]['status']
        print(f"Status: {status}")
        stationName = data['rows'][0]['stationName']
        print(f"Station Name: {stationName}")
        powerStationGuid = data['rows'][0]['powerStationGuid']
        logging.debug("GUID: %s", powerStationGuid)

        data = get_data(endpoint="system/station/getPowerStationByGuid?powerStationGuid="+powerStationGuid+"&timezone="+timezone)
        if data:
            totalActivePower = data['data']['totalActivePower']
            print(f"Total Active Power (W): {totalActivePower}")
            dayEnergy = data['data']['dayEnergy']
            print(f"Daily energy (Wh): {dayEnergy}")
            monthEnergy = data['data']['monthEnergy']
            print(f"Monthly energy (Wh): {monthEnergy}")
    
        data = get_data(endpoint="system/station/selectLayoutComponents?powerStationGuid="+powerStationGuid)
        if data:
            pv1Voltage = data['data']['components'][0]['pv1Voltage']
            print(f"Panel1 Voltage (V): {pv1Voltage}")
            pv1Current = data['data']['components'][0]['pv1Current']
            print(f"Panel1 Current (A): {pv1Current}")
            pv1Power = data['data']['components'][0]['pv1Power']
            print(f"Panel1 Power (W): {pv1Power}")
            pv2Voltage = data['data']['components'][0]['pv2Voltage']
            print(f"Panel2 Voltage (V): {pv2Voltage}")
            pv2Current = data['data']['components'][0]['pv2Current']
            print(f"Panel2 Current (A): {pv2Current}")
            pv2Power = data['data']['components'][0]['pv2Power']
            print(f"Panel2 Power (W): {pv2Power}")                    