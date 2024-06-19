# pyTalent Monitor - Gather data from the www.talent-monitoring.com REST API

## Motivation

Our small home PV (a [priWatt priWall Duo](https://priwatt.de/stecker-solaranlagen/fassade/priwall-duo/SW10354.1)) came with a Tsuness TSOL-MS800 inverter that only shares its metrics with a proprietary cloud service hosted on https://www.talent-monitoring.com/. We either need to use their web application or a mobile app to understand how our solar power plant is performing. My intention was to create an integration for [Home Assistant](https://www.home-assistant.io/), so I can integrate the data into a dashboard.

`pyTalentMonitor` is a simple Python script that I hacked together to explore the Talent Monitoring REST API that is used by the vendor's mobile and web applications.

**Note: This software is not affiliated with or supported by Tsuness or any other company involved in this product.**

I used the [Network Monitor](https://firefox-source-docs.mozilla.org/devtools-user/network_monitor/index.html) built into [Firefox Developer Tools](https://firefox-dev.tools/) and [Postman](https://www.postman.com/) to extract and analyze the API calls used by the Talent Monitoring web application to populate its dashboards.

## Current Status

**Note:*** I don't expect to further extend or develop this script. There is an integration into Home Assistant that is based on this code now: [ha-talent-monitor](https://github.com/StephanU/ha-talent-monitor) by [@StephanU](https://github.com/StephanU/) - please contribute to his project, if you have any feedback to share.

The script works and currently connects to the API using the username and password required by the mobile and web application. It prints out a few values that I am interested in. It makes a lot of assumptions to simplify the code (only one power plant, only two PV panels).

The login credentials can be provided via the `--username` and `--password` command line arguments, or via environment variables (`PYTALENT_USERNAME` and `PYTALENT_PASSWORD`).

Example Output:
```
python pyTalentMonitor/__init__.py -u user@example.com -p password
Status: ready
StationName: priwatt priWall duo
SignalStrength(%): 74
InverterTemp(C): 40.0
TotalActivePower(W): 601.8
DailyEnergy(Wh): 2730.0
MonthlyEnergy(Wh): 25580.0
YearlyEnergy(Wh): 148160.0
Panel1Voltage(V): 33.3
Panel1Current(A): 9.78
Panel1Power(W): 326.2
Panel2Voltage(V): 33.6
Panel2Current(A): 8.95
Panel2Power(W): 300.7
LineCurrent(A): 2.54
LineVoltage(V): 236.6
LineFrequency(Hz): 49.98
```

The script can also generate JSON output by using the ``--json`` command line argument.

Example Output:
```
 python pyTalentMonitor/__init__.py -u user@example.com -p password --json
{
    "Status": "ready",
    "StationName": "priwatt priWall duo",
    "SignalStrength(%)": 72,
    "InverterTemp(C)": 40.0,
    "TotalActivePower(W)": 601.8,
    "DailyEnergy(Wh)": 2730.0,
    "MonthlyEnergy(Wh)": 25580.0,
    "YearlyEnergy(Wh)": 148160.0,
    "Panel1Voltage(V)": 32.3,
    "Panel1Current(A)": 10.04,
    "Panel1Power(W)": 327.3,
    "Panel2Voltage(V)": 34.1,
    "Panel2Current(A)": 8.95,
    "Panel2Power(W)": 302.7,
    "LineCurrent(A)": 2.57,
    "LineVoltage(V)": 235.0,
    "LineFrequency(Hz)": 49.98
}
```

## Next Steps

I used this script as an opportunity to brush up on my (admittedly lousy) Python coding skills and learn more about connecting to REST APIs.

My final goal was to be able to visualize these metrics in a [Home Assistant Dashboard](https://www.home-assistant.io/dashboards/), which required a number of additional steps that I needed to learn more about:

- [X] [Add more useful values to the output](https://github.com/LenzGr/talent-monitoring/issues/2)
- [X] [Convert the script to use object-oriented programming paradigms](https://github.com/LenzGr/talent-monitoring/issues/1)
- [X] [Convert the script into a proper Python module/package](https://github.com/LenzGr/talent-monitoring/issues/3)
- [ ] Publish the Python Module on the [Python Package Index](https://pypi.org/) (will likely never be done)
- [X] Create a [Home Assistant Integration](https://www.home-assistant.io/integrations/) that uses the module (this step was not done by me)

Some other projects/resources to study in order to achieve this goal include:

* [tsun-talent-monitoring](https://github.com/asciidisco/tsun-talent-monitoring) by [@asciidisco](https://github.com/asciidisco) - a Node.js project / Docker container that pulls data from Talent Monitoring cloud and converts it into a digestible JSON structure for consumption via HTTP/REST
* [tsun-gen3-proxy](https://github.com/s-allius/tsun-gen3-proxy) - A proxy for TSUN Gen 3 Micro-Inverters for easy MQTT/Home-Assistant integration
* [pyAdax](https://github.com/Danielhiversen/pyAdax) by [@Danielhiversen](https://github.com/Danielhiversen/)

## LICENSE

MIT License (see `LICENSE` for details)
