import utils
import pytz
import sys
import random
from datetime import datetime

logger = utils.createLogger("scheduling")
config = utils.loadConfig()
scheduling_config = config["scheduling"]
timezone_name = scheduling_config["local_timezone"]
try:
    timezone = pytz.timezone(timezone_name)
except pytz.UnknownTimeZoneError:
    logger.error("timezone {} not found in tz data. make sure it is in the list - https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")
    sys.exit(1)
working_days = scheduling_config["working_days"]
min_days_per_week = scheduling_config.get("min_days_per_week", 1)
if min_days_per_week == -1:
    min_days_per_week = len(working_days)
if min_days_per_week < 0 or min_days_per_week > len(working_days):
    logger.error("min_days_per_work should be in [0, len(working_days)] or -1")
    sys.exit(1)
working_hours = scheduling_config["working_hours"]
if len(working_hours) == 0:
    logger.error("working hours must contain atleast one start-end period")
    sys.exit(1)

def getRandomHour(seed):
    total_duration = sum([(period["end"] - period["start"]) for period in working_hours])
    rng = random.Random(seed)
    random_offset = rng.random() * total_duration
    # locate this offset within one of the working hour periods
    random_hour = None
    offset = random_offset
    for period in working_hours:
        duration = period["end"] - period["start"]
        if offset <= duration:
            random_hour = period["start"] + offset
            break
        else:
            offset -= duration
    if random_hour is None:
        logger.error("unable to hour at offset {} for a total working duration of {} [working hours {}]".format(random_offset, total_duration, working_hours))
        raise ValueError("unable to locate offset", offset, duration, working_hours)
    return random_hour

def getDatetimeFromHour(base_dt, hour):
    hour, minute = divmod(int(hour*60), 60)
    dt = datetime(year=base_dt.year, month=base_dt.month, day=base_dt.day, hour=hour, minute=minute, tzinfo=base_dt.tzinfo)
    return dt

def getTodaySchedule():
    # returns - (should_schedule: boolean, delay_seconds: float)
    now = datetime.now(tz=timezone)
    year, week, weekday = now.isocalendar()
    # at random pick number of days to schedule this week
    seed = (year*100 + week)*10
    rng = random.Random(seed)
    num_days_this_week = rng.randint(min_days_per_week, len(working_days))
    selected_days_this_week = sorted(rng.sample(working_days, num_days_this_week))
    logger.info("days for scheduling this week - {} [today's weekday = {}]".format(selected_days_this_week, weekday))
    if weekday not in selected_days_this_week:
        logger.info("not selected for scheduling today")
        return False, None
    
    hour = getRandomHour(seed + weekday)
    scheduled_dt = getDatetimeFromHour(now, hour)
    logger.info("expected trigger at {} [today at hour = {:.2f}]".format(scheduled_dt, hour))
    if scheduled_dt < now:
        logger.info("trigger time is in the past. skipping.")
        return False, None
    delay_secs = (scheduled_dt - now).total_seconds()
    return True, delay_secs
