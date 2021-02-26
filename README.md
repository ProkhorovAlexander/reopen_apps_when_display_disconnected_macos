# Reopen list of apps when disconnects from external display
Python automation script to reopen list of apps when you disconnect from external display.

## Why? 

Using MBP 16" with external display I've noticed that utilization of the discrete GPU continues even when display is disconnected, it leads to higher energy consumption and generates more head. 

Investigating the reason I found out that it's due to some apps still using dGPU resourses even though it's unnecessaryu, some of the those apps are Telegram, PyCharm and even Messages in some cases (status on Feb 2021), 
it stops when you reopen them. So i've decided to automatize this process.

## How to use

Clone repository, edit **APPS_TO_REOPEN** list upon your needs than navigate to the project directory in Terminal and run following commands:

```
pip install -r requirements.txt
python3 reopen_apps_when_unplugged.py
```

**Important:** When running for the first time you might receive a prompt asking you to grant Terminal access to System events. 


**PS:**<br>
It's not polished at the moment and I haven't tested it that much, after some time I will try to make it a bit better and will add crontab instructions so the script would run right after reboot.
