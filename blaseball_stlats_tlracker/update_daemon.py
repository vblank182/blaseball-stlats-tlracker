# Blaseball Stlats Tlracker - Main module
# Jesse Williams 🎸

from blaseball_stlats_tlracker import connectToRedis, updatePlayerIdCache


def updatePlayerStatCache(playerNames, type):
    # Takes a list of player names with a given type, checks for any missing names from the DB cache, retrieves them from the API, and stores them in the DB
    # This function will be run periodically by a separate process in order to update the cache DB with fresh data.
    # Player type can be 'batter' or 'pitcher'

    rd = connectToRedis()

    # Make sure player IDs are present in DB
    updatePlayerIdCache(playerNames, rd)

    # Update each player's data
    for playerName in playerNames:

        # Get ID for this player
        playerID = rd.get(playerName).decode("utf-8")

        # Construct a Player object to hold the data retrieved from the API
        if (type == 'batter'):
            playerData = _requestPlayerStatsFromAPI(playerID, BATTER_STATS, group='hitting')[0]
            player = Batter('batter', playerName, playerID, playerData)

        elif (type == 'pitcher'):
            playerData = _requestPlayerStatsFromAPI(playerID, PITCHER_STATS, group='pitching')[0]
            player = Pitcher('pitcher', playerName, playerID, playerData)

        else:
            print(f'[Error] Player type cannot be `{type}`.')
            sys.exit(2)

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
