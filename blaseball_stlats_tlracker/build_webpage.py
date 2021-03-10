# Blaseball Stlats Tlracker - Build Stlats Viewer Webpage
# Jesse Williams 🎸
# Requires Python >= 3.9

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
