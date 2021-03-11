# Blaseball Stlats Tlracker - Update stlats Redis DB with fresh data
# Jesse Williams 🎸
# Requires Python >= 3.9

# Redis endpoint URI:
#  [[scheme]]             [[userinfo user:pass (with user field blank)]]                                [[host]]                      [[port]]
#    redis  ://  :p9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxe7  @  ec0-00-000-000-000.compute-1.amazonaws.com  :  25xx9
#
# Redis value types:  bytes, string, int, float
# Redis lists set and read using `rpush` and `lpop`/`lrange`

import redis, os, re
from urllib import parse

def saveData():
    # Data:
    # {fullName, location, team_nickname, team_emoji, }

    # Get Redis location URL from Heroku env variable
    rd_url = os.getenv("REDIS_URL")

    # Separate parts of URI for Redis constructor
    rd_scheme, rd_pw, rd_host, rd_port = re.search("(\w+)\:\/\/\:([\w\d]+)\@(.+)\:(\d+)", rd_url).groups()

    rd = redis.Redis(host=rd_host, port=rd_port, password=rd_pw)


    rd.set('foo', 'bar')
    g1 = rd.get('foo')
    print(g1)

    rd.rpush('list', 'Goodwin Morin')  # Start a linked list
    rd.rpush('list', 'Seattle Garages')
    gl1 = rd.lrange('list', 0, -1)  # Get entire list
    print(gl1)

    rd.rpush('list', '0.333', '69', '42')
    gl2 = rd.lrange('list', 0, -1)
    print(gl2)

saveData()
