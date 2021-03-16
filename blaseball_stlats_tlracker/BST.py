# Blaseball Stlats Tlracker - Main module
# Jesse Williams 🎸

## TODO: Possibly need to convert all data pulled from Redis from a bytestring to a string
## TODO: Move Player class and other helper functions into a python library accessible from both
## TODO: Add a logging system, including API and DB request counts

## Notes
# Values pulled from the Redis DB will be in raw byte string format and need to be converted with `.decode("utf-8")` before using as strings

import sys, os, re
from urllib.parse import quote
from time import sleep
import requests
import redis


########################
##| Global Variables |##
########################
REQUESTS_MADE_API = 0
REQUESTS_MADE_DB = 0


#########################
##| Class Definitions |##
#########################

class Player():
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
    REDIS_INFO_FIELDS = ['name', 'team_location', 'team_nickname', 'team_emoji']
    REDIS_BATTER_FIELD_ORD = REDIS_INFO_FIELDS + BATTER_STATS
    REDIS_PITCHER_FIELD_ORD = REDIS_INFO_FIELDS + PITCHER_STATS

    @staticmethod
    def parseCacheData(playerType, data):
        parsedData = {}

        # HACK: We don't need to worry about these because we don't need them for the 'data' part of the Player constructor
        parsedData['season'] = ''  ## TODO: Include this in the DB?
        parsedData['player'] = {'id': '', 'fullName': ''}

        # Index these values directly from the REDIS list to make sure they keep the correct order
        parsedData['team'] = {
            'location': data[Player.REDIS_INFO_FIELDS.index('team_location')],
            'nickname': data[Player.REDIS_INFO_FIELDS.index('team_nickname')],
            'team_emoji': data[Player.REDIS_INFO_FIELDS.index('team_emoji')]
        }

        # Set individual player stat attributes (depending on type)
        # Index these values directly from the REDIS list to make sure they keep the correct order
        stats = {}
        if (playerType == 'batter'):
            for statName in Player.BATTER_STATS:
                stats[statName] = data[Player.REDIS_BATTER_FIELD_ORD.index(statName)]

        elif (playerType == 'pitcher'):
            for statName in Player.PITCHER_STATS:
                stats[statName] = data[Player.REDIS_PITCHER_FIELD_ORD.index(statName)]
        else:
            print(f'[Error] Player type cannot be `{playerType}`.')
            sys.exit(2)

        parsedData['stat'] = stats

        return parsedData

    def __init__(self, ptype, name, id, data):
        self.ptype = ptype    # Must be 'batter' or 'pitcher'
        self.name = name
        self.id = id
        self.data = data
        # The 'data' parameter should be formatted as the 'splits' json dict response from API:
        #   { 'season':#, 'stat':{x:x}, 'player':{x:x}, 'team':{x:x} }

        # By constructing a Player object, we can manage the order of the data values
        #   within the class itself and allow for arbitrary attribute reads from the app side.
        # All operations dependent on the ordering of stat fields should be handled within the Player class.
        # That way, ordering can be kept consistent by the class and player attributes can still be
        #   accessed arbitrarily from outside without any knowledge of DB ordering.


        # Set player team
        self.team_location = self.data['team']['location']
        self.team_nickname = self.data['team']['nickname']

        # Format emoji as an HTML code: &#xFFFFF;
        emoji_hex = self.data['team']['team_emoji']

        ## HACK: If we get a bytestring here, we must be receiving the data from the cache.
        #        This means the emoji is already HTML formatted and we just need to convert it to a string.
        if type(emoji_hex).__name__ == 'bytes':
            self.team_emoji = emoji_hex.decode('utf-8')
        # IF we just get a regular string, assume we got an API response which should be formatted as "0xFFFFF"
        else:
            emoji_hex = emoji_hex[1:]                   # Take off the '0' at the start of the string
            self.team_emoji = "&#" + emoji_hex + ";"    # Construct full HTML unicode string


        # Set individual player stat attributes (depending on type)
        if (ptype == 'batter'):
            for statName in Player.BATTER_STATS:
                setattr(self, statName, float(self.data['stat'][statName]))

        elif (ptype == 'pitcher'):
            for statName in Player.PITCHER_STATS:
                setattr(self, statName, float(self.data['stat'][statName]))
        else:
            print(f'[Error] Player type cannot be `{ptype}`.')
            sys.exit(2)

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

    def setMultiplier(self, multiplier):
        self.multiplier = multiplier


