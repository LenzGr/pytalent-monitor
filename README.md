# Talent Monitoring - Gathering data from the www.talent-monitoring.com REST API

## Motivation

Our small home PV (a [priWatt priWall Duo](https://priwatt.de/stecker-solaranlagen/fassade/priwall-duo/SW10354.1)) came with a Tsuness TSOL-MS800 inverter that only shares its metrics with a proprietary cloud service hosted on https://www.talent-monitoring.com/. We either need to use their web application or a mobile app to understand how our solar power plant is performing.

`talent-monitoring.py` is a simple Python script that I hacked together to explore the Talent Monitoring REST API that is used by the vendor's mobile and web applications.

**Note: This software is not affiliated with or supported by Tsuness or any other company involved in this product.**

I used the [Network Monitor](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/index.html) built into [Firefox Developer Tools](https://firefox-dev.tools/) and [Postman](https://www.postman.com/) to extract and analyze the API calls used by the Talent Monitoring web application to populate its dashboards.

## Current Status

The script currently connects to the API using the username and password required by the mobile and web application and prints out a few values that I am interested in. It makes a lot of assumptions to simplify the code (only one power plant, only two PV panels).

The login credentials can be provided via the `--username` and `--password` command line arguments, or via environment variables (`TALENT_USERNAME` and `TALENT_PASSWORD`).

Example Output:
```
./talent-monitoring.py -u user@example.com -p password
Status: ready
Station Name: priwatt priWall duo
GUID: 13147bf1-0d11-11ee-8469-00163e00342d
Total Active Power (W): 184.0
Daily energy (Wh): 410.0
Monthly energy (Wh): 45250.0
Panel1 Voltage (V): 33.3
Panel1 Current (A): 2.19
Panel1 Power (W): 73.2
Panel2 Voltage (V): 32.9
Panel2 Current (A): 2.05
Panel2 Power (W): 67.8
```

## Next Steps

I use this script as an opportinity to brush up my (admittedly lousy) Python coding skills and learn more about connecting to REST APIs.

My final goal is to be able to visualize these metrics in a [Home Assistant Dashboard](https://www.home-assistant.io/dashboards/), but this requires a number of additional steps that I need to learn more about:

- [ ] Convert the script to use object oriented programming paradigms
- [ ] Convert the script into a proper Python module
- [ ] Publish the Python Module on the [Python Package Index](https://pypi.org/)
- [ ] Create a [Home Assistant Integration](https://www.home-assistant.io/integrations/) that uses the module

If you have any experience in performing these steps, I gladly accept pull requests and suggestions!

Some other project/resources to study in order to achieve this goal include:

* [pyAdax](https://github.com/Danielhiversen/pyAdax) by [@Danielhiversen](https://github.com/Danielhiversen/)

## LICENSE

MIT License (see `LICENSE` for details)