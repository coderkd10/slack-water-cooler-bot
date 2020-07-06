#!/usr/bin/env python3

# should be added to a cronjob firing everyday
# e.g at 10 AM IST everyday
# 30 4 * * * python3 path/main.py >> logfile

import time
import random

import bot
import scheduling

if __name__ == "__main__":
    shouldScheduleToday, delay_seconds = scheduling.getTodaySchedule()
    if shouldScheduleToday:
        time.sleep(delay_seconds)
        bot.ping()
