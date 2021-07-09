import argparse
import calendar
import datetime
import time

import requests



def timestamper(timestamp):
    """
    Converts timestamps from json to NhNmNs output in a formatted string
    :param timestamp: formatted like "2021-06-04T01:25:26Z"
    :return: formatted f string containing time data
    """

    # timestamp = "2021-06-04T01:25:26Z"
    td = timestamp.split("T", 1)
    tdd = f"{td[0]} {td[1]}"
    tss = tdd.split("Z", 1)
    iso_stamp = tss[0]

    now = time.gmtime()
    nowsecs = calendar.timegm(now)
    nowstamp = datetime.datetime.utcfromtimestamp(nowsecs)
    killtime = datetime.datetime.fromisoformat(iso_stamp)
    tdelta = nowstamp - killtime

    tsdelta = str(tdelta)
    tssdelta = tsdelta.split(":", 2)
    deltastring = f"{tssdelta[0]}h {tssdelta[1]}m {tssdelta[2]}s ago"

    return deltastring


def name2id(sys_name):
    """
    Converts a Solar System name to Solar System ID
    :param sys_name: String value name of the system such as "Jita" or "D-PNP9"
    :return: system_id: the ID value of the provided system name.
    """
    search_url = (
        f"https://esi.evetech.net/latest/search/?categories=solar_system&datasource=tranquility&language=en"
        f"&search={sys_name} "
    )
    search_object = requests.get(search_url)
    search_json = search_object.json()
    system_id = search_json["solar_system"][0]
    return system_id


def id2name(sys_id):
    """
    Helper function to convert system IDs to name for verification purposes
    :param sys_id: the integer value ID of the system to be checked
    :return: system_name: the string name of the system
    """
    search_url = f"https://esi.evetech.net/latest/universe/systems/{sys_id}/"
    search_object = requests.get(search_url)
    search_json = search_object.json()
    system_name = search_json["name"]
    return system_name
