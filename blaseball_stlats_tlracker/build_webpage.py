# Blaseball Stlats Tlracker - Build Stlats Viewer Webpage
# Jesse Williams 🎸
# Requires Python >= 3.9

### TEST ###
import main as bst
import os
from time import sleep
############


def generatePage(path, content):

    html_start = """
    <html>
    """

    html_head = """
    <head>

    </head>
    """

    html_body = f"""
    <body>
        <h1>Blaseball.</h1>
        <h3>{content[0]} [{content[1]}] has a BA of {content[2]}</h3>

    </body>
    """

    html_end = """
    </html>
    """

    html = [html_start, html_head, html_body, html_end]

    # Create/overwrite the HTML file at `path` with the newly generated one.
    with open(path, "w") as f:
        f.write("".join(html))



### TEST ###
cwd = os.getcwd()
print(cwd)
print("--------------------------------")
#print(next(os.walk('.'))[1])
print(next(os.walk('./web'))[2])
print("--------------------------------")

playerNameList = ["Goodwin Morin"]
plIDs = bst.getPlayerIDs(playerNameList)
fields = ['batting_average']
stats_list = bst.requestPlayerStatsFromAPI(plIDs, fields)

abs_dir = os.path.join(cwd, "web", "results.html")
print(abs_dir)
generatePage(abs_dir, [stats_list[0][0], stats_list[0][2], stats_list[0][1]["batting_average"]])

test_dir = os.path.join(cwd, "web", "index.html")
print(test_dir)
with open(test_dir, "w") as f:
    f.write("<html><body>Test Results Page</body></html>")

    print("--------------------------------")
    #print(next(os.walk('.'))[1])
    print(next(os.walk('./web'))[2])
    print("--------------------------------")

#############
print("...")

for _ in range(100):
    sleep(10)
    print(next(os.walk('./web'))[2])


#############
