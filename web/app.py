from flask import Flask, render_template
import redis, os, re
from urllib import parse
from blaseball_stlats_tlracker import Player, getPlayerStatsByName

def _getScaling():
    scaling = {}

    with open('item_scaling.txt', 'r') as f:
        lines = f.readlines()

        # Add an extra '0' to the start of the list to make item qtys align with indices

        # Hot Dogs
        scaling['hotdogs'] = [0] + lines[0]

        # Sunflower Seeds
        scaling['sunflowerseeds'] = [0] + lines[1]

        # Pickles
        scaling['pickles'] = [0] + lines[2]

        ## TEST
        print(f'TEST: Hotdogs @ 25 = {scaling['hotdogs'][25]}')
        print(f'TEST: Hotdogs @ 50 = {scaling['hotdogs'][50]}')
        print(f'TEST: Pickles @ 17 = {scaling['pickles'][17]}')
        print(f'TEST: Pickles @ 69 = {scaling['pickles'][69]}')
        print(f'TEST: SS @ 0 = {scaling['sunflowerseeds'][0]}')
        print(f'TEST: SS @ 1 = {scaling['sunflowerseeds'][1]}')
        print(f'TEST: SS @ 99 = {scaling['sunflowerseeds'][99]}')

    return scaling

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
        players=players,
        scaling=_getScaling(),
    )


if __name__ == "__main__":
    bst_frontend.run()
