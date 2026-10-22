from flask import Flask, abort, render_template

from load import Roster, load

app = Flask(__name__)

r = Roster()
load(r)


@app.route("/")
def index():
    return render_template("index.html", r=r)


@app.route("/staff/<int:number>")
def staff(number):
    if number not in r.staff:
        abort(404)
    return render_template(
        "staff.html", r=r, staff=r.staff[number], duties=r.duties_for(number)
    )


if __name__ == "__main__":
    app.run(port=5000)