#########################
##| Private Functions |##
#########################

def _createDirectory(dir):
    # Helper to set up directories
    cwd = os.getcwd()
    abs_dir = os.path.join(cwd, dir)
    if not os.path.exists(abs_dir):
        os.mkdir(abs_dir)

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

        global REQUESTS_MADE_API
        REQUESTS_MADE_API += 1

        if rsp.status_code != 200:
            print(f'[Error] API returned HTTP status code {rsp.status_code}')
            sys.exit(1)

        try:
            rsp_json = rsp.json()[0]['splits'][0]  # Read API response into a JSON list object
        except IndexError as e:
            # If list is empty, either we didn't get a proper response (likely a misspelling or missing DB entry),
            #   or we got an empty response (likely because the player doesn't have any data for the selected season).

            # Check if we got an empty json response (successful API response, but no data)
            if rsp.json()[0]['splits'] == []:
                print(f'[Error] No data returned from API for player with ID {playerID}. Skipping player. Error message:\n{e}')
                stats_list.append(None)  # Return None for this player

            # If not, the API request must have returned an error
            else:
                print(f'[Error] API request failed for player with ID {playerID}. Skipping player. Error message:\n{e}')
                stats_list.append(None)  # Return None for this player
            continue  # Skip to next player

        # Return list of JSON "splits" response for each player, including player info, team, and stats
        # Available keys: 'season', 'stat' (dict), 'player', 'team'
        stats_list.append(rsp_json)

    return stats_list


def _updatePlayerIdCache(playerNames, redis_connection=None, force_update=False):
    # Run this on player name lists before making stat requests
    # Returns dict of player names to IDs which can be used immediately after calling for an update

    # Check if we were passed an existing connection object. If not, create one.
    if redis_connection == None: rd = connectToRedis()
    else: rd = redis_connection

    playerNameToIdDict = {}

    # For each player, check if their ID already exists in the DB. If not, get it from the API.
    for playerName in playerNames:
        playerID = rd.get(playerName)  # Check DB for player name:id (returns None if no key exists)

        if force_update:
            # If we want to force an update, get data from the API and save to DB as (name:id) pairs
            playerID = _requestPlayerIDsFromAPI(playerName)[playerName]  # this returns a dict so we need to get the value
            rd.set(playerName, playerID)
            print(f'[Debug] ID force-refreshed from API -- {playerName}:{playerID}')

        else:
            if playerID:
                # If we already have the ID in the DB, we don't need to update it
                playerID = playerID.decode("utf-8")  # Convert the ID to a proper string
                print(f'[Debug] ID found in keystore -- {playerName}:{playerID}')
            else:
                # If we don't have the ID cached, get it from the API and save to DB as (name:id) pairs
                playerID = _requestPlayerIDsFromAPI(playerName)[playerName]  # this returns a dict so we need to get the value
                rd.set(playerName, playerID)
                print(f'[Debug] ID not found in keystore, loaded from API -- {playerName}:{playerID}')

        # Save the player name and ID to return
        playerNameToIdDict[playerName] = playerID

    return playerNameToIdDict

def _getMultiplier(playerName):
    ## TODO: Replace this with a system for reading player multipliers from the API

    players_with_2x_mult = ['York Silk', 'Nagomi Mcdaniel']         # Super Idol
    players_with_5x_mult = ['Wyatt Glover', 'Adalberto Tosser']     # Credit to the Team

    if playerName in players_with_2x_mult:
        return 2
    elif playerName in players_with_5x_mult:
        return 5
    else:
        return 1


########################
##| Public Functions |##
########################

