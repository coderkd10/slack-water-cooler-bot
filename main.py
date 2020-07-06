#!/usr/bin/env python3

# should be added to a cronjob firing everyday
# e.g at 10 AM IST everyday
# 30 4 * * * python3 path/main.py >> path/cronjob.log 2>&1

import time
import random

import utils
import bot
import scheduling

logger = utils.createLogger("main")

if __name__ == "__main__":
    logger.info("starting water cooler bot...")
    shouldScheduleToday, delay_seconds = scheduling.getTodaySchedule()
    if shouldScheduleToday:
        time.sleep(delay_seconds)
        bot.ping()
