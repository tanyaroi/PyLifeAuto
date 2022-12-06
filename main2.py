from datetime import datetime, timedelta
import os

FILE_EXT = ".txt"
TIME_FMT = "%H:%M"

def write_timezones(zone_diff, zones_dir, zone_name):

    if not os.path.exists(zones_dir):
        os.mkdir("times")

    current_zone = datetime.now()
    target_zone = current_zone + timedelta(hours = zone_diff)
    
    fmt_target_zone = target_zone.strftime(TIME_FMT)

    with open(os.path.join(zones_dir, zone_name + FILE_EXT), "w") as f:
        f.write(f"{fmt_target_zone}\n")


def read_timezones(zones_dir, zone_name):
    
    file_path = os.path.join(zones_dir, zone_name + FILE_EXT)

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            zone_str = f.readline()
            zone_dt = datetime.strptime(zone_str, TIME_FMT + "\n")
            print(zone_dt)


write_timezones(7, "times", "japan")
read_timezones("times", "japan")