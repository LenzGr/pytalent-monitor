#!/usr/bin/env python3

import argparse
import json
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
    parser = argparse.ArgumentParser(description="pyTalent - Talent Solar Monitoring Script")
    parser.add_argument('-u', '--username', required=False, help="Username to log in")
    parser.add_argument('-p', '--password', required=False, help="Password to log in")
    parser.add_argument('--json', action='store_true', help="Return output as JSON object")
    args = parser.parse_args()

    if args.username and args.password:
        return args.username, args.password, args.json

    username = args.username or os.environ.get('PYTALENT_USERNAME')
    password = args.password or os.environ.get('PYTALENT_PASSWORD')
    if username and password:
        return username, password, args.json

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
    username, password, return_json = get_credentials()
    token = login(username, password)

    data = get_data(endpoint="system/station/list", token=token)
    if data:
        first_station = data['rows'][0]
        status = first_station['status']
        stationName = first_station['stationName']
        powerStationGuid = first_station['powerStationGuid']
        logging.debug("GUID: %s", powerStationGuid)

        data = get_data(endpoint=f"system/station/getPowerStationByGuid?powerStationGuid={powerStationGuid}&timezone={TIMEZONE}", token=token)
        if data:
            power_data = data['data']
            totalActivePower = power_data['totalActivePower']
            dayEnergy = power_data['dayEnergy']
            monthEnergy = power_data['monthEnergy']
            yearEnergy = power_data['yearEnergy']

        data = get_data(endpoint=f"system/station/selectLayoutComponents?powerStationGuid={powerStationGuid}", token=token)
        if data:
            components = data['data']['components'][0]
            pv1Voltage = components['pv1Voltage']
            pv1Current = components['pv1Current']
            pv1Power = components['pv1Power']
            pv2Voltage = components['pv2Voltage']
            pv2Current = components['pv2Current']
            pv2Power = components['pv2Power']

        # Create a dictionary to store the results
        result = {
            "Status": status,
            "StationName": stationName,
            "TotalActivePower(W)": totalActivePower,
            "DailyEnergy(Wh)": dayEnergy,
            "MonthlyEnergy(Wh)": monthEnergy,
            "YearlyEnergy(Wh)": yearEnergy,
            "Panel1Voltage(V)": pv1Voltage,
            "Panel1Current(A)": pv1Current,
            "Panel1Power(W)": pv1Power,
            "Panel2Voltage(V)": pv2Voltage,
            "Panel2Current(A)": pv2Current,
            "Panel2Power(W)": pv2Power,
        }

        # Print or return the result as JSON
        if return_json:
            print(json.dumps(result, indent=4))
        else:
            for key, value in result.items():
                print(f"{key}: {value}")
