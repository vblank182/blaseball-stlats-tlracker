# Blaseball Stlats Tlracker - Main Functions
# Jesse Williams 🎸
# Requires Python >= 3.9

import sys
import os
from urllib.parse import quote
import requests
import pickle

requests_made = 0
path_cache_playerIDs = os.path.join('cache', 'blaseball_player_id_cache.pickle')

def _createDirectory(dir):
    # Helper to set up directories
    cwd = os.getcwd()
    abs_dir = os.path.join(cwd, dir)
    if not os.path.exists(abs_dir):
        os.mkdir(abs_dir)

def requestPlayerIDsFromAPI(players):
    # Takes a list of player names and returns a dict of IDs from the blaseball-reference API

    playerIDs = {}

    for player in players:

        player_URIencoded = quote(player)
        rsp = requests.get(f'https://api.blaseball-reference.com/v1/playerIdsByName?name={player_URIencoded}&current=true')

        global requests_made
        requests_made += 1

        if rsp.status_code != 200:
            print(f'[Error] API returned HTTP status code {rsp.status_code}')
            sys.exit(1)

        try:
            rsp_json = rsp.json()[0]  # Read API response into a JSON list object
        except IndexError:
            # If list is empty, we didn't get a proper response (likely a misspelling or missing DB entry)
            print(f'[Error] API couldn\'t find player named `{player}`.')
            sys.exit(1)

        playerIDs[player] = rsp_json['player_id']

    return playerIDs

def requestPlayerStatsFromAPI(playerIDs, fields, group='hitting', season='current', gameType='R'):
    #  playerIDs : Dict mapping player names to IDs
    #  fields    : List of stat fields (strings) as defined by /v2/config in API
    #  group     : 'hitting' or 'pitching'
    #  season    : 'current' or an integer (1-indexed)
    #  gameType  : 'R' for regular season, 'P' for postseason

    if season != 'current':     # If a number was passed in, set the season
        season = f'{season-1}'  # Seasons are 0-indexed in API, so subtract 1 and convert to string

    fieldsStr = ",".join(fields)  # Make comma-separated list of fields to feed into API call
    fieldsStr_URIencoded = quote(fieldsStr)

    stats_list = []

    for playerID in list(playerIDs.values()):
        rsp = requests.get(f'https://api.blaseball-reference.com/v2/stats?type=season&group={group}&fields={fieldsStr_URIencoded}&season={season}&gameType={gameType}&playerId={playerID}')

        global requests_made
        requests_made += 1

        if rsp.status_code != 200:
            print(f'[Error] API returned HTTP status code {rsp.status_code}')
            sys.exit(1)

        try:
            rsp_json = rsp.json()[0]['splits'][0]  # Read API response into a JSON list object
        except IndexError:
            # If list is empty, we didn't get a proper response (likely a misspelling or missing DB entry)
            print(f'[Error] API failed.')
            sys.exit(1)

        # Return structure: [(player_name, {stats}, team_nickname, team_emoji), ...]
        stats_list.append( (rsp_json['player']['fullName'], rsp_json['stat'], rsp_json['team']['nickname'], rsp_json['team']['team_emoji']) )

    return stats_list

def getPlayerIDs(players):
    # Retrieves player IDs from either a cache file or the API and returns a dict of players and IDs

    # If cache file does not exist, get all of our IDs from the API, and create a cache file
    if not os.path.exists(path_cache_playerIDs):
        playerIDs = requestPlayerIDsFromAPI(players)

        _createDirectory("cache")  # Make sure directory exists

        with open(path_cache_playerIDs, 'w+b') as f:
            pickle.dump(playerIDs, f)  # Create a new cache file and save IDs

        # Return full set of player IDs in this request (since we know this is a fresh request with no cache)
        return playerIDs


    # If cache file exists, read as many player IDs as possible, then retrieve the rest from API and save them to cache
    else:
        with open(path_cache_playerIDs, 'r+b') as f:
            playerIDs = pickle.load(f)

        # Check if any players in the requested list don't show up in the cache
        playersNotInCache = list( set(players) - set(list(playerIDs.keys())) )
        if len(playersNotInCache) > 0:
            playerIDsNotInCache = requestPlayerIDsFromAPI(playersNotInCache)  # Get missing player IDs from API

            playerIDs |= playerIDsNotInCache  # Merge new player IDs into cached dict

            with open(path_cache_playerIDs, 'w+b') as f:
                pickle.dump(playerIDs, f)  # Save IDs to cache file, overwriting the old one

        # Return only the IDs that were requested
        playerIDsRequestedOnly = {k:playerIDs[k] for k in players}
        return playerIDsRequestedOnly


if __name__ == '__main__':

    playerNameList = ["Aldon Cashmoney", "York Silk", "Goodwin Morin", "Wyatt Glover", "Ren Hunter"]  ## TODO: pull from a file?

    plIDs = getPlayerIDs(playerNameList)


    # For list of allowed fields, see 'dataField's in https://api.blaseball-reference.com/v2/config
    ## TODO: Make a function to parse /v2/config and generate list of options. Possible make a class to represent a general option set.
    fields = ['batting_average', 'hits', 'home_runs', 'stolen_bases']

    stats_list = requestPlayerStatsFromAPI(plIDs, fields)

    print()
    for stats in stats_list:
        print("----------------------------------------------------------------")
        print(f'{stats[0]} [{stats[2]}]')
        print(f'BA: {stats[1]["batting_average"]}\tH: {stats[1]["hits"]}\tHR: {stats[1]["home_runs"]}\tSB: {stats[1]["stolen_bases"]}\t')
    print("----------------------------------------------------------------")
    print()

    print(f'[Debug] API requests made: {requests_made}')

    # {'Aldon Cashmoney': 'efafe75e-2f00-4418-914c-9b6675d39264', 'York Silk': '86d4e22b-f107-4bcf-9625-32d387fcb521', 'Goodwin Morin': '864b3be8-e836-426e-ae56-20345b41d03d'}
    # efafe75e-2f00-4418-914c-9b6675d39264,86d4e22b-f107-4bcf-9625-32d387fcb521,864b3be8-e836-426e-ae56-20345b41d03d
