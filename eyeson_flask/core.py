import argparse
import calendar
import datetime
import time

import requests
import json


from . import translators


class Victim:
    def __init__(self):
        self.name = ""
        self.corp = ""
        self.corpticker = ""
        self.alice = ""
        self.aliceticker = ""
        self.ship = ""
        self.killdate = ""


def num_stargates(sys_id):
    """
    Returns the number of stargates in a specified system.
    :param sys_id: System ID (int) of the designated system to lookup
    :return: integer value of the number of gates in a system.  Will always be >0
    """
    base_url = f"https://esi.evetech.net/latest/universe/systems/{sys_id}/"
    ret_obj = requests.get(base_url)
    obj_json = ret_obj.json()
    n_gates = len(obj_json["stargates"])
    return n_gates


def get_kills_dict(sys_id, list_len):
    """
    Creates a list of kill IDs and a list of hashes and zips those together in to a dictionary
    :param sys_id: the integer value ID of the system to be checked
    :param list_len: The upper bound of number of entries in the lists to create
    :return: Returns a dictionary of lists kill_list and hash_list but also returns the lists themselves
    """
    kill_list = []
    hash_list = []

    zkb_base_url = f"https://zkillboard.com/api/solarSystemID/{sys_id}/"
    zkb_obj = requests.get(zkb_base_url)
    zkb_json = zkb_obj.json()
    i = 0
    while i < list_len:
        kill_list.append(zkb_json[i]["killmail_id"])
        # print(zkb_json[i]["killmail_id"])
        hash_list.append(zkb_json[i]["zkb"]["hash"])
        # print(zkb_json[i]["zkb"]["hash"])
        i += 1

    kills_dict = dict(zip(kill_list, hash_list))
    return kills_dict, kill_list, hash_list


def get_jumps(sysid):
    """
    Retrieves number of jumps in the last 24h or whatever
    :param sysid: the integer value ID of the system to be checked
    :return: Returns integer number of jumps for specified system
    """
    base_url = (
        "https://esi.evetech.net/latest/universe/system_jumps/?datasource=tranquility"
    )
    ret_obj = requests.get(base_url)
    ret_json = ret_obj.json()
    for i in ret_json:
        if i["system_id"] == sysid:
            sysjumps = i["ship_jumps"]
    return sysjumps


def get_recent_kills(sysid):
    """
    Retrieves recent metrics for specified system in list format for ease of parsing
    :param sysid:  the integer value ID of the system to be checked
    :return: List of npc_kills, pod_kills, ship_kills for the specified system.
    """
    interaction_list = []
    base_url = (
        "https://esi.evetech.net/latest/universe/system_kills/?datasource=tranquility"
    )
    ret_obj = requests.get(base_url)
    ret_json = ret_obj.json()
    for i in ret_json:
        if i["system_id"] == sysid:
            interaction_list.append(i["npc_kills"])
            interaction_list.append(i["pod_kills"])
            interaction_list.append(i["ship_kills"])
    return interaction_list


def create_objects(n):
    """
    Creates a list of Victim objects as defined by the Victim class
    :param n: Where n is equal to the number of frags defined by the user at runtime
    :return: Returns a list of Victim objects with blank attributes
    """
    victims = []
    while len(victims) < int(n):
        victims.append(Victim())
    return victims


def fill_in_object(vic, kill_id, kill_hash):
    """
    This function defines the attributes of each object in the Victim list.
    :param vic: Victim object
    :param kill_id: Kill ID fetched from zKillboard
    :param kill_hash: Kill hash fetched from zKillboard
    :return: Returns a Victim object with defined attributes
    """
    mail_obj = requests.get(
        f"https://esi.evetech.net/latest/killmails/{kill_id}/{kill_hash}/"
    )

    mail_json = mail_obj.json()
    kd_json = mail_json["killmail_time"]

    adj_date = translators.timestamper(kd_json)

    vic.killdate = adj_date

    try:
        vic_id = mail_json["victim"]["character_id"]
        viccorp_id = mail_json["victim"]["corporation_id"]
    except:
        vic_id = "none"
        viccorp_id = mail_json["victim"]["corporation_id"]

    try:
        vicalice_id = mail_json["victim"]["alliance_id"]
    except:
        vicalice_id = "none"

    vicship_id = mail_json["victim"]["ship_type_id"]

    if vic_id != "none":
        vicname_obj = requests.get(
            f"https://esi.evetech.net/latest/characters/{vic_id}"
        )
        vicname_json = vicname_obj.json()
        vic.name = vicname_json["name"]
    else:
        vic.name = "none"

    viccorp_id_obj = requests.get(
        f"https://esi.evetech.net/latest/corporations/{viccorp_id}/?datasource=tranquility"
    )
    viccorp_json = viccorp_id_obj.json()
    vic.corp = viccorp_json["name"]
    vic.corpticker = viccorp_json["ticker"]

    if vicalice_id == "none":
        vic.alice = "none"
        vic.aliceticker = "NONE"

    else:
        vicalice_obj = requests.get(
            f"https://esi.evetech.net/latest/alliances/{vicalice_id}/?datasource=tranquility"
        )
        vicalice_json = vicalice_obj.json()
        vic.alice = vicalice_json["name"]
        vic.aliceticker = vicalice_json["ticker"]

    ids_url = f"https://esi.evetech.net/latest/universe/types/{vicship_id}/?datasource=tranquility&language=en"
    ids_req = requests.get(ids_url)
    ids_json = ids_req.json()
    vic.ship = ids_json["name"]
    return vic