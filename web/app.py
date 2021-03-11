from flask import Flask, render_template
import redis, os, re
from urllib import parse

#############
## Helpers ##
#############
def connectToRedis():
    # Connects to Redis DB and returns a Redis object

    # Get Redis location URL from Heroku env variable
    rd_url = os.getenv("REDIS_URL")

    # Separate parts of URI for Redis constructor
    rd_scheme, rd_pw, rd_host, rd_port = re.search("(\w+)\:\/\/\:([\w\d]+)\@(.+)\:(\d+)", rd_url).groups()

    return redis.Redis(host=rd_host, port=rd_port, password=rd_pw)

###########
## Flask ##
###########
bst_frontend = Flask(__name__)

@bst_frontend.route("/")
def index():

    ## TEST
    rd = connectToRedis()
    print("%%%%%%%% FLASK %%%%%%%%")
    pid = rd.get("Ren Hunter")
    print( pid )
    print("~~~~~~~~~~~~~~~~~~~~~~~")
    print( rd.lrange(pid, 0, -1) )
    print("%%%%%%%%  END  %%%%%%%%")

    # Render HTML with count variable
    return render_template("index.html", data=data)

if __name__ == "__main__":
    bst_frontend.run()
