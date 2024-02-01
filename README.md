# datadog-smartmon
Datadog plugin to report hard drive metrics

## Introduction

A simple Datadog plugin to report hard drive stats. Uses pySMART to discover all hard drives and pushes all S.M.A.R.T information for each drive to DataDog. Useful for monitoring a file server or home nas.

![Alt text](/datadog-screenshot.png "Datadog screenshot")

## Instructions

* Install smartmon tools
```
apt-get install smartmontools
```

* Ubuntu 22.04 or later need aditional package
```
apt-get install exfatprogs
```

* Allow `smartctl` to be executed by non-root users (sorry!)
```
chmod +s /usr/sbin/smartctl
```

* Install pySMART to the custom datadog embedded python location (seriously?!)
```
sudo -Hu dd-agent /opt/datadog-agent/embedded/bin/pip install pysmart
```
   
* Copy over the custom check and check config file to the DataDog agent install directory   
```
cp smartmon.yaml /etc/datadog-agent/conf.d/
cp smartmon.py /etc/datadog-agent/checks.d/
```

* Restart the Datadog agent
