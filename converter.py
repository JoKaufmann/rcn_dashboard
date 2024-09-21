import pandas as pd

def str_to_timedelta(time_str):
    if pd.isna(time_str):
        return pd.NaT
    # Remove non-numeric characters from the milliseconds part
    time_str = ''.join([char if char.isdigit() or char in [':', '.'] else '' for char in time_str])
    minutes, seconds = time_str.split(':')
    seconds, subseconds = seconds.split('.')
    total_seconds = int(minutes) * 60 + int(seconds) + int(subseconds) / 10**len(subseconds)
    return pd.to_timedelta(total_seconds, unit='s')

def str_to_sec(time_str):
    time = str_to_timedelta(time_str)
    return time.total_seconds()