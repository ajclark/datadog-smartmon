# datadog-smartmon
DataDog plugin to report hard drive metrics

## Introduction

A simple DataDog plugin to report hard drive stats. Uses pySMART to discover all hard drives and pushes all S.M.A.R.T information for each drive to DataDog. Useful for monitoring a file server or home nas.

## Instructions

* Install smartmon tools
```
apt-get install smartmontools
```

* Allow `smartctl` to be executed by non-root users (sorry!)
```
chmod +s /usr/sbin/smartctl
```

* Install pySMART to the custom datadog embedded python location (seriously?!)
```
/opt/datadog-agent/embedded/bin/pip install pysmart
```
   
* Copy over the custom check and check config file to the DataDog agent install directory   
```
    cp smartmon.yaml /etc/dd-agent/conf.d/
    cp smartmon.py /etc/dd-agent/checks.d/
```

* Restart the DataDog agent
