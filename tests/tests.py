import blaseball_stlats_tlracker.main as bst
import blaseball_stlats_tlracker.build_webpage as bw

import os
cwd = os.getcwd()


playerNameList = ["Goodwin Morin"]#["Goodwin Morin", "Wyatt Glover", "York Silk"]

plIDs = bst.getPlayerIDs(playerNameList)
fields = ['batting_average']

stats_list = bst.requestPlayerStatsFromAPI(plIDs, fields)

print()
for stats in stats_list:
    print("----------------------------------------------------------------")
    print(f'{stats[0]} [{stats[2]}]')
    print(f'BA: {stats[1]["batting_average"]}')
print("----------------------------------------------------------------")
print()
print(f'[Debug] API requests made: {bst.requests_made}')


### TEST
abs_dir = os.path.join(cwd, "web", "results.html")
bw.generatePage(abs_dir, [stats_list[0][0], stats_list[0][2], stats_list[0][1]["batting_average"]])
