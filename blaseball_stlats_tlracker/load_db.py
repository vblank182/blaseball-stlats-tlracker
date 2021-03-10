# Blaseball Stlats Tlracker - Load Data into DB
# Jesse Williams 🎸
# Requires Python >= 3.9

def saveData():
    # Data:
    # {fullName, location, team_nickname, team_emoji, }

    ## TEST
    import redis, os

    print("________")
    print(os.getenv("REDIS_URL"))
    print("--------")
    print(os.getenv("REDIS_TLS_URL"))
    print("--------")
    print(os.getenv("PATH"))
    print("^^^^^^^^")

    print("________")
    print(os.getenvb("REDIS_URL"))
    print("--------")
    print(os.getenvb("REDIS_TLS_URL"))
    print("--------")
    print(os.getenvb("PATH"))
    print("^^^^^^^^")

    redis_url = os.getenv("REDIS_URL") #.encode("idna")  # encode properly for redis package
    rd = redis.Redis(redis_url)

    s = rd.set('foo', 'bar')
    print(s)
    g = rd.get('foo')
    print(g)

saveData()
