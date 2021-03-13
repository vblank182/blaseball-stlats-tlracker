from flask import Flask, render_template
import redis, os, re
from urllib import parse
from blaseball_stlats_tlracker import Player
from blaseball_stlats_tlracker import connectToRedis

#############
## Helpers ##
#############
def _getData(playerName):
    rd = connectToRedis()
    playerID = rd.get(playerName)                               # Get player ID by name lookup
    playerDataBytes = rd.lrange(playerID, 0, -1)                # Get player data by ID lookup
    playerData = [b.decode("utf-8") for b in playerDataBytes]   # Convert data values into proper strings

    ## Data format:
    ##   [b'Ren Hunter', b'New York', b'Millennials', b'0x1F4F1', b'298', b'84', b'11', b'11', b'0', b'51', b'5', b'4', b'15', b'70', b'0.282', b'0.322', b'19', b'0.313', b'0.564', b'0.877', b'168', b'3', b'3', b'0', b'17', b'0']


    #~~ Ultimate goal here is to have this app call `updatePlayerStatCache` or some other intermediate function from the BST module,
    #~~   which should then update the DB cache and return a Player object (we import Player here so we have the type defined).
    #~~ Then we can grab arbitrary stat values from the Player object by name (matched with the STATS static variables.)


    Player()

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
    playerDatas = []
    names = ["Aldon Cashmoney", "York Silk", "Goodwin Morin", "Wyatt Glover", "Ren Hunter"]
    for name in names:
        playerDatas.append(_getData(name))

    # Render HTML with count variable
    return render_template("index.html", data={'name': playerDatas[0], 'team': f'{playerData[1]} {playerData[2]}', 'batting_average': playerData[14]})


if __name__ == "__main__":
    bst_frontend.run()
