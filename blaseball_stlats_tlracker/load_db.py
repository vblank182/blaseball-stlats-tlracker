# Blaseball Stlats Tlracker - Load Data into DB
# Jesse Williams 🎸
# Requires Python >= 3.9

# Redis endpoint anatomy:
#  [[scheme]]             [[userinfo user:pass (with user field blank)]]                                [[host]]                      [[port]]
#    redis  ://  :p9xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxe7  @  ec0-00-000-000-000.compute-1.amazonaws.com  :  25xx9

def saveData():
    # Data:
    # {fullName, location, team_nickname, team_emoji, }

    ## TEST
    import redis, os, urllib

    print("________")
    print(os.getenv("REDIS_URL"))
    print("--------")
    print(os.getenv("REDIS_TLS_URL"))
    print("--------")
    print(os.getenv("PATH"))
    print("^^^^^^^^")

    # Get Redis location from Heroku env variable and parse URI
    rd_url = os.getenv("REDIS_URL")
    rd_pw, rd_host = urllib.parse.urlparse(rd_url).netloc.split("@")
    rd_port = urllib.parse.urlparse(rd_url).port

    print(f'{rd_url}  ==  {rd_host} : {rd_port} with {rd_pw}')

    rd = redis.Redis(host=rd_host, port=rd_port, password=rd_pw)

    print("~~~~~~~~")
    s = rd.set('foo', 'bar')
    print(s)
    g = rd.get('foo')
    print(g)

saveData()
