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

    names = ["Goodwin Morin", "Aldon Cashmoney", "York Silk", "Wyatt Glover", "Ren Hunter"]

    players = getPlayerStatsByName(names, 'batter')

    ## TEST Render HTML
    return render_template(
        "index.html",
        players=players
    )


if __name__ == "__main__":
    bst_frontend.run()
