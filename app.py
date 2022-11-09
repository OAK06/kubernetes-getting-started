from flask import Flask
from helpers import DBHelper as DB

import socket


app = Flask(__name__)


@app.route("/")
def hello():
    html = """Hello World!
    Hostname: {hostname}"""
    html = html.format(hostname=socket.gethostname())
    try:
        conn = DB.getConn()
        result = DB.fetchone(conn, "SELECT version();")
        version = ""
        for i in result:
            version = i
        html += " | DB Version: {version}"
        html = html.format(version=version)
    except Exception as e:
        html = str(e)

    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
