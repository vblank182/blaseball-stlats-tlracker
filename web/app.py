from flask import Flask, render_template

bst_frontend = Flask(__name__)

@bst_frontend.route("/")
def index():

    # Load current count
    with open("count.txt", "r") as f:
        count = int(f.read())

    # Increment the count
    count += 1

    # Overwrite the count
    with open("count.txt", "w") as f:
        f.write(str(count))

    # Make some test data
    data = {'name': "Goodwin Morin", 'ba': 0.369}

    # Render HTML with count variable
    return render_template("index.html", count=count, data=data)

if __name__ == "__main__":
    bst_frontend.run()
