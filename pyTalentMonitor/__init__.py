#!/usr/bin/env python3

import argparse
import asyncio
import json
import logging
import os

from aiohttp import ClientSession

# Configure logging
logging.basicConfig(level=logging.INFO)

BASE_URL = "https://www.talent-monitoring.com/prod-api"
TIMEZONE = "+02:00"


class AuthenticationError(Exception):
    pass


class TalentSolarMonitor:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        session: ClientSession = None,
        return_json: bool = False,
    ):
        self.username = username or os.environ.get("PYTALENT_USERNAME")
        self.password = password or os.environ.get("PYTALENT_PASSWORD")
        self.session = session
        self.return_json = return_json
        self.token = None

    def get_credentials(self):
        if not self.username or not self.password:
            raise ValueError(
                "Credentials not provided via command line arguments or environment variables."
            )

    async def login(self):
        login_data = {"username": self.username, "password": self.password}
        response = await self.session.post(f"{BASE_URL}/login", json=login_data)
        response_data = await response.json()
        if "token" in response_data:
            self.token = response_data["token"]
            logging.debug("Login successful - received token: %s", self.token)
        else:
            logging.error("Login failed. Got status code %s", response.status)
            raise AuthenticationError("Authentication failed")

    async def refresh_token(self):
        logging.debug("Token expired. Refreshing token...")
        self.login()

    async def get_data(self, endpoint):
        if not self.token:
            self.login()
        headers = {"Authorization": f"Bearer {self.token}"}
        response = await self.session.get(f"{BASE_URL}/{endpoint}", headers=headers)
        if response.status == 401:  # Unauthorized, token might be expired
            self.refresh_token()
            headers["Authorization"] = f"Bearer {self.token}"
            response = await self.session.get(f"{BASE_URL}/{endpoint}", headers=headers)

        if response.status == 200:
            return await response.json()
        else:
            logging.error("Failed to fetch data. Status Code: %s", response.status)
            return None

    async def fetch_solar_data(self):
        self.get_credentials()
        await self.login()

        data = await self.get_data(endpoint="system/station/list")
        if data and "rows" in data and len(data["rows"]) > 0:
            first_station = data["rows"][0]
            status = first_station["status"]
            stationName = first_station["stationName"]
            powerStationGuid = first_station["powerStationGuid"]
            logging.debug("GUID: %s", powerStationGuid)

            data = await self.get_data(
                endpoint=f"system/station/getPowerStationByGuid?powerStationGuid={powerStationGuid}&timezone={TIMEZONE}"
            )
            if data:
                power_data = data["data"]
                totalActivePower = power_data["totalActivePower"]
                dayEnergy = power_data["dayEnergy"]
                monthEnergy = power_data["monthEnergy"]
                yearEnergy = power_data["yearEnergy"]

            data = await self.get_data(endpoint=f"tools/device/selectDeviceInverter")
            if data:
                deviceGuid = data["rows"][0]["deviceGuid"]

            data = await self.get_data(
                endpoint=f"tools/device/selectDeviceInverterInfo?deviceGuid={deviceGuid}"
            )
            if data:
                pv = data["data"]["pv"]
                pv1Voltage = pv[0]["voltage"]
                pv1Current = pv[0]["current"]
                pv1Power = pv[0]["power"]
                pv2Voltage = pv[1]["voltage"]
                pv2Current = pv[1]["current"]
                pv2Power = pv[1]["power"]

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

            if self.return_json:
                return json.dumps(result, indent=4)
            else:
                for key, value in result.items():
                    print(f"{key}: {value}")


async def main(username: str, password: str, return_json: bool):
    async with ClientSession() as session:
        talent_monitor = TalentSolarMonitor(username, password, session, return_json)
        result = await talent_monitor.fetch_solar_data()
        if result:
            print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="pyTalent - Talent Solar Monitoring Script"
    )
    parser.add_argument("-u", "--username", required=False, help="Username to log in")
    parser.add_argument("-p", "--password", required=False, help="Password to log in")
    parser.add_argument(
        "--json", action="store_true", help="Return output as JSON object"
    )
    args = parser.parse_args()

    asyncio.run(main(args.username, args.password, args.json))
