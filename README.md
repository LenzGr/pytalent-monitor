# pyTalent Monitor - Gather data from the www.talent-monitoring.com REST API

## Motivation

Our small home PV (a [priWatt priWall Duo](https://priwatt.de/stecker-solaranlagen/fassade/priwall-duo/SW10354.1)) came with a Tsuness TSOL-MS800 inverter that only shares its metrics with a proprietary cloud service hosted on https://www.talent-monitoring.com/. We either need to use their web application or a mobile app to understand how our solar power plant is performing.

`pytalent-monitor.py` is a simple Python script that I hacked together to explore the Talent Monitoring REST API that is used by the vendor's mobile and web applications.

**Note: This software is not affiliated with or supported by Tsuness or any other company involved in this product.**

I used the [Network Monitor](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/index.html) built into [Firefox Developer Tools](https://firefox-dev.tools/) and [Postman](https://www.postman.com/) to extract and analyze the API calls used by the Talent Monitoring web application to populate its dashboards.

## Current Status

The script currently connects to the API using the username and password required by the mobile and web application and prints out a few values that I am interested in. It makes a lot of assumptions to simplify the code (only one power plant, only two PV panels).

The login credentials can be provided via the `--username` and `--password` command line arguments, or via environment variables (`PYTALENT_USERNAME` and `PYTALENT_PASSWORD`).

Example Output:
```
./pytalent-monitor.py -u user@example.com -p password
Status: ready
StationName: priwatt priWall duo
TotalActivePower(W): 192.0
DailyEnergy(Wh): 2490.0
MonthlyEnergy(Wh): 5020.0
YearlyEnergy(Wh): 107460.0
Panel1Voltage(V): 33.4
Panel1Current(A): 4.67
Panel1Power(W): 156.0
Panel2Voltage(V): 34.4
Panel2Current(A): 1.28
Panel2Power(W): 44.1
```

The script can also generate JSON output by using the ``--json`` command line argument.

Example Output:
```
 ./pytalent-monitor.py -u user@example.com -p password --json
{
    "Status": "ready",
    "StationName": "priwatt priWall duo",
    "TotalActivePower(W)": 192.0,
    "DailyEnergy(Wh)": 2490.0,
    "MonthlyEnergy(Wh)": 5020.0,
    "YearlyEnergy(Wh)": 107460.0,
    "Panel1Voltage(V)": 33.4,
    "Panel1Current(A)": 4.67,
    "Panel1Power(W)": 156.0,
    "Panel2Voltage(V)": 34.4,
    "Panel2Current(A)": 1.28,
    "Panel2Power(W)": 44.1
}
```

## Next Steps

I use this script as an opportunity to brush up on my (admittedly lousy) Python coding skills and learn more about connecting to REST APIs.

My final goal is to be able to visualize these metrics in a [Home Assistant Dashboard](https://www.home-assistant.io/dashboards/), but this requires a number of additional steps that I need to learn more about:

- [ ] [Add more useful values to the output](https://github.com/LenzGr/talent-monitoring/issues/2)
- [X] [Convert the script to use object-oriented programming paradigms](https://github.com/LenzGr/talent-monitoring/issues/1)
- [ ] [Convert the script into a proper Python module/package](https://github.com/LenzGr/talent-monitoring/issues/3)
- [ ] Publish the Python Module on the [Python Package Index](https://pypi.org/)
- [ ] Create a [Home Assistant Integration](https://www.home-assistant.io/integrations/) that uses the module

If you have any experience in performing these steps, I gladly accept pull requests and suggestions!

Some other projects/resources to study in order to achieve this goal include:

* [tsun-talent-monitoring](https://github.com/asciidisco/tsun-talent-monitoring) by [@asciidisco](https://github.com/asciidisco) - a Node.js project / Docker container that pulls data from Talent Monitoring cloud and converts it into a digestible JSON structure for consumption via HTTP/REST
* [pyAdax](https://github.com/Danielhiversen/pyAdax) by [@Danielhiversen](https://github.com/Danielhiversen/)

## LICENSE

MIT License (see `LICENSE` for details)