def connectToRedis():
    ## TODO: Possibly should make this back into a private function if nothing uses it
    # Connects to Redis DB and returns a Redis object

    # Get Redis location URL from Heroku env variable
    rd_url = os.getenv("REDIS_URL")

    # Separate parts of URI for Redis constructor
    rd_scheme, rd_pw, rd_host, rd_port = re.search("(\w+)\:\/\/\:([\w\d]+)\@(.+)\:(\d+)", rd_url).groups()

    return redis.Redis(host=rd_host, port=rd_port, password=rd_pw)

def updatePlayerStatCache(playerNames, playerType):
    # Takes a list of player names with a given type, checks for any missing names from the DB cache, retrieves them from the API, and stores them in the DB
    # This function will be run periodically by a separate process in order to update the cache DB with fresh data
    # Returns a list of populated player objects (probably not needed, but just in case)
    # Player type can be 'batter' or 'pitcher'
    # This should be the only place we run `_requestPlayerStatsFromAPI`

    ## TODO: Log timestamps of updates to be referenced by the web app (to show time of last update)
    ## TODO: Make 'playerType' parameter a list of player types corresponding to their order in 'playerNames', or combine them into a tuple??

    rd = connectToRedis()

    # Make sure player IDs are present in DB
    playerNameToIdDict = _updatePlayerIdCache(playerNames, rd)

    players = []

    # Update each player's data
    for playerName in playerNames:

        # Get ID for this player (since we just ran an update, we can use the returned IDs)
        playerID = playerNameToIdDict[playerName]

        # Construct a Player object to hold the data retrieved from the API
        if (playerType == 'batter'):
            playerData = _requestPlayerStatsFromAPI(playerID, Player.BATTER_STATS, group='hitting')[0]
            if not playerData: continue  # If we got a None response, skip player

            player = Player(playerType, playerName, playerID, playerData)  # Create player object

        elif (playerType == 'pitcher'):
            playerData = _requestPlayerStatsFromAPI(playerID, Player.PITCHER_STATS, group='pitching')[0]
            if not playerData: continue  # If we got a None response, skip player

            player = Player(playerType, playerName, playerID, playerData)  # Create player object

        else:
            print(f'[Error] Player type cannot be `{playerType}`.')
            sys.exit(2)

        # Add player to list of player objects
        players.append(player)


    # Store player data in Redis DB as a linked list with player ID as the key
    for player in players:

        # If a DB entry for this player already exists, delete it first to overwrite with new data
        if (rd.exists(player.id) > 0):
            rd.delete(player.id)

        if (playerType == 'batter'): fields = Player.REDIS_BATTER_FIELD_ORD
        elif (playerType == 'pitcher'): fields = Player.REDIS_PITCHER_FIELD_ORD

        for field in fields:
            rd.rpush(player.id, getattr(player, field))

    return players


def getPlayerStatsByName(playerNames, playerType):
    # Used by the web app to request player objects containing cached player data
    # Returns a list of Player objects populated with data

    ## TODO: Make 'playerType' parameter a list of player types corresponding to their order in 'playerNames', or combine them into a tuple?

    # If a single player ID was passed in, make it a list
    if type(playerNames).__name__ == 'str': playerNames = [playerNames]

    rd = connectToRedis()

    # For each player, create a player object and populate with data from cache DB
    players = []
    for playerName in playerNames:
        try:
            playerID = rd.get(playerName)                   # Get player's ID using name
        except:
            print(f'[Error] Cannot find ID for player {playerName} in DB cache. Skipping player.')
            continue

        try:
            playerCacheData = rd.lrange(playerID, 0, -1)    # Get player's data using ID
        except:
            print(f'[Error] Cannot find data for player {playerName} with ID {playerID} in DB cache. Skipping player.')
            continue

        playerCacheData = [s.decode("utf-8") for s in playerCacheData]  # Convert values to strings

        # Parse the player data into the correct form to construct the player object
        print(f'[Debug] For player {playerName},  playerCacheData: {playerCacheData}')  ## TEST
        playerData = Player.parseCacheData(playerType, playerCacheData)

        # Create the Player object
        player = Player(playerType, playerName, playerID, playerData)

        # Set player's coin multiplier
        multiplier = _getMultiplier(playerName)
        player.setMultiplier(multiplier)

        players.append(player)

    return players
