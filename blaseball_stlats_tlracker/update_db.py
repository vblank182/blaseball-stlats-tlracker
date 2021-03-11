# Blaseball Stlats Tlracker - Update stlats Redis DB with fresh data
# Jesse Williams 🎸

# ---- DEPRECATED ---- #

###-#-#-#-#-###
###  Redis  ###
###-#-#-#-#-###
# Redis endpoint URI:
#  [[scheme]]             [[userinfo user:pass (with user field blank)]]                                [[host]]                      [[port]]
#    redis  ://  :p9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxe7  @  ec0-00-000-000-000.compute-1.amazonaws.com  :  25xx9
#
# << redis.py methods >>
#
#  set()/get(): Used to set/get a single key/value pair in the DB
#  Ex:   rd.set('foo', 'bar')
#        print( rd.get('foo') )
#  Allowed value types:  bytes, string, int, float
#
#  rpush(): Used to start or continue a linked list by pushing a value on the right
#  lpop(): Used to read a single value from the left of the list
#  lrange(): Used to read a range of values from a list, or the entire list

import redis, os, re
from time import sleep

def update():
    # Get Redis location URL from Heroku env variable
    rd_url = os.getenv("REDIS_URL")

    # Separate parts of URI for Redis constructor
    rd_scheme, rd_pw, rd_host, rd_port = re.search("(\w+)\:\/\/\:([\w\d]+)\@(.+)\:(\d+)", rd_url).groups()

    # Open Redis connection
    rd = redis.Redis(host=rd_host, port=rd_port, password=rd_pw)

    player_id_dict = bst.getPlayerIDs(["Goodwin Morin", "York Silk", "Aldon Cashmoney"])

    player_list = bst.requestPlayerStatsFromAPI(player_id_dict, ['batting_average', 'hits', 'home_runs', 'stolen_bases'])

    player_ids = []
    for player in player_list:  # [(player id, player name, team location, team nickname, team emoji, {player stats dict}), ...]

        # Store player data with the player ID as the key.
        # List structure: [player name, team location, team nickname, team emoji, stat1, ..., statN]
        rd.rpush(player[0], player[1])  # Player name
        rd.rpush(player[0], player[2])  # Player team location
        rd.rpush(player[0], player[3])  # Player team nickname
        rd.rpush(player[0], player[4])  # Player team emoji
        rd.rpush(player[0], player[5]['batting_average'])  # Player stat BA
        rd.rpush(player[0], player[5]['hits'])  # Player stat H
        rd.rpush(player[0], player[5]['home_runs'])  # Player stat HR
        rd.rpush(player[0], player[5]['stolen_bases'])  # Player stat SB

        player_ids.append(player[0])

        ## TODO: Log requests made to/from DB and return total to main

    # print('________________')
    # print( rd.lrange(player_ids[0], 0, -1) )
    # print('________________')
    # print( rd.lrange(player_ids[1], 0, -1) )
    # print('________________')
    # print( rd.lrange(player_ids[2], 0, -1) )
    # print('^^^^^^^^^^^^^^^^')
