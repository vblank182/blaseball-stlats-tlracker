import blaseball_stlats_tlracker.main as bst

# import os
# a=os.walk(".")
# for _ in range(50):
#     print(a.__next__())

import os


dirs = ["cache"]
cwd = os.getcwd()
print(cwd)
for dir in dirs:
    abs_dir = os.path.join(cwd, dir)
    if not os.path.exists(abs_dir):
        os.mkdir(abs_dir)



playerNameList = ["Goodwin Morin", "Wyatt Glover", "York Silk"]

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
