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
        scaling['hotdogs'] = ['0'] + lines[0].strip().split(',')
        scaling['hotdogs'] = [int(i) for i in scaling['hotdogs']]

        # Sunflower Seeds
        scaling['sunflowerseeds'] = ['0'] + lines[1].strip().split(',')
        scaling['sunflowerseeds'] = [int(i) for i in scaling['sunflowerseeds']]

        # Pickles
        scaling['pickles'] = ['0'] + lines[2].strip().split(',')
        scaling['pickles'] = [int(i) for i in scaling['pickles']]

        ## TEST
        print(f"TEST: Hotdogs @ 25 = {scaling['hotdogs'][25]}")
        print(f"TEST: Hotdogs @ 50 = {scaling['hotdogs'][50]}")
        print(f"TEST: Pickles @ 17 = {scaling['pickles'][17]}")
        print(f"TEST: Pickles @ 69 = {scaling['pickles'][69]}")
        print(f"TEST: SS @ 0 = {scaling['sunflowerseeds'][0]}")
        print(f"TEST: SS @ 1 = {scaling['sunflowerseeds'][1]}")
        print(f"TEST: SS @ 99 = {scaling['sunflowerseeds'][99]}")

    return scaling

#############
##| Flask |##
#############
bst_frontend = Flask(__name__)

@bst_frontend.route("/")
def index():

    names = ["Goodwin Morin", "Aldon Cashmoney", "York Silk", "Wyatt Glover", "Ren Hunter"]
    players = getPlayerStatsByName(names, 'batter')


    scaling=_getScaling()
    item_counts = {'hotdogs': 50, 'sunflowerseeds': 69, 'pickles': 99}

    player_base_returns = {}
    for player in players:
        player_base_returns[player.name] = (scaling['hotdogs'][item_counts['hotdogs']] * player.home_runs) + (scaling['sunflowerseeds'][item_counts['sunflowerseeds']] * player.hits) + (scaling['pickles'][item_counts['pickles']] * player.stolen_bases)
    print(scaling)
    print(players[0].multiplier)
    print(player_base_returns[players[0].name])

    ## TEST Render HTML
    return render_template(
        "index.html",
        players=players,
        player_base_returns=player_base_returns,
    )


if __name__ == "__main__":
    bst_frontend.run()
