# Blaseball Stlats Tlracker - Cache update
# Jesse Williams 🎸

from blaseball_stlats_tlracker import updatePlayerStatCache
import os

#try:
# Read list of batter names from file
with open('/app/common/players_batters.txt') as f:
    batterNames = f.readlines()
    batterNames = [name.strip() for name in batterNames]

# Read list of pitcher names from file
with open('/app/common/players_pitchers.txt') as f:
    pitcherNames = f.readlines()
    pitcherNames = [name.strip() for name in pitcherNames]

# Update batters
if len(batterNames) > 0:
    updatePlayerStatCache(batterNames, 'batter')

# Update pitchers
if len(pitcherNames) > 0:
    updatePlayerStatCache(pitcherNames, 'pitcher')

    print('[Debug] Successfully updated player stat cache.')

#except:
#    print('[Error] Could not update player stat cache.')
