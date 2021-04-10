# Blaseball Stlats Tlracker - Cache update
# Jesse Williams 🎸

# To run manually from command prompt, use `heroku run -a blaseball-stlats-tlracker python blaseball_stlats_tlracker/update_cache.py`

from blaseball_stlats_tlracker import updatePlayerStatCache

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
    print('[Debug] Updating player data for batters.')
    updatePlayerStatCache(batterNames, 'batter')
    print('[Debug] Finished updating player data for batters.')

# Update pitchers
if len(pitcherNames) > 0:
    print('[Debug] Updating player data for pitchers.')
    updatePlayerStatCache(pitcherNames, 'pitcher')
    print('[Debug] Finished updating player data for pitchers.')

print('[Debug] Successfully updated player stat cache.')

#except:
#    print('[Error] Could not update player stat cache.')
