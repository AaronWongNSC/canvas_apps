"""
Utilities to work with dates
"""

from datetime import datetime
from zoneinfo import ZoneInfo

def local_date_time_to_ztime(date:str, time:str, tz = ZoneInfo('America/Los_Angeles')) -> str:
    """
    Convert a local date (MM/DD/YYYY or MM/DD/YY) and local 24-hour time (HH:MM) to a z-time string.

    Parameters
    ----------
    date : str
        The date in MM/DD/YYYY format.
    time : str
        the time in 24-hour HH:MM format.
    tz : ZoneInfo
        A ZoneInfo time zone. Default is 'America/Los_Angeles'.

    Returns
    -------
    str
        A z-time string for the given local date and time
    """
    month, day, year = date.split('/')
    hour, minute = time.split(':')

    # Conversions
    month = int(month)
    day = int(day)
    year = int(year)
    if year < 100:
        year += 2000
    hour = int(hour)
    minute = int(minute)

    # Create datetime object
    local_datetime = datetime(year=year, month=month, day=day, hour=hour, minute=minute, tzinfo=tz)
    return local_datetime.astimezone(ZoneInfo('UTC')).isoformat().replace('+00:00', 'Z')

def local_dt_to_ztime(local_datetime: datetime) -> str:
    """Convert an aware datetime object to a z-time string.
    
    Parameters
    ----------
    local_datetime : datetime
        The timezone aware datetime object.

    Returns
    -------
    str
        A z-time string for the given local date and time    
    """
    utc_time = local_datetime.astimezone(ZoneInfo('UTC')).isoformat()
    z_time = utc_time.replace('+00:00', 'Z')
    return z_time

def split_ztime(z_time: str, tz = ZoneInfo('America/Los_Angeles')) -> list[str]:
    """Convert a z-time string into a local time date string of the form MM/DD/YYYY
    and local time string of the form HH:MM in 24-hour form.

    Parameters
    ----------
    z_time : str
        The z-time string to be converted.
    tz : ZoneInfo
        The timezone to be converted to. The default is 'America/Los_Angeles'.

    Returns
    -------
    str
        A local date string of the form MM/DD/YYYY
        A local time string of the form HH:MM

    """
    utc_datetime = datetime.fromisoformat(z_time.replace('Z', '+00:00')).replace(tzinfo=ZoneInfo('UTC'))
    local_iso = utc_datetime.astimezone(tz).isoformat()
    local_date = '/'.join([local_iso[5:7], local_iso[8:10], local_iso[0:4]])
    local_time = local_iso[11:16]
    return local_date, local_time


def ztime_to_local(z_time: str, tz = ZoneInfo('America/Los_Angeles')) -> str:
    """Convert a z-time string to an ISO string for the tz timezone.

    Parameters
    ----------
    z_time : str
        The z-time string to be converted.
    tz : ZoneInfo
        The timezone to be converted to. The default is 'America/Los_Angeles'.

    Returns
    -------
    str
        A z-time string for the given local date and time
    
    """
    utc_time = z_time.replace('Z', '+00:00')
    utc_datetime = datetime.fromisoformat(utc_time).replace(tzinfo=ZoneInfo('UTC'))
    local_time_iso = utc_datetime.astimezone(tz).isoformat()
    return local_time_iso
