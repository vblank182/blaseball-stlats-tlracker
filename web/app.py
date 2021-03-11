from flask import Flask, render_template
import redis, os, re
from urllib import parse

#############
## Helpers ##
#############
def _connectToRedis():
    # Connects to Redis DB and returns a Redis object
    # Get Redis location URL from Heroku env variable
    rd_url = os.getenv("REDIS_URL")
    # Separate parts of URI for Redis constructor
    rd_scheme, rd_pw, rd_host, rd_port = re.search("(\w+)\:\/\/\:([\w\d]+)\@(.+)\:(\d+)", rd_url).groups()
    return redis.Redis(host=rd_host, port=rd_port, password=rd_pw)

def _getData(playerName):
    rd = _connectToRedis()
    playerID = rd.get(playerName)                             # Get player ID by name lookup
    playerDataBytes = rd.lrange(playerID, 0, -1)                # Get player data by ID lookup
    playerData = [b.decode("utf-8") for b in playerDataBytes]   # Convert data values into proper strings
    return playerData

###########
## Flask ##
###########
bst_frontend = Flask(__name__)

@bst_frontend.route("/")
def index():

    ## TEST ##
    ## Data format:
    ##   [b'Ren Hunter', b'New York', b'Millennials', b'0x1F4F1', b'298', b'84', b'11', b'11', b'0', b'51', b'5', b'4', b'15', b'70', b'0.282', b'0.322', b'19', b'0.313', b'0.564', b'0.877', b'168', b'3', b'3', b'0', b'17', b'0']
    playerData = _getData("Ren Hunter")

    # Render HTML with count variable
    return render_template("index.html", data={'name': playerData[0], 'team': f'{playerData[1]} {playerData[2]}', 'ba': playerData[14]})


if __name__ == "__main__":
    bst_frontend.run()
