from flask import Flask, render_template

from load import Roster, load

app = Flask(__name__)

r = Roster()
load(r)


@app.route("/")
def index():
    return render_template("index.html", r=r)


@app.route("/staff/<slug>")
def staff(slug):
    name = None
    for staff in r.stafflist:
        if staff.index == int(slug):
            name = staff.name
    return render_template("staff.html", r=r, name=name)


if __name__ == "__main__":
    app.run(port=5000)
