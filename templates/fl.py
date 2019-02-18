from flask import Flask, render_template, request, redirect
import json
from map import js_load, friends_locations, locations_to_coordinates, to_map

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/register", methods=["POST"])
def register():
    if not request.form.get("name"):
        return render_template("failure.html")
    acc = request.form.get("name")
    js = js_load(acc)
    friends = friends_locations(js)
    to_map(locations_to_coordinates(friends))
    return render_template("My_Map.html")


if __name__ == "__main__":
    app.run(debug=True)

