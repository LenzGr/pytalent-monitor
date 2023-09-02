#!/usr/bin/env python3

import argparse
import logging
import os
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://www.talent-monitoring.com/prod-api"
TIMEZONE = "+02:00"

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
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    response_data = response.json()
    if "token" in response_data:
        token = response_data["token"]
        logging.debug("Login successful - received token: %s", token)
        return token
    else:
        logging.error("Login failed. Got status code %s", response.status_code)
        raise AuthenticationError("Authentication failed")

def refresh_token(username, password):
    logging.debug("Token expired. Refreshing token...")
    return login(username, password)

def get_data(endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)
    
    if response.status_code == 401:  # Unauthorized, token might be expired
        token = refresh_token(username, password)
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Failed to fetch data. Status Code: %s", response.status_code)
        return None

if __name__ == "__main__":
    username, password = get_credentials()
    token = login(username, password)

    data = get_data(endpoint="system/station/list", token=token)
    if data:
        first_station = data['rows'][0]
        status = first_station['status']
        print(f"Status: {status}")
        stationName = first_station['stationName']
        print(f"Station Name: {stationName}")
        powerStationGuid = first_station['powerStationGuid']
        logging.debug("GUID: %s", powerStationGuid)

        data = get_data(endpoint=f"system/station/getPowerStationByGuid?powerStationGuid={powerStationGuid}&timezone={TIMEZONE}", token=token)
        if data:
            power_data = data['data']
            totalActivePower = power_data['totalActivePower']
            print(f"Total Active Power (W): {totalActivePower}")
            dayEnergy = power_data['dayEnergy']
            print(f"Daily energy (Wh): {dayEnergy}")
            monthEnergy = power_data['monthEnergy']
            print(f"Monthly energy (Wh): {monthEnergy}")
            yearEnergy = power_data['yearEnergy']
            print(f"Yearly energy (Wh): {yearEnergy}")

        data = get_data(endpoint=f"system/station/selectLayoutComponents?powerStationGuid={powerStationGuid}", token=token)
        if data:
            components = data['data']['components'][0]
            pv1Voltage = components['pv1Voltage']
            print(f"Panel1 Voltage (V): {pv1Voltage}")
            pv1Current = components['pv1Current']
            print(f"Panel1 Current (A): {pv1Current}")
            pv1Power = components['pv1Power']
            print(f"Panel1 Power (W): {pv1Power}")
            pv2Voltage = components['pv2Voltage']
            print(f"Panel2 Voltage (V): {pv2Voltage}")
            pv2Current = components['pv2Current']
            print(f"Panel2 Current (A): {pv2Current}")
            pv2Power = components['pv2Power']
            print(f"Panel2 Power (W): {pv2Power}")
