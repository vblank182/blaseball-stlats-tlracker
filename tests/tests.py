from blaseball_stlats_tlracker import BST as bst
import os

p = bst.Player(name="Pitching Machine")

print(f'Name: {p.name}')

print('\nAll tests passed! :D')

# cwd = os.getcwd()
# playerNameList = ["Goodwin Morin"]
#
# plIDs = bst.getPlayerIDs(playerNameList)
# fields = ['batting_average']
#
# stats_list = bst.requestPlayerStatsFromAPI(plIDs, fields)
#
# print()
# for stats in stats_list:
#     print("----------------------------------------------------------------")
#     print(f'{stats[0]} [{stats[2]}]')
#     print(f'BA: {stats[1]["batting_average"]}')
# print("----------------------------------------------------------------")
# print()
# print(f'[Debug] API requests made: {bst.requests_made}')
