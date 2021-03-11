# Blaseball Stlats Tlracker - Main Functions
# Jesse Williams 🎸

## TODO: Possibly need to convert all data pulled from Redis from a bytestring to a string

## Notes
# Values pulled from the Redis DB will be in raw byte string format and need to be converted with `.decode("utf-8")` before using as strings

import sys, os, re
from urllib.parse import quote
import requests
import redis

## Global Variables #########################################################################################################################################
REQUESTS_MADE_API = 0
REQUESTS_MADE_DB = 0

# Player stats fields to match API
# For list of allowed fields, see 'dataField's in https://api.blaseball-reference.com/v2/config
BATTER_STATS = ['at_bats', 'hits', 'doubles', 'triples', 'quadruples', 'runs_batted_in',
'stolen_bases', 'caught_stealing', 'walks', 'strikeouts', 'batting_average', 'batting_average_risp', 'hits_risp', 'on_base_percentage',
'slugging', 'on_base_slugging', 'total_bases', 'gidp', 'sacrifice_bunts', 'sacrifice_flies', 'home_runs', 'hit_by_pitches']
# Broken fields(?): 'games_played', 'runs_scored', 'sacrifices'

PITCHER_STATS = ['wins', 'losses', 'win_pct', 'earned_run_average', 'games', 'shutouts', 'innings', 'hits_allowed',
'runs_allowed', 'home_runs_allowed', 'walks', 'strikeouts', 'quality_starts', 'batters_faced', 'whip', 'hits_per_9',
'home_runs_per_9', 'walks_per_9', 'strikeouts_per_9', 'strikeouts_per_walk', 'hit_by_pitches', 'pitches_thrown']
# Broken fields(?): 'strikeout_percentage', 'walk_percentage'

# The Redis DB will store linked lists of player data with fields and ordering in this list
# These names should correspond to the Player object attributes
# Player stats are added to the end of the list, ordered according to BATTER_STATS/PITCHER_STATS
REDIS_BATTER_FIELDS = ['name', 'team_location', 'team_nickname', 'team_emoji'] + BATTER_STATS
REDIS_PITCHER_FIELDS = ['name', 'team_location', 'team_nickname', 'team_emoji'] + PITCHER_STATS

#############################################################################################################################################################

class Player():
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = id

    def setName(self, name):
        self.name = name

    def setId(self, id):
        self.id = id

    def setTeam(self, team_location, team_nickname, team_emoji=None, team_color1=None, team_color2=None, team_league=None, team_division=None):
        self.team_location = team_location
        self.team_nickname = team_nickname
        self.team_emoji = team_emoji
        self.team_color1 = team_color1
        self.team_color2 = team_color2
        self.team_league = team_league
        self.team_division = team_division


class Batter(Player):
    # Batter subclass with stats from API relevant to batters (stats taken from https://api.blaseball-reference.com/v2/config)
    def setStats(self, statdict):
        self.statdict = statdict.copy()

        # Create individual attributes for each stat so they can be referenced from the object directly
        for statName in BATTER_STATS:
            setattr(self, statName, statdict[statName])

class Pitcher(Player):
    # Pitcher subclass with stats from API relevant to pitchers (stats taken from https://api.blaseball-reference.com/v2/config)
    def setStats(self, statdict):
        self.statdict = statdict.copy()

        # Create individual attributes for each stat so they can be referenced from the object directly
        for statName in PITCHER_STATS:
            setattr(self, statName, statdict[statName])


def _createDirectory(dir):
    # Helper to set up directories
    cwd = os.getcwd()
    abs_dir = os.path.join(cwd, dir)
    if not os.path.exists(abs_dir):
        os.mkdir(abs_dir)

def _connectToRedis():
    # Connects to Redis DB and returns a Redis object

    # Get Redis location URL from Heroku env variable
    rd_url = os.getenv("REDIS_URL")

    # Separate parts of URI for Redis constructor
    rd_scheme, rd_pw, rd_host, rd_port = re.search("(\w+)\:\/\/\:([\w\d]+)\@(.+)\:(\d+)", rd_url).groups()

    return redis.Redis(host=rd_host, port=rd_port, password=rd_pw)

def _requestPlayerIDsFromAPI(playerNames):
    # Takes a list of player names (or a single player name string) and returns a dict of (name:id) pairs from the blaseball-reference API

    # If a single player name was passed in, make it a list
    if type(playerNames).__name__ == 'str': playerNames = [playerNames]

    playerIDs = {}

    for playerName in playerNames:

        playerName_URIencoded = quote(playerName)
        rsp = requests.get(f'https://api.blaseball-reference.com/v1/playerIdsByName?name={playerName_URIencoded}&current=true')

        global REQUESTS_MADE_API
        REQUESTS_MADE_API += 1

        if rsp.status_code != 200:
            print(f'[Error] API returned HTTP status code {rsp.status_code}')
            sys.exit(1)

        try:
            rsp_json = rsp.json()[0]  # Read API response into a JSON list object
        except IndexError:
            # If list is empty, we didn't get a proper response (likely a misspelling or missing DB entry)
            print(f'[Error] API couldn\'t find player named `{playerName}`.')
            sys.exit(1)

        playerIDs[playerName] = rsp_json['player_id']

    return playerIDs

