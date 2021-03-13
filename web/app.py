from flask import Flask, render_template
import redis, os, re
from urllib import parse
from blaseball_stlats_tlracker import Player, getPlayerStatsByName

#############
##| Flask |##
#############
bst_frontend = Flask(__name__)

@bst_frontend.route("/")
def index():

    names = ["Aldon Cashmoney", "York Silk", "Goodwin Morin", "Wyatt Glover", "Ren Hunter"]

    players = getPlayerStatsByName(names, 'batter')

    # Render HTML with count variable
    return render_template("index.html", data={'name': playerDatas[0], 'team': f'{playerData[1]} {playerData[2]}', 'batting_average': playerData[14]})


if __name__ == "__main__":
    bst_frontend.run()
