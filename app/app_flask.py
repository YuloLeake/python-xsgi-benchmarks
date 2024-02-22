from flask import Flask, request, jsonify

from service import Service


app = Flask(__name__)
service = Service()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/pass-through-async", methods=['POST'])
def pass_through_async():
    return None, 404


@app.route("/pass-through-sync", methods=['POST'])
def pass_through_sync():
    data = request.get_json()
    data = service.pass_through_sync(data)
    return jsonify(data)


@app.route("/calc-distance-async", methods=['POST'])
def calc_distance_async():
    return None, 404


@app.route("/calc-distance-sync", methods=['POST'])
def calc_distance_sync():
    data = request.get_json()
    data = service.calc_distance_sync()
    return jsonify(data)
