from flask import Flask, render_template
import redis, os, re
from urllib import parse
from blaseball_stlats_tlracker import Player, getPlayerStatsByName

## REMOVE: This function is no longer needed since we have the scaling weights in the JS update function
def _getScaling():
    scaling = {}

    with open('item_scaling.txt', 'r') as f:
        lines = f.readlines()

        # We add an extra '0' to the start of the list to make item qtys align with indices

        # Hot Dogs
        scaling['hotdogs'] = ['0'] + lines[0].strip().split(',')
        scaling['hotdogs'] = [int(i) for i in scaling['hotdogs']]

        # Sunflower Seeds
        scaling['sunflowerseeds'] = ['0'] + lines[1].strip().split(',')
        scaling['sunflowerseeds'] = [int(i) for i in scaling['sunflowerseeds']]

        # Pickles
        scaling['pickles'] = ['0'] + lines[2].strip().split(',')
        scaling['pickles'] = [int(i) for i in scaling['pickles']]

    return scaling

#############
##| Flask |##
#############
bst_frontend = Flask(__name__)
bst_frontend.config['APPLICATION_ROOT'] = '/app/web'  # Set root of webserver


@bst_frontend.route("/")
def index():

    # Read list of batter names from file
    with open('../common/players_batters.txt') as f:
        batterNames = f.readlines()
        batterNames = [name.strip() for name in batterNames]

    # Read list of pitcher names from file
    with open('../common/players_pitchers.txt') as f:
        pitcherNames = f.readlines()
        pitcherNames = [name.strip() for name in pitcherNames]


    ## TODO: Split into two pages, one for batters and one for pitchers?
    names = batterNames  ## TEMP

    players = getPlayerStatsByName(names, 'batter')


    return render_template(
        "index.html",
        players=players,
    )


if __name__ == "__main__":
    bst_frontend.run()