def _requestPlayerStatsFromAPI(playerIDs, fields, group='hitting', season='current', gameType='R'):
    #  playerIDs : List of player IDs
    #  fields    : List of stat fields (strings) as defined by /v2/config in API
    #  group     : 'hitting' or 'pitching'
    #  season    : 'current' or an integer (1-indexed)
    #  gameType  : 'R' for regular season, 'P' for postseason

    ## TODO: Handle API errors if bad fields are provided

    # If a single player ID was passed in, make it a list
    if type(playerIDs).__name__ == 'str': playerIDs = [playerIDs]

    # If a number was passed in for season, set the season
    # Seasons are 0-indexed in API, so subtract 1 and convert to string
    if season != 'current':
        season = f'{season-1}'

    fieldsStr = ",".join(fields)  # Make comma-separated list of fields to feed into API call
    fieldsStr_URIencoded = quote(fieldsStr)

    stats_list = []

    for playerID in playerIDs:
        rsp = requests.get(f'https://api.blaseball-reference.com/v2/stats?type=season&group={group}&fields={fieldsStr_URIencoded}&season={season}&gameType={gameType}&playerId={playerID}')
        print(f'https://api.blaseball-reference.com/v2/stats?type=season&group={group}&fields={fieldsStr_URIencoded}&season={season}&gameType={gameType}&playerId={playerID}')  ## TEST

        global REQUESTS_MADE_API
        REQUESTS_MADE_API += 1

        if rsp.status_code != 200:
            print(f'[Error] API returned HTTP status code {rsp.status_code}')
            sys.exit(1)

        try:
            rsp_json = rsp.json()[0]['splits'][0]  # Read API response into a JSON list object
        except IndexError:
            # If list is empty, we didn't get a proper response (likely a misspelling or missing DB entry)
            print(f'[Error] API failed.')
            sys.exit(1)

        # Return list of JSON "splits" response for each player, including player info, team, and stats
        # Available keys: 'season', 'stat' (dict), 'player', 'team'
        stats_list.append(rsp_json)

    return stats_list



def updatePlayerIdCache(playerNames):
    # Takes a list of player names, checks for any missing names from the DB cache, retrieves them from the API, and stores them in the DB
    # Run this on player name lists before making stat requests

    rd = _connectToRedis()

    for playerName in playerNames:
        playerID = rd.get(playerName).decode("utf-8")  # Check DB for player name:id (returns None if no key exists)
        if playerID:
            # If we already have the ID in the DB, we don't need to update it
            print(f'[Debug] ID found in keystore -- {playerName}:{playerID}')
        else:
            # If we don't have the ID cached, get it from the API and save to DB as (name:id) pairs
            playerID = _requestPlayerIDsFromAPI(playerName)[playerName]  # this returns a dict so we need to get the value
            rd.set(playerName, playerID)
            print(f'[Debug] ID not found in keystore, loaded from API -- {playerName}:{playerID}')


def updatePlayerStatCache(playerNames, type, updateFlag=True):
    # Takes a list of player names, retrieves stats data from the API, then stores the new stats in the DB.
    # Returns a list of the player objects
    # Player type can be 'batter' or 'pitcher'
    ## TODO: Log timestamps of updates and prevent updates that happened within the same hour (since they won't change more often than that)

    # Update player ID cache to make sure the required player IDs are in the DB
    if updateFlag: updatePlayerIdCache(playerNames)

    rd = _connectToRedis()

    players = []
    # Update each player's data
    for playerName in playerNames:

        # Get ID for this player
        playerID = rd.get(playerName).decode("utf-8")

        # Construct a Player object to hold the data retrieved from the API
        if (type == 'batter'):
            player = Batter(name=playerName, id=playerID)
            playerData = _requestPlayerStatsFromAPI(playerID, BATTER_STATS, group='hitting')[0]

        elif (type == 'pitcher'):
            player = Pitcher(name=playerName, id=playerID)
            playerData = _requestPlayerStatsFromAPI(playerIDs, PITCHER_STATS, group='pitching')[0]

        else:
            print(f'[Error] Player type cannot be `{type}`.')
            sys.exit(2)

        # Set player team
        ## TODO: Set more team data fields
        teamData = playerData['team']
        player.setTeam(teamData['location'], teamData['nickname'], team_emoji=teamData['team_emoji'])

        # Set player stats dict
        player.setStats(playerData['stat'])

        # Add player to list of player objects
        players.append(player)


    # Store player data in Redis DB as a linked list with player ID as the key
    for player in players:

        # If a DB entry for this player already exists, delete it first to overwrite with new data
        if (rd.exists(player.id) > 0):
            rd.delete(player.id)

        if (type == 'batter'): FIELDS = REDIS_BATTER_FIELDS
        elif (type == 'pitcher'): FIELDS = REDIS_PITCHER_FIELDS

        for field in FIELDS:
            rd.rpush(player.id, getattr(player, field))  # Player name

    return players


if __name__ == '__main__':

    ## TEST
    rd = _connectToRedis()

    playerNameList = ["Aldon Cashmoney", "York Silk", "Goodwin Morin", "Wyatt Glover", "Ren Hunter"]  ## TODO: pull from a file?

    players = updatePlayerStatCache(playerNameList, 'batter', updateFlag=True)

    print("vvvvvvvvvvvvvvvvvvvvvv")
    print( f'ID: {rd.get(players[2].name).decode("utf-8")}' )
    print("----------------------")
    print( f'Stats: {rd.lrange(players[2].id, 0, -1)}' )
    print("^^^^^^^^^^^^^^^^^^^^^^")

    print(f'[Debug] API requests made: {REQUESTS_MADE_API}')
