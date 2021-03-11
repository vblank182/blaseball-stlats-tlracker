# Blaseball Stlats Tlracker - Update stlats Redis DB with fresh data
# Jesse Williams 🎸
# Requires Python >= 3.9

# Redis endpoint anatomy:
#  [[scheme]]             [[userinfo user:pass (with user field blank)]]                                [[host]]                      [[port]]
#    redis  ://  :p9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxe7  @  ec0-00-000-000-000.compute-1.amazonaws.com  :  25xx9

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

    print(rd)

    test_player_name = rd.set('foo1', 'bar')
    test_player_stats = rd.set('foo2', ["0.333", "47", "36"])

    g1 = rd.get('foo1')
    g2 = rd.get('foo2')
    print(g1)
    print(g2)

saveData()
